import logging
from datetime import datetime
from bits_aviso_python_sdk.helpers.google import authenticate_google_service_account
from googleapiclient import _auth

logger = logging.getLogger(__name__)


class Chronicle:
    """A class to interact with Chronicle API."""

    # Default start and end times for Chronicle API are set to 12AM on the current day and the time the script is run.
    START_TIME = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
    END_TIME = datetime.now().isoformat() + 'Z'
    SCOPES = ['https://www.googleapis.com/auth/chronicle-backstory']

    def __init__(self, service_account_credentials):
        """Initializes the Chronicle class.

        Args:
            service_account_credentials (dict, str): The service account credentials in json format or the path to the
            credentials file.
        """
        credentials = authenticate_google_service_account(service_account_credentials, scopes=self.SCOPES)
        self.auth = _auth.authorized_http(credentials)
        self.url = 'https://backstory.googleapis.com/v1'

    def list_assets(self, start_time=START_TIME, end_time=END_TIME, page_size=100):
        """Lists the assets in Chronicle based on the given time range and page size.

        Args:
            start_time (str, optional): The start time for the query. Defaults to START_TIME.
            end_time (str, optional): The end time for the query. Defaults to END_TIME.
            page_size (int, optional): The number of assets to return per page. Defaults to 100.

        Returns:
			list[dict]: The list of assets from Chronicle.
        """
        url = f'{self.url}/artifact/listassets?start_time={start_time}&end_time={end_time}&page_size={page_size}'
        response = self.auth.request(url, 'GET')
        return response.json()
