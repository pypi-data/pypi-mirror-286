import base64
from datetime import date
from collections.abc import Iterable
from typing import Any


def json_normalize_dict(source: dict[Any, Any]) -> dict[Any, Any]:
    """
    Turn the values in *source* into values that can be serialized to JSON, thus avoiding *TypeError*.

    Possible transformations:
        - *bytes* e *bytearray* are changed to *str* in *Base64* format
        - *date* and *datetime* are changed to their respective ISO formats
        - *Iterable* is changed into a *list*
        - all other types are left unchanged
    For convenience, the possibly modified *source* itself is returned.
    HAZARD: depending on the type of object contained in *source*, the final result may not be serializable.

    :param source: the dict to be made serializable
    """
    for key, value in source.items():
        if isinstance(value, dict):
            json_normalize_dict(source=value)
        elif isinstance(value, bytes | bytearray):
            source[key] = base64.b64encode(s=value).decode()
        elif isinstance(value, date):
            source[key] = value.isoformat()
        elif isinstance(value, Iterable) and not isinstance(value, str):
            source[key] = json_normalize_iterable(source=value)

    return source


def json_normalize_iterable(source: Iterable) -> list[Any]:
    """
    Return a new *list* containing the values in *source*, made serializable if necessary.

    Possible operations:
        - *bytes* e *bytearray* are changed to *str* in *Base64* format
        - *date* and *datetime* are changed to their respective ISO formats
        - *Iterable* is changed into a *list*
        - all other types are left unchanged
    The serialization allows for these values to be used in JSON strings.
    HAZARD: depending on the type of object contained in *source*, the final result may not be serializable.

    :param source: the dict to be made serializable
    :return: list with serialized values
    """
    result: list[Any] = []
    for value in source:
        if isinstance(value, dict):
            json_normalize_dict(source=value)
            result.append(value)
        elif isinstance(value, bytes | bytearray):
            result.append(base64.b64encode(value).decode())
        elif isinstance(value, date):
            result.append(value.isoformat())
        elif isinstance(value, Iterable) and not isinstance(value, str):
            result.append(json_normalize_iterable(source=value))
        else:
            result.append(value)

    return result
