import datetime
import json
import logging

logger = logging.getLogger(__name__)


def parse_to_nldjson(data_to_parse, upload_date=True):
    """Parses the given data into newline delimited json.
    Adds the upload date to the payload and ensures the columns do not have invalid characters.

    Args:
        data_to_parse (dict, list[dict]): The data to be parsed.
        upload_date (bool, optional): Whether to add the upload date to the payload. Defaults to True.

    Returns:
        str: The newline delimited json.
    """
    # check if the data is valid
    if isinstance(data_to_parse, str):
        raise TypeError("Data to parse must be a dictionary or a list of dictionaries.")

    # string to store nldjson
    nld_json = ""

    # convert dict to list if there's only one item
    if isinstance(data_to_parse, dict):
        data_to_parse = [data_to_parse]

    # convert to newline delimited json
    if upload_date:  # add upload date to the payload
        for item in data_to_parse:
            item["upload_date"] = datetime.date.today().isoformat()
            nld_json += f"{json.dumps(item)}\n"

    else:  # upload date is not required
        for item in data_to_parse:
            nld_json += f"{json.dumps(item)}\n"

    return nld_json
