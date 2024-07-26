# Python Worker Tracer Extension

This extension imports the Datadog Python Tracer, automatically patches all available modules, and creates a root span for an Azure Function.

## Usage

1. pip install the package 

    - `pip install dd-azure-worker-extension`

2. import it into the code of the function app

    - `import dd-azure-worker-extension`

3. Add the following environment variable to the Azure Function App
    - `PYTHON_ENABLE_WORKER_EXTENSIONS=1`
