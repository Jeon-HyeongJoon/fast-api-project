import os
from uuid import uuid4


def ordered_uuid():
    [a, b, c, d, e] = str(uuid4()).split("-")
    return f"{c}{b}{a}{d}{e}"


def must(state, error: Exception):
    if not state:
        raise error


def get_environment() -> str:
    return os.environ.get("ENV", "local")
    # return os.environ.get("ENV", "docker")
