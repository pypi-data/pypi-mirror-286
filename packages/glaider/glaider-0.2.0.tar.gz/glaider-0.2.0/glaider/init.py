from .interfaces.openai import openai
from .interfaces.cohere import cohere

from .protection.protection import protection

from .data_processor.data_processor import data_processor

from .authenticator import is_valid


def init(api_key: str) -> None:
    if not is_valid(api_key):
        raise Exception("API key is not valid")

    openai._init(glaider_api_key=api_key)
    cohere._init(glaider_api_key=api_key)

    protection._init(glaider_api_key=api_key)

    data_processor._init(glaider_api_key=api_key)
