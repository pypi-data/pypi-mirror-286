
from typing import List

from pydantic import BaseModel


class GenerateInput(BaseModel):
    temperature: float
    prompt: str
    max_tokens: int = 50
    model: str = "command-light"
    model_kwargs: dict = {}


class SummarizeInput(BaseModel):
    temperature: float
    prompt: str
    additional_command: str = ""
    model: str = "command-light"
    model_kwargs: dict = {}


class CompletionInput(BaseModel):
    model: str = "text-davinci-003"
    prompt: str
    max_tokens: int = 50
    temperature: float = 0
    model_kwargs: dict = {}


class ChatCompletionInput(BaseModel):
    model: str = "gpt-3.5-turbo"
    messages: list = [
        {"role": "assistant", "content": "You are an intelligent assistant."}
    ]
    temperature: float = 0
    max_tokens: int = 2000
    model_kwargs: dict = {}


class EditInput(BaseModel):
    prompt: str
    instruction: str
    model: str = "text-davinci-edit-001"


class EmbeddingInput(BaseModel):
    embedding_texts: List[str]
    model: str = "text-embedding-ada-002"


class AWSBedrockTextInput(BaseModel):
    model: str
    max_tokens: int
    prompt: str = ""
    temperature: float = 0
    model_kwargs: dict = {}


class AWSBedrockEmbedInput(BaseModel):
    model: str
    max_tokens: int
    embedding_texts: List[str] = []
