import json
import httpx
import llm
import os
import click
from pydantic import Field, field_validator
from typing import Optional, List, Generator

MODELS = [
    "databricks-dbrx-instruct",
    "databricks-meta-llama-3.1-405b-instruct",
    "databricks-meta-llama-3.1-70b-instruct",
    "databricks-meta-llama-3-70b-instruct",
    "databricks-llama-2-70b-chat",
    "databricks-mixtral-8x7b-instruct"
]

class DatabricksOptions(llm.Options):
    max_tokens: Optional[int] = Field(
        description="The maximum number of tokens to generate",
        default=None,
    )
    temperature: Optional[float] = Field(
        description="The sampling temperature",
        default=1.0,
    )
    top_p: Optional[float] = Field(
        description="The probability threshold for nucleus sampling",
        default=1.0,
    )
    top_k: Optional[int] = Field(
        description="The number of top tokens to consider for top-k-filtering",
        default=None,
    )
    stop: Optional[List[str]] = Field(
        description="Sequences where the model should stop generating further tokens",
        default_factory=list,
    )

    @field_validator("temperature")
    @classmethod
    def validate_temperature(cls, temperature):
        if not (0.0 <= temperature <= 2.0):
            raise ValueError("temperature must be in range 0.0-2.0")
        return temperature

    @field_validator("top_p")
    @classmethod
    def validate_top_p(cls, top_p):
        if not (0.0 < top_p <= 1.0):
            raise ValueError("top_p must be in range (0.0, 1.0]")
        return top_p

class DatabricksChat(llm.Model):
    can_stream = True

    class Options(DatabricksOptions):
        pass

    def __init__(self, model_id):
        self.model_id = model_id
        self.base_url = self.get_base_url()
        super().__init__()

    def get_base_url(self):
        base_url = os.environ.get("DATABRICKS_WORKSPACE_URL")
        if not base_url:
            config = self.load_config()
            base_url = config.get("base_url")
        if not base_url:
            raise ValueError("Databricks workspace URL not set. Please set the DATABRICKS_WORKSPACE_URL environment variable or use the databricks-config command.")
        base_url = base_url.rstrip('/')
        return base_url

    def load_config(self):
        config_path = llm.user_dir() / "llm-databricks-config.json"
        if config_path.exists():
            return json.loads(config_path.read_text())
        return {}

    def execute(self, prompt, stream, response, conversation) -> Generator[str, None, None]:
        key = llm.get_key("", "databricks", "LLM_DATABRICKS_KEY") or getattr(
            self, "key", None
        )
        messages = self.build_messages(prompt, conversation)
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        }
        data = {
            "messages": messages,
            "max_tokens": prompt.options.max_tokens,
            "temperature": prompt.options.temperature,
            "top_p": prompt.options.top_p,
            "top_k": prompt.options.top_k,
            "stop": prompt.options.stop,
            "stream": stream,
        }

        url = f"{self.base_url}/serving-endpoints/{self.model_id}/invocations"

        if stream:
            yield from self._stream_response(url, headers, data)
        else:
            yield from self._non_stream_response(url, headers, data, response)

    def _stream_response(self, url: str, headers: dict, data: dict) -> Generator[str, None, None]:
        with httpx.stream("POST", url, json=data, headers=headers) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if isinstance(line, bytes):
                    line = line.decode('utf-8')
                if line.startswith("data: "):
                    try:
                        chunk = json.loads(line[6:])
                        content = chunk["choices"][0]["delta"].get("content", "")
                        if content:
                            yield content
                    except json.JSONDecodeError:
                        continue  # Skip invalid JSON lines

    def _non_stream_response(self, url: str, headers: dict, data: dict, response) -> Generator[str, None, None]:
        r = httpx.post(url, json=data, headers=headers)
        r.raise_for_status()
        result = r.json()
        response.response_json = result
        content = result["choices"][0]["message"]["content"]
        yield content

    def build_messages(self, prompt, conversation) -> List[dict]:
        messages = []
        if conversation:
            for response in conversation.responses:
                messages.extend([
                    {"role": "user", "content": response.prompt.prompt},
                    {"role": "assistant", "content": response.text()},
                ])
        messages.append({"role": "user", "content": prompt.prompt})
        if prompt.system:
            messages.insert(0, {"role": "system", "content": prompt.system})
        return messages

@llm.hookimpl
def register_models(register):
    # Load custom models from JSON file
    custom_models_path = llm.user_dir() / "llm-databricks-models.json"
    if custom_models_path.exists():
        custom_models = json.loads(custom_models_path.read_text())
        models = custom_models
    else:
        models = MODELS

    for model_id in models:
        register(DatabricksChat(model_id))

@llm.hookimpl
def register_commands(cli):
    @cli.command(name="databricks-config")
    def databricks_config():
        "Configure Databricks model serving settings"
        config_path = llm.user_dir() / "llm-databricks-config.json"
        if config_path.exists():
            config = json.loads(config_path.read_text())
        else:
            config = {}
        click.echo("Databricks Configuration")
        click.echo("------------------------")
        click.echo("You can set the Databricks workspace URL using this command.")
        click.echo("")
        base_url = click.prompt(
            "Enter your Databricks workspace URL",
            default=config.get("base_url", os.environ.get("DATABRICKS_WORKSPACE_URL", ""))
        )
        config["base_url"] = base_url
        config_path.write_text(json.dumps(config, indent=2))
        click.echo(f"Configuration saved to {config_path}")
        click.echo("Remember, you can always override this setting with the DATABRICKS_WORKSPACE_URL environment variable.")
