import logging
import requests
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)


class SentinelOne:
	"""A class to interact with the SentinelOne API."""
	def __init__(self, token, domain='https://broadinstitute.sentinelone.net', version='v2.1'):
		"""Initializes the SentinelOne class. Authenticates by generating a token based on the username and password.
		A new token is generated every time the class is called.

		Args:
			token (str): The token to authenticate with.
			domain (str, optional): The domain to authenticate with. Defaults to 'https://broadinstitute.sentinelone.net'.
			version (str, optional): The version of the SentinelOne API to use. Defaults to 'v2.1'.
		"""
		self.domain = domain
		self.version = version
		self.token = token
		self.headers = {
			'Authorization': f'ApiToken {self.token}',
			'Content-Type': 'application/json'
		}
		self.check_token_expiration()  # check the token's expiration date

	def check_token_expiration(self):
		"""Checks the token's expiration date. If the token is set to expire in a week, TBD."""
		expiration = self.get_token_expiration()
		# datetime objects
		exp_date = datetime.strptime(expiration, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
		now = datetime.now(timezone.utc)

		# timedelta objects
		limit = timedelta(days=7)  # refresh if its 7 days until expiration
		delta = exp_date - now  # difference in time

		# pretty string of the time remaining
		remaining = str(delta).split(",")[0]

		if delta < limit:  # if there is less than 15 days remaining, refresh
			logger.warning(f'API authentication token expires in {remaining}.')
			# TODO: either regenerate the token or send a notification
		else:
			logger.info(f'API authentication token expires in {remaining}.')

	def get_token_expiration(self):
		"""Checks the token's expiration date. If the token is set to expire in a day, a new token is generated."""
		url = f'{self.domain}/web/api/{self.version}/users/api-token-details'

		try:
			payload = {
				"data": {
					"apiToken": self.token
				}
			}
			response = requests.post(url, headers=self.headers, json=payload)
			response.raise_for_status()
			expiration = response.json()['data']['expiresAt']
			return expiration

		except (requests.exceptions.RequestException, KeyError) as e:
			logger.error(f'Error checking token expiration: {e}')
			return

	def list_agents(self, limit=1000):
		"""Lists the agents in SentinelOne based on the given limit.
		Args:
			limit (int, optional): The number of agents to return. Defaults to 1000.

		Returns:
			list(dict): A list of agents in SentinelOne.
		"""
		url = f'{self.domain}/web/api/{self.version}/agents?limit={limit}'
		agents = []

		try:  # initial call in order to get the cursor
			response = requests.get(url, headers=self.headers)
			response.raise_for_status()  # raise an exception if the status code is not 200
			data = response.json()  # json data
			agents.extend(data['data'])  # add the initial agents to the list
			total = data['pagination']['totalItems']  # total number of agents
			logger.info(f"Retrieving agents from SentinelOne... {len(agents)}/{total}.")

			# if there are more agents to retrieve
			while 'nextCursor' in data['pagination'] and data['pagination']['nextCursor']:
				cursor = data['pagination']['nextCursor']  # get the cursor
				next_page_url = f'{url}&cursor={cursor}'  # add the cursor to the url
				response = requests.get(next_page_url, headers=self.headers)
				response.raise_for_status()  # raise an exception if the status code is not 200
				data = response.json()  # json data
				agents.extend(data['data'])  # add the agents to the list
				logger.info(f"Retrieving agents from SentinelOne... {len(agents)}/{total}.")

			# return the list of agents
			return agents

		except requests.exceptions.RequestException as e:
			logging.error(f'Error retrieving SentinelOne agents: {e}')
			return

		except (KeyError, AttributeError) as e:  # in case cursor is broken or something
			logging.error(f'Error retrieving cursor for S1 agents: {e}')
			return
