import datetime
import json
import logging
import os
from typing import Dict, Tuple

import jwt


def get_env_bool(key: str) -> bool:
    """ Handles the boolean environment variable assignment """
    if not key in os.environ:
        raise KeyError("No environment variable %s", key)
    
    if not os.environ[key] in ("True", "False"):
        raise AssertionError("Key %s is not proper boolean: %s", key, os.environ[key])
    
    return os.environ[key] == "True"

def text_to_dict(text_data: str | None, logger: logging.Logger) -> Dict:
    """
    Converts the given text data into a dictionary.

    Args:
        text_data (str): The text data to be converted.

    Returns:
        Dict: The converted dictionary.

    Raises:
        TypeError: If the payload is not a string, byte, or bytearray instance representing a json object.
    """
    logger.info("Text to dictionary data: %s", text_data)
    
    if not isinstance(text_data, (str, bytes, bytearray)):
        _msg = "Payload must be a string, byte, or bytearray instance representing a json object"
        logger.error(_msg)
        raise TypeError(_msg)

    data: Dict | None | any = json.loads(text_data)

    if not isinstance(data, Dict):
        _msg = "Payload must be a json object"
        logger.error(_msg)
        raise TypeError(_msg)

    logger.info("Payload received: %s", data)

    return data

def check_required_fields(data: Dict, logger: logging.Logger) -> Tuple[str, str, str]:
    """
    Check if the required fields are present in the data dictionary.

    Args:
        data (Dict): A dictionary containing the data to be checked.

    Returns:
        Tuple[str, str, str]: A tuple containing the values of the required fields.

    Raises:
        TypeError: If any of the required fields are missing or have an incorrect type.
    """
    logger.info("Checking fields: %s", data)
    
    # Extract the required fields from the data
    token: str | None = data.get("token")
    task: str | None = data.get("task")
    message: str | None = data.get("message")

    # Check if the required fields are present
    if not isinstance(token, str):
        _msg = "Token is missing"
        logger.error(_msg)
        raise TypeError(_msg)
    if not isinstance(task, str):
        _msg = "Task is missing"
        logger.error(_msg)
        raise TypeError(_msg)
    if not isinstance(message, str):
        _msg = "Message is missing"
        logger.error(_msg)
        raise TypeError(_msg)

    logger.info("Token: %s, Task: %s, Message: %s", token, task, message)

    return token, task, message

def decode_token(token: str, logger: logging.Logger) -> Dict:
    """
    Decode a JWT token and return the decoded payload.

    Args:
        token (str): The JWT token to decode.

    Returns:
        Dict: The decoded payload as a dictionary.

    Raises:
        jwt.exceptions.InvalidTokenError: If the token is invalid or expired.

    """
    logger.info("Decoding token: %s", token)
    
    passcode: str = os.getenv("CONSUMER_SECRET")
    decoded: Dict = jwt.decode(
        token,
        passcode,
        leeway=datetime.timedelta(seconds=1),
        algorithms=["HS256"],
        options={"require": ["exp"]},
    )

    logger.info("Token decoded: %s", decoded)

    username: str = decoded.get("username")
    logger.info("Username: %s", username)

    return username