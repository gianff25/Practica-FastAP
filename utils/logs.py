import json
from datetime import date, datetime


def log(obj: dict):
    """
    Logs the provided dictionary object to a file.

    The provided dictionary `obj` is modified to include the current timestamp (`time`) in ISO 8601 format.
    The modified dictionary is then appended to a file named with the current date in the `logs` directory.

    :param obj: The dictionary object to be logged.
    """
    obj["time"] = datetime.utcnow().isoformat()
    with open(f"logs/{date.today()}.txt", "a") as f:
        f.write(json.dumps(obj) + "\n")
