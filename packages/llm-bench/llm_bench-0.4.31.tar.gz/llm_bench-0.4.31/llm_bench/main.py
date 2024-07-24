import typer
import pkg_resources
import speedtest
import time
from .systeminfo import sysmain
from llm_bench import check_ollama, run_benchmark
import asyncio
import threading

app = typer.Typer()

def get_model_path(model: str) -> str:
    """ Helper function to return the correct file path based on the model size """
    return pkg_resources.resource_filename('llm_bench', f'data/{model}_models.yml')

@app.command()
def check_internet():
    """Check and print the internet speed."""
    try:
        start_time = time.time()
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000
        upload_speed = st.upload() / 1_000_000
        elapsed_time = time.time() - start_time
        print(f"Download Speed: {download_speed:.2f} Mbps")
        print(f"Upload Speed: {upload_speed:.2f} Mbps")
        print(f"Internet speed test duration: {elapsed_time:.2f} seconds")
    except speedtest.ConfigRetrievalError as e:
        print(f"Failed to retrieve speed test configuration: {e}")
    except speedtest.SpeedtestException as e:
        print(f"Failed to complete the speed test: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

@app.command()
def sysinfo():
    sys_info = sysmain.get_extra()
    print(f"system specs: {sys_info['specs']}")

@app.command()
def check_version(ollamabin: str = typer.Option('ollama', help="Path to the Ollama binary.")):
    ollama_version = check_ollama.check_ollama_version(ollamabin)
    print(f"ollama_version: {ollama_version} \n")

@app.command()
def run(
    ollamabin: str = typer.Option('ollama', help="Path to the Ollama binary."),
    model: str = typer.Option(
        "all", help="Select model: all-small, gemma-small, llama3-small, mistral-small, phi3-small, qwen-small, all-medium, gemma-medium, phi3-medium, llama3-medium, all-large, drbx-large, llama3-large",
        case_sensitive=False, show_choices=True
    ),
    test: bool = typer.Option(
        False, '--test', help="Flag to toggle between default and alternative benchmark tests."
    ),
    steps: int = typer.Option(
        10, help="Set the amount of inferences",
        min=1, max=10
    ),
    concurrent: int = typer.Option(
        1, '--concurrent', '-c', help="Number of concurrent users to simulate",
        min=1
    ),
    monitor_gpu: bool = typer.Option(
        False, '--monitor-gpu', help="Periodically monitor GPU during the benchmark."
    ),
    verbose: bool = typer.Option(
        False, '--verbose', help="Print the GPU timestamp data."
    )
):
    """Run the benchmark tests with optional periodic GPU monitoring."""


    benchmark_file = pkg_resources.resource_filename('llm_bench', 'data/benchmark_instructions.yml')
    models_file = get_model_path(model)

    if test:
        print(f"Testing pulled model(s)")

    results = asyncio.run(run_benchmark.run_benchmark(models_file, steps, benchmark_file, test, ollamabin, concurrent, monitor_gpu, verbose))


if __name__ == "__main__":
    app()