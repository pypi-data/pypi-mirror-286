
import datetime
import json
from typing import Iterator, Optional

import cohere
from cohere.responses.generation import StreamingText


from glaider.entities.pii_scrubber import scrub_all
from glaider.entities.utils import StreamProcessor


SUPPORTED_COHERE_ENDPOINTS = ["generate", "summarize"]


class CohereWrapper:
    """
    This is a simple wrapper around the Cohere API client, which adds
    PII scrubbing before requests are sent, and DB logging after responses
    are received
    """

    def __init__(self) -> None:
        pass

    def get_api_key(self):
        try:
            return self.cohere_client.api_key
        except AttributeError:
            return None

    def set_api_key(self, value):
        self.cohere_client = cohere.Client(value)

    def _validate_cohere_endpoint(self, endpoint: str) -> None:
        """
        Check if endpoint is a supported Cohere endpoint, else raise an error

        :param endpoint: The name of a Cohere endpoint
        :type endpoint: str
        :raises NotImplementedError: Raised if endpoint is not a supported Cohere endpoint
        """
        if endpoint not in SUPPORTED_COHERE_ENDPOINTS:
            raise NotImplementedError(
                f"Cohere endpoint must be one of `{SUPPORTED_COHERE_ENDPOINTS}`"
            )

    def _call_summarize_endpoint(
        self,
        text: str,
        additional_command: str,
        model: str,
        temperature: float,
        **kwargs,
    ):
        """
        Call the summarize endpoint from the Cohere client and return response

        :param text: Text to summarize
        :type text: str
        :param additional_command: Command providing instructions
        :type additional_command: str
        :param model: Model to hit
        :type model: str
        :param temperature: Temperature altering the creativity of the response
        :type temperature: float
        :return: Response from Cohere
        :rtype: _type_
        """
        return self.cohere_client.summarize(
            model=model,
            text=text,
            temperature=temperature,
            additional_command=additional_command,
            **kwargs,
        )

    def _call_generate_endpoint(
        self,
        prompt: str,
        model: str,
        max_tokens: int,
        temperature: float,
        stream: bool = False,
        **kwargs,
    ):
        """
        Call the generate endpoint from the Cohere client and return response

        :param prompt: String prompt
        :type prompt: str
        :param model: Model to hit
        :type model: str
        :param max_tokens: Maximum tokens for prompt and completion
        :type max_tokens: int
        :param temperature: Temperature altering the creativity of the response
        :type temperature: float
        :return: Response from Cohere
        :rtype: _type_
        """
        resp = self.cohere_client.generate(
            model=model,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=stream,
            **kwargs,
        )
        return resp

    def _flatten_cohere_response(self, cohere_response):
        """
        Flatten response from Cohere as JSON

        :param cohere_response: Raw response from Cohere
        :type cohere_response: _type_
        :return: Flattened Cohere response as JSON
        :rtype: _type_
        """
        return json.loads(json.dumps(cohere_response, default=lambda o: o.__dict__))

    def send_cohere_request(
        self,
        endpoint: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        prompt: Optional[str] = None,
        temperature: Optional[float] = 0,
        stream: bool = False,
        additional_command: Optional[str] = "",
        **kwargs,
    ):
        """
        Send a request to the Cohere API and log interaction to the DB

        :param endpoint: Valid Cohere endpoint to hit
        :type endpoint: str
        :param model: Model to hit, defaults to None
        :type model: Optional[str], optional
        :param max_tokens: Maximum tokens for prompt and completion, defaults to None
        :type max_tokens: Optional[int], optional
        :param prompt: String prompt, defaults to None
        :type prompt: Optional[str], optional
        :param temperature: Temperature altering the creativity of the response, defaults to 0
        :type temperature: Optional[float], optional
        :param additional_command: Additional command used for summarization
        :type additional_command: Optional[str], optional
        :param kwargs: other parameters to pass to cohere api.
        :type kwargs: Optional[dict]
        :return: Flattened response from Cohere
        :rtype: _type_
        """
        self._validate_cohere_endpoint(endpoint)

        # Scrub sensitive information and get PII details
        prompt, pii_detected = scrub_all(prompt)

        if endpoint == "generate":
            result = self._call_generate_endpoint(
                prompt, model, max_tokens, temperature, stream, **kwargs
            )
        elif endpoint == "summarize":
            result = self._call_summarize_endpoint(
                prompt, additional_command, model, temperature, **kwargs
            )

        if not stream:
            cohere_response = self._flatten_cohere_response(result)
        else:
            stream_processor = StreamProcessor(stream_processor=stream_generator_cohere)
            cohere_response = stream_processor.process_stream(result)
            self._cached_response = stream_processor.get_cached_streamed_response()

        return cohere_response, pii_detected

    # def write_logs_to_db(self, db_logs: dict):
    #     if isinstance(db_logs["cohere_response"], list):
    #         db_logs["cohere_response"] = "".join(db_logs["cohere_response"])
    #     write_record_to_db(CohereRequests(**db_logs))


def stream_generator_cohere(generator: Iterator) -> Iterator[dict]:
    chunk: StreamingText
    for chunk in generator:
        yield chunk.text
