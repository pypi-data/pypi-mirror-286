# llm-benchmark (ollama-benchmark)

LLM Benchmark for Throughput via Ollama (Local LLMs)

## Installation Steps

```bash
pip install llm-bench
```

## Usage for general users directly

```bash
llm_bench run
```

## ollama installation with the following models installed

7B model can be run on machines with 8GB of RAM

13B model can be run on machines with 16GB of RAM

## Usage explaination

On Windows, Linux, and macOS, it will detect memory RAM size to first download required LLM models.

When memory RAM size is greater than or equal to 4GB, but less than 7GB, it will check if gemma:2b exist. The program implicitly pull the model.

```bash
ollama pull gemma:2b
```

When memory RAM size is greater than 7GB, but less than 15GB, it will check if these models exist. The program implicitly pull these models

```bash
ollama pull gemma:2b
ollama pull gemma:7b
ollama pull mistral:7b
ollama pull llama2:7b
ollama pull llava:7b
```

When memory RAM siz is greater than 15GB, it will check if these models exist. The program implicitly pull these models

```bash
ollama pull gemma:2b
ollama pull gemma:7b
ollama pull mistral:7b
ollama pull llama2:7b
ollama pull llama2:13b
ollama pull llava:7b
ollama pull llava:13b
```

## Python Poetry manually(advanced) installation

<https://python-poetry.org/docs/#installing-manually>

## For developers to develop new features on Windows Powershell or on Ubuntu Linux or macOS

```bash
python3 -m venv .venv
. ./.venv/bin/activate
pip install -U pip setuptools
pip install poetry
```

## Usage in Python virtual environment

```bash
poetry shell
poetry install
llm_benchmark hello jason
```

### Example #1 send systeminfo and benchmark results to a remote server

```bash
llm_bench run
```

### Example #2 Do not send systeminfo and benchmark results to a remote server

```bash
llm_bench run --no-sendinfo
```

### Example #3 Benchmark run on explicitly given the path to the ollama executable (When you built your own developer version of ollama)

```bash
llm_bench run --ollamabin=~/code/ollama/ollama
```

## Reference

[Ollama](https://ollama.com)
