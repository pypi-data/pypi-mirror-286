import os
import requests
import mlflow
from dotenv import load_dotenv
from modelhub.utils import handle_response

load_dotenv()

class ModelHub:
    """ A client for interacting with the ModelHub API. """
    
    def __init__(self, base_url, api_key=None):
        """
        Initializes a ModelHub object.

        Args:
            base_url (str): The base URL of the ModelHub API.
            api_key (str, optional): The API key for authentication. Defaults to None.
        """
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"} if api_key else {}

    def post(self, endpoint, json=None, params=None, files=None, data=None):
        """
        Sends a POST request to the specified endpoint.

        Args:
            endpoint (str): The endpoint to send the request to.
            json (dict, optional): JSON data to send in the request body. Defaults to None.
            params (dict, optional): Query parameters to include in the request. Defaults to None.
            files (dict, optional): Files to upload with the request. Defaults to None.
            data (dict, optional): Data to send in the request body. Defaults to None.

        Returns:
            The response from the server.
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(
            url, json=json, headers=self.headers, params=params, files=files, data=data
        )
        return handle_response(response)

    def get(self, endpoint, params=None):
        """
        Sends a GET request to the specified endpoint.

        Args:
            endpoint (str): The endpoint to send the request to.
            params (dict, optional): The query parameters to include in the request. Defaults to None.

        Returns:
            The response from the GET request.
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        return handle_response(response)

    def put(self, endpoint, json=None):
        """
        Sends a PUT request to the specified endpoint with the given JSON payload.

        Args:
            endpoint (str): The endpoint to send the request to.
            json (dict, optional): The JSON payload to include in the request. Defaults to None.

        Returns:
            The response from the server.

        Raises:
            Any exceptions raised by the underlying requests library.
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.put(url, json=json, headers=self.headers)
        return handle_response(response)

    def delete(self, endpoint):
        """
        Sends a DELETE request to the specified endpoint.

        Args:
            endpoint (str): The endpoint to send the DELETE request to.

        Returns:
            The response from the server.

        Raises:
            Exception: If there is an error in sending the request or handling the response.
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.delete(url, headers=self.headers)
        return handle_response(response)

    def mlflow(self):
        """
        Configures the MLflow tracking and registry URIs and sets environment variables for authentication.

        Returns:
            The configured mlflow object.
        """
        response = self.get("mlflow/tracking_uri")
        tracking_uri = response.get("tracking_uri")
        mlflow.set_tracking_uri(tracking_uri)

        response = self.get("mlflow/credentials")
        username = response.get("username")
        password = response.get("password")

        if username and password:
            mlflow.set_tracking_uri(tracking_uri)
            mlflow.set_registry_uri(tracking_uri)
            os.environ["MLFLOW_TRACKING_USERNAME"] = username
            os.environ["MLFLOW_TRACKING_PASSWORD"] = password

        return mlflow
