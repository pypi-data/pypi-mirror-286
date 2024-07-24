import random
import string
import uuid

from pydantic_core import PydanticCustomError

from core.common.messages import messages as _


def random_string(size: int = 20, format_string: str = None) -> str:
    return ''.join(random.choice(format_string) for _ in range(size))


def generate_password(length: int = 15) -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    password = 'Pa1@'.join(random.choice(characters) for _ in range(length))
    return password


def generate_uuid() -> str:
    return str(uuid.uuid4())
