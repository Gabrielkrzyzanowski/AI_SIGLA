# Report on T02 - Ollama HTTP Client + CLI Wrapper + Test Script 

## Python Virtual Environment 

A Python virtual environment is an isolated directory tree that contains its own Python interpreter and an independent set of installed packages. 

To initialize a virtual environment, execute the following command inside your project's root folder:
``` bash
python3 -m venv .venv
```

One must activate the environment before installing packages or running scripts.
``` bash
source .venv/bin/activate
```

With the environment active, the local package installer (pip) targets this isolated directory exclusively. To install all necessary software dependencies, reference the requirement manifest:
``` bash
pip install requirements.txt
``` 

> The -r flag is required when installing dependencies directly from a structured requirements.txt manifest file.

## Ollama HTTP Client + CLI Wrapper 

Ollama exposes a local REST API by default on port 11434. Using Python’s standard requests library, it is possible to build a custom HTTP client that handles payload serialization and communicates directly with locally deployed language models.

The implementation architecture is divided into two operational modules:
- `ollama_wrapper.py`: Handles backend integration, structuring JSON payloads to map endpoint expectations, managing headers, and returning API responses.
- `ollama_wrapper_caller.py`: Exposes backend capabilities directly to the terminal interface via the *click* package.

**Example Client Trigger Command:** 
``` bash
python ollama_wrapper.py --model gemma4:e4b-it-qat --temperature 0.7 --top_p 0.9 --system_prompt "You are a concise technical writer." "Summarize HTTP protocol features."
``` 

## Test Script  

To maintain system reliability and continuously verify API endpoint stability, an automated testing framework was implemented using pytest.

The test suite validates integration surfaces by programmatically triggering mock and live calls to the client. This guarantees that parameters pass through the HTTP body cleanly and that any response structure errors are caught early during development.

**Example Test Execution:**
``` bash
python -m pytest -vv tests/
```  

**Example Test Output:**
``` bash
======================================== test session starts =========================================
platform linux -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0 -- /home/gabriel/projects/AI_SIGLA/.venv/bin/python
cachedir: .pytest_cache
rootdir: /home/gabriel/projects/AI_SIGLA
collected 1 item

tests/test_ollama_client.py::TestClient::test_generate_stream PASSED                           [100%]

========================================= 1 passed in 12.14s =========================================
```  
