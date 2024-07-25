import json
import pathlib
import pytest
from pytest_httpx import IteratorStream
import llm

TEST_MODELS = [
    "databricks-dbrx-instruct",
    "databricks-meta-llama-3.1-405b-instruct"
]

@pytest.fixture(scope="session")
def llm_user_path(tmp_path_factory):
    tmpdir = tmp_path_factory.mktemp("llm")
    return str(tmpdir)

@pytest.fixture(autouse=True)
def mock_env(monkeypatch, llm_user_path):
    monkeypatch.setenv("LLM_DATABRICKS_KEY", "test_key")
    monkeypatch.setenv("LLM_USER_PATH", llm_user_path)
    monkeypatch.setenv("DATABRICKS_WORKSPACE_URL", "https://test.databricks.com")
    # Write a llm-databricks-models.json file
    (pathlib.Path(llm_user_path) / "llm-databricks-models.json").write_text(
        json.dumps(list(TEST_MODELS), indent=2)
    )

@pytest.fixture
def mocked_stream(httpx_mock):
    httpx_mock.add_response(
        url="https://test.databricks.com/serving-endpoints/databricks-dbrx-instruct/invocations",
        method="POST",
        stream=IteratorStream(
            [
                b'data: {"choices": [{"delta": {"content": "I am an AI"}, "index": 0}]}\n\n',
                b'data: {"choices": [{"delta": {"content": " assistant"}, "index": 0}]}\n\n',
                b'data: {"choices": [{"delta": {"content": "."}, "index": 0}]}\n\n',
            ]
        ),
        headers={"content-type": "text/event-stream"},
    )
    return httpx_mock

def test_stream(mocked_stream):
    model = llm.get_model("databricks-dbrx-instruct")
    response = model.prompt("How are you?")
    chunks = list(response)
    assert chunks == ["I am an AI", " assistant", "."]
    request = mocked_stream.get_request()
    assert json.loads(request.content) == {
        "messages": [{"role": "user", "content": "How are you?"}],
        "max_tokens": None,
        "temperature": 1.0,
        "top_p": 1.0,
        "top_k": None,
        "stop": [],
        "stream": True,
    }

def test_stream_with_options(mocked_stream):
    model = llm.get_model("databricks-dbrx-instruct")
    model.prompt(
        "How are you?",
        temperature=0.5,
        top_p=0.8,
        max_tokens=10,
        stop=["END"],
    ).text()
    request = mocked_stream.get_request()
    assert json.loads(request.content) == {
        "messages": [{"role": "user", "content": "How are you?"}],
        "max_tokens": 10,
        "temperature": 0.5,
        "top_p": 0.8,
        "top_k": None,
        "stop": ["END"],
        "stream": True,
    }

def test_no_stream(httpx_mock):
    httpx_mock.add_response(
        url="https://test.databricks.com/serving-endpoints/databricks-dbrx-instruct/invocations",
        method="POST",
        json={
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "I'm an AI assistant created by Databricks.",
                    },
                }
            ],
        },
    )
    model = llm.get_model("databricks-dbrx-instruct")
    response = model.prompt("What are you?", stream=False)
    assert response.text() == "I'm an AI assistant created by Databricks."

def test_get_base_url(monkeypatch):
    model = llm.get_model("databricks-dbrx-instruct")

    # Test with environment variable
    monkeypatch.setenv("DATABRICKS_WORKSPACE_URL", "https://env.databricks.com")
    assert model.get_base_url() == "https://env.databricks.com"

    # Test with config file
    monkeypatch.delenv("DATABRICKS_WORKSPACE_URL")
    config_path = llm.user_dir() / "llm-databricks-config.json"
    config_path.write_text(json.dumps({"base_url": "https://config.databricks.com"}))
    assert model.get_base_url() == "https://config.databricks.com"

    # Test with no configuration
    config_path.unlink()
    with pytest.raises(ValueError):
        model.get_base_url()