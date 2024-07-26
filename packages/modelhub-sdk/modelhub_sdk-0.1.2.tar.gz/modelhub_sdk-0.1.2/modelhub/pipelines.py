import yaml
import base64
import logging
import requests
from modelhub.client import ModelHub

logger = logging.getLogger("modelhub.pipelines")


class Pipelines:
    def __init__(self, client: ModelHub):
        self.client = client

    def load_config(self, config_path):
        """
        Loads the configuration file from the given path.

        Args:
            config_path (str): The path to the configuration file.

        Returns:
            tuple: A tuple containing the pipeline configuration and the list of stages.
        """
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        pipeline_config = config.get("pipeline", {})
        return pipeline_config, config.get("stages", [])

    def create_stage(self, stage):
        """
        Create a stage for the pipeline.

        Args:
            stage (dict): A dictionary containing the stage information.

        Returns:
            dict: A dictionary representing the created stage.

        Raises:
            FileNotFoundError: If the script or requirements file specified in the stage dictionary is not found.

        """
        script, requirements = "", ""
        if "script" in stage and "requirements" in stage:
            with open(stage["script"], "r", encoding="utf-8") as f:
                script = f.read()
            with open(stage["requirements"], "r", encoding="utf-8") as f:
                requirements = f.read()
            script_encoded = base64.b64encode(script.encode()).decode()
            requirements_encoded = base64.b64encode(requirements.encode()).decode()
        else:
            script_encoded, requirements_encoded = None, None

        return {
            "name": stage["name"],
            "type": "python",
            "params": {},
            "depends_on": stage.get("depends_on", []),
            "script": script_encoded,
            "requirements": requirements_encoded,
            "resources": stage.get("resources", {}),
        }

    def search_pipeline(self, name):
        """
        Searches for a pipeline with the given name.

        Args:
            name (str): The name of the pipeline to search for.

        Returns:
            dict or None: The existing pipeline if found, or None if not found.

        Raises:
            requests.exceptions.HTTPError: If an HTTP error occurs.
            requests.exceptions.RequestException: If a general request error occurs.
        """
        try:
            existing_pipeline = self.client.get(f"pipelines/search?name={name}")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                existing_pipeline = None
            else:
                logger.error("HTTP error: %s", e.response.text)
                raise
        except requests.exceptions.RequestException as e:
            logger.error("Request error: %s", str(e))
            raise
        return existing_pipeline

    def create_or_update_pipeline(self, config_path):
        """
        Creates or updates a pipeline based on the provided configuration.

        Args:
            config_path (str): The path to the pipeline configuration file.

        Returns:
            dict: The response from the API containing the pipeline information.

        Raises:
            ValueError: If the pipeline configuration is invalid.
        """
        pipeline_config, stages = self.load_config(config_path)
        name = pipeline_config.get("name", "custom_pipeline")
        description = pipeline_config.get("description", "")
        experiment_id = pipeline_config.get("experiment_id", "")
        dataset_id = pipeline_config.get("dataset_id", "")
        image_tag = pipeline_config.get("image_tag", "")

        if (
            not name
            or not experiment_id
            or not dataset_id
            or not image_tag
            or not stages
        ):
            raise ValueError("Pipeline configuration is invalid")

        stages = [self.create_stage(stage) for stage in stages]

        ## handle if pipeline not exists

        existing_pipeline = self.search_pipeline(name)

        if existing_pipeline:
            return self.client.put(
                f"pipelines/{existing_pipeline['pipeline_id']}",
                {
                    "name": name,
                    "description": description,
                    "experiment_id": experiment_id,
                    "dataset_id": dataset_id,
                    "stages": stages,
                    "image_tag": image_tag,
                },
            )
        else:
            return self.client.post(
                "pipelines",
                {
                    "name": name,
                    "description": description,
                    "experiment_id": experiment_id,
                    "dataset_id": dataset_id,
                    "stages": stages,
                    "image_tag": image_tag,
                },
            )

    def submit(self, pipeline_id):
        """
        Submits a pipeline for execution.

        Args:
            pipeline_id (str): The ID of the pipeline to submit.

        Returns:
            Response: The response object returned by the API.
        """
        return self.client.post(f"pipelines/{pipeline_id}/submit")

    def get(self, pipeline_id):
        """
        Retrieves a pipeline by its ID.

        Args:
            pipeline_id (str): The ID of the pipeline to retrieve.

        Returns:
            dict: The pipeline information.

        Raises:
            Exception: If the pipeline cannot be found or an error occurs during retrieval.
        """
        return self.client.get(f"pipelines/{pipeline_id}")

    def list(self, page_number=1, page_size=10):
        """
        Retrieve a list of pipelines.

        Args:
            page_number (int, optional): The page number to retrieve. Defaults to 1.
            page_size (int, optional): The number of pipelines per page. Defaults to 10.

        Returns:
            dict: A dictionary containing the list of pipelines.

        """
        return self.client.get(
            "pipelines", params={"page_number": page_number, "page_size": page_size}
        )

    def delete(self, pipeline_id):
        """
        Deletes a pipeline with the specified pipeline_id.

        Args:
            pipeline_id (str): The ID of the pipeline to delete.

        Returns:
            dict: A dictionary containing the response from the API.

        Raises:
            SomeException: If there is an error while deleting the pipeline.
        """
        return self.client.delete(f"pipelines/{pipeline_id}")

    def get_logs(self, namespace, pod_name, container=None):
        """
        Retrieves the logs for a specific pod in a given namespace.

        Args:
            namespace (str): The namespace of the pod.
            pod_name (str): The name of the pod.
            container (str, optional): The name of the container within the pod. Defaults to None.

        Returns:
            dict: The logs for the specified pod.

        """
        return self.client.get(
            f"pipelines/logs/{namespace}/{pod_name}", params={"container": container}
        )
