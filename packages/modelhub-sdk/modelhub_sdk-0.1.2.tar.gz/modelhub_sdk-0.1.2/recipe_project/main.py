import logging
from modelhub.modelhub import ModelHub
from modelhub.pipelines import Pipelines

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Initialize the ModelHub client
modelhub = ModelHub(base_url="http://localhost:3000/api/v1")

created_pipeline = modelhub.pipelines.create_or_update_pipeline("config/pipeline.yaml")
print("Pipeline created/updated with ID:", created_pipeline["pipeline_id"])

# Submit the pipeline for execution
pipeline_id = created_pipeline["pipeline_id"]
modelhub.pipelines.submit(pipeline_id)