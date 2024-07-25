import json
import logging
import google.auth.exceptions
import google.api_core.exceptions
from google.cloud import secretmanager
from bits_aviso_python_sdk.helpers.google import authenticate_google_service_account

logger = logging.getLogger(__name__)


class SecretManager:
	"""SecretManager class to interface with Google's Secret Manager API."""

	def __init__(self, service_account_credentials=None):
		"""Initializes the SecretManager class. If service account credentials are not provided,
		the credentials will be inferred from the environment.

		Args:
			service_account_credentials (dict, str, optional): The service account credentials in json format
			or the path to the credentials file. Defaults to None.
		"""
		self.client = secretmanager.SecretManagerServiceClient()

		if service_account_credentials:
			credentials = authenticate_google_service_account(service_account_credentials)
			self.client = secretmanager.SecretManagerServiceClient(credentials=credentials)
		else:
			try:
				self.client = secretmanager.SecretManagerServiceClient()

			except google.auth.exceptions.DefaultCredentialsError as e:
				logger.error(f"Unable to authenticate service account. {e}")
				self.publisher_client = None

	def get_secret(self, project_id, secret_name, secret_version="latest"):
		"""Gets the secret data from secret manager.

		Args:
			project_id (string): The project id of the secret.
			secret_name (string): The name of the secret.
			secret_version (string, optional): The version of the secret. Defaults to "latest".

		Returns:
			str, dict: The secret data from secret manager.
		"""
		try:
			client = secretmanager.SecretManagerServiceClient()
			secret = client.secret_version_path(project_id, secret_name, secret_version)
			response = client.access_secret_version(request={"name": secret})

			try:  # try to parse the secret data as json
				secret_data = json.loads(response.payload.data.decode("UTF-8"))

			except json.JSONDecodeError:  # if it fails, return the data as is
				secret_data = response.payload.data.decode("UTF-8")

			return secret_data

		except (google.api_core.exceptions.NotFound, google.api_core.exceptions.InvalidArgument) as e:
			message = f'Unable to get the secret {secret_name} from secret manager. {e} '
			logging.error(message)  # logging message

			raise ValueError(message)  # raise an error with the message
