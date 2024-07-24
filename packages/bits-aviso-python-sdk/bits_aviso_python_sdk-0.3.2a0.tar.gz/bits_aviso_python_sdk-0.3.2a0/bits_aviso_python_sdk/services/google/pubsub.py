import json
import logging
import google.auth.exceptions
from google.cloud import pubsub
from bits_aviso_python_sdk.helpers.helpers import authenticate_google_service_account

logger = logging.getLogger(__name__)


class Pubsub:
	"""Pubsub class for sending messages to a given pubsub topic."""

	def __init__(self, project_id, service_account_credentials=None):
		"""Initializes the Pubsub class. If service account credentials are not provided,
		the credentials will be inferred from the environment.

		Args:
			project_id (str): The project id of the pubsub topic.
			service_account_credentials (dict, str, optional): The service account credentials in json format
			or the path to the credentials file. Defaults to None.
		"""
		self.project_id = project_id

		if service_account_credentials:
			credentials = authenticate_google_service_account(service_account_credentials)
			self.publisher_client = pubsub.PublisherClient(credentials=credentials)
		else:
			try:
				self.publisher_client = pubsub.PublisherClient()
			except google.auth.exceptions.DefaultCredentialsError as e:
				logger.error(f"Unable to authenticate service account. {e}")
				self.publisher_client = None

	def send(self, topic_name, message):
		"""Publishes a message to a topic.

		Args:
			topic_name (str): The name of the pubsub topic.
			message (dict): The message body to post to the pubsub topic.
		"""
		try:
			topic_uri = self.publisher_client.topic_path(self.project_id, topic_name)
			logger.info(f"Attempting to publish message to {topic_name} in project {self.project_id}.")
			publish_future = self.publisher_client.publish(topic_uri, data=json.dumps(message, default=str).encode("utf-8"))
			publish_future.result()
			logger.info(f"Published message to {topic_name} in project {self.project_id}.")

		except AttributeError as e:
			logger.error(f"Unable to publish message to {topic_name} in project {self.project_id}. {e}")



