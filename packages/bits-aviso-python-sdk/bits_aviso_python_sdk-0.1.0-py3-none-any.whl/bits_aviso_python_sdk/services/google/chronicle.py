import logging
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient import _auth


class Chronicle:
	"""A class to interact with Chronicle API."""

	# Default start and end times for Chronicle API are set to 12AM on the current day and the time the script is run.
	START_TIME = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
	END_TIME = datetime.now().isoformat() + 'Z'

	def __init__(self, service_account_credentials, ):
		self.auth = self.authenticate(service_account_credentials)
		self.base_url = 'https://backstory.googleapis.com/v1'

	def authenticate(self, service_account_credentials):
		"""Authenticates the service account with the Chronicle API and returns an authorized http object.

		Args:
			service_account_credentials (dict, str): The service account credentials in json format
			or the path to the credentials file.

		Returns:
			AuthorizedHttp: The authorized http object.
		"""
		scopes = ['https://www.googleapis.com/auth/chronicle-backstory']

		credentials = None
		if isinstance(service_account_credentials, dict):  # If credentials are provided as a dict
			try:
				credentials = service_account.Credentials.from_service_account_info(service_account_credentials,
																					scopes=scopes)
			except AttributeError as e:
				logging.error(f'Unable to authenticate service account with info. {e}')
		elif isinstance(service_account_credentials, str):  # If credentials are provided as a file path
			try:
				credentials = service_account.Credentials.from_service_account_file(service_account_credentials,
																					scopes=scopes)
			except AttributeError as e:
				logging.error(f'Unable to authenticate service account with file. {e}')

		if credentials:
			return _auth.authorized_http(credentials)
		else:
			logging.error('Authentication to Google Chronicle failed. No credentials provided.')
			return None

	def list_assets(self, start_time=START_TIME, end_time=END_TIME, page_size=100):
		"""Lists the assets in Chronicle based on the given time range and page size.

		Args:
			start_time (str, optional): The start time for the query. Defaults to START_TIME.
			end_time (str, optional): The end time for the query. Defaults to END_TIME.
			page_size (int, optional): The number of assets to return per page. Defaults to 100.

		Returns:

		"""
		url = f'{self.base_url}/artifact/listassets?start_time={start_time}&end_time={end_time}&page_size={page_size}'
		response = self.auth.request(url, 'GET')
		return response
