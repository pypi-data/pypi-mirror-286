# ModelHub SDK

ModelHub SDK for managing ML pipelines using FastAPI and Argo Workflows.

## Installation

Install the SDK using pip:

```sh
pip install modelhub
```

## Usage 

```sh
from modelhub.client import ModelHubClient
from modelhub.pipeline import Pipeline

client = ModelHubClient(api_base_url="http://your-modelhub-service-endpoint")

pipeline = Pipeline(client=client, config_path="path/to/your/pipeline.yaml")
created_pipeline = pipeline.create_pipeline()

print("Pipeline created with ID:", created_pipeline["pipeline_id"])

# Submit the pipeline for execution
pipeline_id = created_pipeline["pipeline_id"]
pipeline.submit(pipeline_id)
```