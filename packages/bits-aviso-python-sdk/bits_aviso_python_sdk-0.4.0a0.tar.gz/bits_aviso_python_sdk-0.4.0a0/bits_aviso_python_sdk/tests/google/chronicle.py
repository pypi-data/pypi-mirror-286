import os
from bits_aviso_python_sdk.services.google.chronicle import Chronicle


def test_list_assets(chronicle):
	"""Tests the list_assets method."""
	chronicle.list_assets()


def test():
	credentials = os.environ.get("DATA_MOVER")
	c = Chronicle(service_account_credentials=credentials)
	print(c.list_assets())


if __name__ == "__main__":
	# Add the parent directory of `services` to sys.path
	test()
