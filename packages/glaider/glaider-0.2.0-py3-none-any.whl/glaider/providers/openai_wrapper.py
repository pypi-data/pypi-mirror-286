
import datetime
import json
from typing import Optional, List, Dict, Union, Tuple, Iterator


import openai

from glaider.entities.pii_scrubber import scrub_all
from glaider.entities.utils import StreamProcessor, max_retries


SUPPORTED_OPENAI_ENDPOINTS = {
    "Model": ("list", "retrieve"),
    "ChatCompletion": ("create"),
    "Completion": ("create"),
    "Edits": ("create"),
    "Embedding": ("create"),
}


class OpenAIWrapper:
    """
    This is a simple wrapper around the OpenAI API client, which adds
    PII scrubbing before requests are sent, and DB logging after responses
    are received
    """

    def __init__(self) -> None:
        pass

    def get_api_key(self):
        return openai.api_key

    def set_api_key(self, value):
        openai.api_key = value

    def _validate_openai_endpoint(self, module: str, endpoint: str) -> None:
        """
        Check if module and endpoint are supported in OpenAI, else raise an error

        :param module: The name of an OpenAI module (i.e. "Completion")
        :type module: str
        :param endpoint: The name of an OpenAI endpoint (i.e. "create")
        :type endpoint: str
        :raises NotImplementedError: Raised if OpenAI module or endpoint is not supported
        """
        if module not in SUPPORTED_OPENAI_ENDPOINTS:
            raise NotImplementedError(
                f"`openai_endpoint` must be one of `{SUPPORTED_OPENAI_ENDPOINTS.keys()}`"
            )

        if endpoint not in SUPPORTED_OPENAI_ENDPOINTS[module]:
            raise NotImplementedError(
                f"`{endpoint}` not supported action for `{module}`"
            )

    def _call_model_endpoint(self, endpoint: str, model: Optional[str] = None):
        """
        List or retrieve model(s) from OpenAI

        :param endpoint: Whether to "list" models or "retrieve" a model
        :type endpoint: str
        :param model: Name of model, if "retrieve" is passed, defaults to None
        :type model: Optional[str]
        :raises Exception: Raised if endpoint is "retrieve" and model is unspecified
        :return: List of models or retrieved model
        :rtype: _type_
        """
        if endpoint == "list":
            return openai.Model.list()
        elif endpoint == "retrieve":
            if not model:
                raise Exception("retrieve model needs model name as input")
            return openai.Model.retrieve(model)

    @max_retries(3)
    def _call_completion_endpoint(
        self,
        model: str,
        prompt: str,
        max_tokens: int,
        temperature: Optional[float] = 0,
        stream=False,
        **kwargs,
    ):
        """
        Call the completion endpoint from the OpenAI client and return response
        :param model: Model to hit
        :type model: str
        :param prompt: String prompt
        :type prompt: str
        :param max_tokens: Maximum tokens for prompt and completion
        :type max_tokens: int
        :param temperature: Temperature altering the creativity of the response
        :type temperature: Optional[float]
        :param stream: Return streamed response, defaults to False
        :type stream: bool
        :param kwargs: other parameters to pass to interfaces api.
        :type kwargs: Optional[dict]
        :return: Response from OpenAI
        :rtype: _type_
        """
        return openai.Completion.create(
            model=model,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=stream,
            **kwargs,
        )

    @max_retries(3)
    def _call_chat_completion_endpoint(
        self,
        model: str,
        messages: list,
        temperature: Optional[float] = 0,
        stream=False,
        **kwargs,
    ):
        """
        Call the chat completion endpoint from the OpenAI client and return response

        :param model: Model to hit
        :type model: str
        :param messages: List of messages in the chat so far
        :type messages: list
        :param temperature: Temperature altering the creativity of the response, defaults to 0
        :type temperature: Optional[float]
        :param stream: Return streamed response, defaults to False
        :type stream: bool
        :param kwargs: other parameters to pass to interfaces api. (ie- functions, function_call, etc.)
        :type kwargs: Optional[dict]
        :return: Response from OpenAI
        :rtype: _type_
        """
        return openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=stream,
            **kwargs,
        )

    @max_retries(3)
    def _call_edits_endpoint(self, model: str, input: str, instruction: str):
        """
        Call the edits endpoint from the OpenAI client and return response

        :param model: Model to hit
        :type model: str
        :param input: String to perform the edit on
        :type input: str
        :param instruction: How to edit the input string
        :type instruction: str
        :param stream: Return streamed response, defaults to False
        :type stream: bool
        :return: Response from OpenAI containing edited input
        :rtype: _type_
        """
        return openai.Edit.create(model=model, input=input, instruction=instruction)

    @max_retries(3)
    def _call_embedding_endpoint(self, model: str, texts: List[str]):
        """
        Call the embedding endpoint from the OpenAI client and return response

        :param model: Model to hit
        :type model: str
        :param texts: List of strings to embed
        :type texts: List[str]
        :return: Response from OpenAI containing embeddedings
        :rtype: _type_
        """
        return openai.Embedding.create(input=texts, model=model)

    def send_openai_request(
            self,
            openai_module: str,
            endpoint: str,
            stream: bool = False,
            model: Optional[str] = None,
            max_tokens: Optional[int] = None,
            prompt: Optional[str] = None,
            temperature: Optional[float] = 0,
            messages: Optional[List[Dict[str, str]]] = None,
            instruction: Optional[str] = None,
            embedding_texts: Optional[List[str]] = None,
            **kwargs,
    ) -> Tuple[Union[Dict, Iterator[str]], List[Dict[str, str]]]:
        """
        Send a request to the OpenAI API and return response and logs for db write

        :param openai_module: Valid OpenAI module to hit (i.e. "Completion")
        :type openai_module: str
        :param endpoint: Valid OpenAI endpoint to hit (i.e. "create")
        :type endpoint: str
        :param model: Model to hit, defaults to None
        :type model: Optional[str]
        :param max_tokens: Maximum tokens for prompt and completion, defaults to None
        :type max_tokens: Optional[int]
        :param prompt: _description_, defaults to None
        :type prompt: String prompt, if calling completion or edits, optional
        :param temperature: Temperature altering the creativity of the response, defaults to 0
        :type temperature: Optional[float]
        :param messages: list of messages for chat endpoint
        :type messages: Optional[list]
        :param instruction: How to perform edits, if calling edits, defaults to None
        :type instruction: Optional[str]
        :param embedding_texts: List of prompts, if calling embedding, defaults to None
        :type embedding_texts: Optional[list]
        :param kwargs: other parameters to pass to interfaces api. (ie- functions, function_call, etc.)
        :type kwargs: Optional[dict]
        :return: Flattened response from OpenAI
        :rtype: _type_
        """
        self._validate_openai_endpoint(openai_module, endpoint)

        pii_details = []  # Store PII details for all elements

        # Scrub and capture PII details
        if messages:
            scrubbed_messages = []
            for message in messages:
                scrubbed_message, detected_pii = scrub_all(message)
                scrubbed_messages.append(scrubbed_message)
                pii_details.extend(detected_pii)
            messages = scrubbed_messages

        if prompt:
            prompt, detected_pii = scrub_all(prompt)
            pii_details.extend(detected_pii)

        if embedding_texts:
            scrubbed_texts = []
            for text in embedding_texts:
                scrubbed_text, detected_pii = scrub_all(text)
                scrubbed_texts.append(scrubbed_text)
                pii_details.extend(detected_pii)
            embedding_texts = scrubbed_texts

        if instruction:
            instruction, detected_pii = scrub_all(instruction)
            pii_details.extend(detected_pii)

        # Call endpoints based on the OpenAI module type
        if openai_module == "Model":
            result = self._call_model_endpoint(endpoint, model)
        elif openai_module == "Completion":
            result = self._call_completion_endpoint(
                model, prompt, max_tokens, temperature, stream, **kwargs
            )
        elif openai_module == "ChatCompletion":
            result = self._call_chat_completion_endpoint(
                model, messages, temperature, stream, **kwargs
            )
        elif openai_module == "Edits":
            result = self._call_edits_endpoint(model, prompt, instruction)
        elif openai_module == "Embedding":
            result = self._call_embedding_endpoint(model, embedding_texts)

        return result, pii_details
        #
        # if not stream:
        #     openai_response = result.to_dict()
        #     cached_response = openai_response
        # elif openai_module == "ChatCompletion":
        #     stream_processor = StreamProcessor(
        #         stream_processor=stream_generator_openai_chat
        #     )
        #     openai_response = stream_processor.process_stream(result)
        #     cached_response = stream_processor.get_cached_streamed_response()
        # elif openai_module == "Completion":
        #     stream_processor = StreamProcessor(
        #         stream_processor=stream_generator_openai_completion
        #     )
        #     openai_response = stream_processor.process_stream(result)
        #     cached_response = stream_processor.get_cached_streamed_response()
        # # The cached streaming response is an empty list at this point.
        # # Once the stream is returned to the user it will be populated
        # # Since the DB write happens after the stream, this will always be populated
        #
        # return openai_response

    # def write_logs_to_db(self, db_logs: dict):
    #     if isinstance(db_logs["openai_response"], list):
    #         db_logs["openai_response"] = "".join(db_logs["openai_response"])
    #     write_record_to_db(OpenAIRequests(**db_logs))


def stream_generator_openai_chat(generator: Iterator) -> Iterator[str]:
    for chunk in generator:
        answer = ""
        try:
            current_response = chunk["choices"][0]["delta"]["content"]
            answer += current_response
        except KeyError:
            pass
        yield answer


def stream_generator_openai_completion(generator: Iterator) -> Iterator[str]:
    for chunk in generator:
        answer = ""
        try:
            current_response = chunk["choices"][0]["text"]
            answer += current_response
        except KeyError:
            pass
        yield answer
