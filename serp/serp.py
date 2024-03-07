from internal.internal import Client, ApiCredentials, ClientAsync
from utils.defaults import SYNC_BASE_URL, ASYNC_BASE_URL
import asyncio


class Serp:
    def __init__(self, username, password):
        """
        Initializes a synchronous SERP client.

        Args:
            username (str): The username for API authentication.
            password (str): The password for API authentication.
        """
        api_credentials = ApiCredentials(username, password)
        self.client = Client(SYNC_BASE_URL, api_credentials)

    def get_resp(self, payload, config):
        """
        Processes the payload synchronously and fetches api response.

        Args:
            payload (dict): The payload for the request.

        Returns:
            dict: The response from the server after the job is completed.
        """
        # Remove empty or null values from the payload
        payload = {k: v for k, v in payload.items() if v is not None}

        return self.client.req(payload, "POST", config)


class SerpAsync:
    def __init__(self, username, password):
        """
        Initializes an asynchronous SERP client.

        Args:
            username (str): The username for API authentication.
            password (str): The password for API authentication.
        """
        api_credentials = ApiCredentials(username, password)
        self.client = ClientAsync(ASYNC_BASE_URL, api_credentials)

    async def get_resp(self, payload, config):
        """
        Processes the payload asynchronously and fetches api response.

        Args:
            payload (dict): The payload for the request.

        Returns:
            dict: The response from the server after the job is completed.
        """
        # Remove empty or null values from the payload
        payload = {k: v for k, v in payload.items() if v is not None}

        result = None

        try:
            result = await asyncio.wait_for(
                self.client.execute_with_timeout(payload, config),
                timeout=config["timeout"],
            )
        except asyncio.TimeoutError:
            print("The request timed out")

        return result
