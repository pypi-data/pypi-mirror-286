import os
from bits_aviso_python_sdk.helpers.utilities import initialize_logger
from bits_aviso_python_sdk.services.sentinelone.sentinelone import SentinelOne


def test():
	"""Tests the SentinelOne class."""
	logger = initialize_logger()
	token = os.environ.get("SENTINELONE_TOKEN")
	s = SentinelOne(token)
	s.get_token_expiration()
	agents = s.list_agents()


if __name__ == '__main__':
	test()
