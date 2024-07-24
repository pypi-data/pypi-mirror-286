import json
import logging
import google.auth.exceptions
from google.cloud import pubsub
from google.oauth2 import service_account

logger = logging.getLogger(__name__)


class Pubsub:
	"""Pubsub class for sending messages to a given pubsub topic."""

	def __init__(self, project_id, topic, service_account_credentials=None):
		"""Initializes the Pubsub class. If service account credentials are not provided,
		the credentials will be inferred from the environment.

		Args:
			project_id (str): The project id of the pubsub topic.
			topic (str): The pubsub topic's name.
			service_account_credentials (dict, str, optional): The service account credentials in json format
			or the path to the credentials file. Defaults to None.
		"""
		self.project = project_id
		self.topic = topic
		if service_account_credentials:
			credentials = authenticate_service_account(service_account_credentials)
			self.publisher_client = pubsub.PublisherClient(credentials=credentials)
		else:
			try:
				self.publisher_client = pubsub.PublisherClient()
			except google.auth.exceptions.DefaultCredentialsError as e:
				logger.error(f"Unable to authenticate service account. {e}")
				self.publisher_client = None

	def send(self, message):
		"""Publishes a message to a topic.

		Args:
			message (dict): The message body to post to the pubsub topic.
		"""
		try:
			topic_uri = self.publisher_client.topic_path(self.project, self.topic)
			logger.info(f"Attempting to publish message to {self.topic} in project {self.project}.")
			publish_future = self.publisher_client.publish(topic_uri, data=json.dumps(message, default=str).encode("utf-8"))
			publish_future.result()
			logger.info(f"Published message to {self.topic} in project {self.project}.")

		except AttributeError as e:
			logger.error(f"Unable to publish message to {self.topic} in project {self.project}. {e}")


def authenticate_service_account(service_account_credentials):
	"""Authenticates the service account given.

	Args:
		service_account_credentials (dict, str): The service account credentials.

	Returns:
		google.auth.credentials.Credentials: The authenticated service account credentials.
	"""
	try:
		if isinstance(service_account_credentials, dict):  # If credentials are provided as a dict
			credentials = service_account.Credentials.from_service_account_info(service_account_credentials)

		elif isinstance(service_account_credentials, str):  # If credentials are provided as a file path
			credentials = service_account.Credentials.from_service_account_file(service_account_credentials)

		else:  # If credentials are not provided as a dict or file path
			raise ValueError("Service account credentials must be provided as a dict or file path.")

		return credentials  # Return the authenticated service account credentials

	except (AttributeError, ValueError) as e:
		logger.error(f"Unable to authenticate service account. {e}")
		return
