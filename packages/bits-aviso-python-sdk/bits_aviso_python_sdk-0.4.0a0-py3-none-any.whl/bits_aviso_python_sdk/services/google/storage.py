import google.auth.exceptions
import logging
from google.api_core import exceptions
from google.cloud import storage
from bits_aviso_python_sdk.helpers.google import authenticate_google_service_account
from bits_aviso_python_sdk.helpers.parsers import parse_to_nldjson

logger = logging.getLogger(__name__)


class Storage:
	def __init__(self, service_account_credentials=None):
		"""Initializes the Storage class. If service account credentials are not provided,
		the credentials will be inferred from the environment.

		Args:
			service_account_credentials (dict, str, optional): The service account credentials in json format
			or the path to the credentials file. Defaults to None.
		"""
		if service_account_credentials:
			credentials = authenticate_google_service_account(service_account_credentials)
			self.client = storage.Client(credentials=credentials)
		else:
			try:
				self.client = storage.Client()
			except google.auth.exceptions.DefaultCredentialsError as e:
				logger.error(f"Unable to authenticate service account. {e}")
				self.client = None

	def create_blob(self, bucket, prefix, blob_name):
		"""Creates a blob in the specified bucket.

		Args:
			bucket (google.cloud.storage.bucket.Bucket): The bucket to create the blob in.
			prefix (string): The prefix to use for the blob. Typically, this is the name of the folder.
			blob_name (string): The name of the blob.

		Returns:

		"""
		try:
			# create the blob
			logger.info(f"Creating blob {prefix}/{blob_name} in bucket {bucket}...")
			blob = bucket.blob(f"{prefix}/{blob_name}")
			logger.info(f"Created blob {prefix}/{blob_name} in bucket {bucket}.")

			return blob  # return the blob

		except exceptions.NotFound:
			message = f"Bucket {bucket} not found. Cannot proceed with creating blob {prefix}/{blob_name}."
			logger.error(message)

			raise ValueError(message)

	def get(self, bucket_name):
		"""Gets the specified bucket.

		Args:
			bucket_name (string): The name of the bucket.

		Returns:
			google.cloud.storage.bucket.Bucket: The specified bucket.
		"""
		try:
			# get the bucket
			logger.info(f"Retrieving bucket {bucket_name}...")
			bucket = self.client.get_bucket(bucket_name)
			logger.info(f"Retrieved bucket {bucket_name}.")

			return bucket

		except exceptions.NotFound:
			message = f"Bucket {bucket_name} not found."
			logger.error(message)

			raise ValueError(message)

	def upload(self, bucket_name, prefix, blob_name, data, nldjson=False):
		"""Uploads the data to the specified bucket.

		Args:
			bucket_name (string): The name of the bucket.
			prefix (string): The prefix to use for the blob. Typically, the name of the dataset folder.
			blob_name (string): The name of the blob.
			data (str): The data to be uploaded to the bucket.
			nldjson (bool, optional): Whether to convert data to newline delimited json. Defaults to False.
		"""
		try:
			# get the bucket
			bucket = self.get(bucket_name)
			# create the blob
			blob = self.create_blob(bucket, prefix, blob_name)

			# check if the data needs to be converted to newline delimited json
			if nldjson:
				try:
					data = parse_to_nldjson(data)

				except TypeError:  # data is not a dictionary or a list of dictionaries, probably already converted
					raise ValueError("Unable to convert data to newline delimited json.")

			# upload the data
			logger.info(f"Uploading {prefix}/{blob_name} to {bucket_name}...")
			blob.upload_from_string(data)
			logger.info(f"Uploaded {prefix}/{blob_name} to {bucket_name}.")

		except ValueError as e:
			message = f"Unable to upload {blob_name} to {bucket_name}. {e}"
			logger.error(message)

			raise ValueError(message)  # raise an error with the message
