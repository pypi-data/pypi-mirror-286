import logging
from google.oauth2 import service_account

logger = logging.getLogger(__name__)


def authenticate_google_service_account(service_account_credentials, scopes=None):
    """Authenticates the service account given.

    Args:
        service_account_credentials (dict, str): The service account credentials.
        scopes (list[str], optional): The scopes for the service account. Defaults to None.

    Returns:
        google.auth.credentials.Credentials: The authenticated service account credentials.
    """
    try:
        if isinstance(service_account_credentials, dict):  # If credentials are provided as a dict
            if scopes:  # If scopes are provided, use them
                credentials = service_account.Credentials.from_service_account_info(service_account_credentials,
                                                                                    scopes=scopes)
            else:
                credentials = service_account.Credentials.from_service_account_info(service_account_credentials)

        elif isinstance(service_account_credentials, str):  # If credentials are provided as a file path
            if scopes:  # If scopes are provided, use them
                credentials = service_account.Credentials.from_service_account_file(service_account_credentials,
                                                                                    scopes=scopes)
            else:
                credentials = service_account.Credentials.from_service_account_file(service_account_credentials)

        else:  # If credentials are not provided as a dict or file path
            raise ValueError("Service account credentials must be provided as a dict or file path.")

        return credentials  # Return the authenticated service account credentials

    except (AttributeError, ValueError) as e:
        logger.error(f"Unable to authenticate service account. {e}")
        return
