from glaider.providers.cohere_wrapper import CohereWrapper
from glaider.authenticator import check_api_key
import requests
import datetime


class CohereInterface:

    def __init__(self):
        self._glaider_api_key = None
        self._anonymization = True
        self._cohere_wrapper = None
        self._cohere_wrapper = CohereWrapper()

    def _init(self, glaider_api_key):
        self._glaider_api_key = glaider_api_key

    @property
    def api_key(self):
        return self._cohere_wrapper.get_api_key()

    @api_key.setter
    def api_key(self, value):
        self._cohere_wrapper.set_api_key(value)

    @check_api_key
    def generate(self,
            message: str,
            temperature: float = 0,
            max_tokens: int = 50,
            model: str = "command-light",
            **kwargs
    ):
        """
        Use Cohere's API to generate a response to a prompt.
        """
        resp, sensitive_detected = self._cohere_wrapper.send_cohere_request(
            "generate",
            model=model,
            prompt=message,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs
        )
        self._notify_backend(sensitive_detected)
        return resp

    @check_api_key
    def generate_stream(self,
            temperature: float,
            prompt: str,
            max_tokens: int = 50,
            model: str = "command-light",
            **kwargs
    ):
        resp, sensitive_detected = self._cohere_wrapper.send_cohere_request(
            "generate",
            model=model,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True,
            **kwargs
        )
        self._notify_backend(sensitive_detected)
        return resp

    @check_api_key
    def summarize(self,
            temperature: float,
            prompt: str,
            additional_command: str = "",
            model: str = "command-light",
            **kwargs
    ):
        resp, sensitive_detected = self._cohere_wrapper.send_cohere_request(
            "summarize",
            prompt=prompt,
            additional_command=additional_command,
            temperature=temperature,
            model=model,
            **kwargs
        )
        self._notify_backend(sensitive_detected)
        return resp

    def _notify_backend(self, sensitive_detected):
        for pii_detected in sensitive_detected:
            response = requests.post('https://api.glaider.it/log-prompt', json={
                'username': "untracked",
                'department': "untracked",
                'action': "Anonymized",
                'risk': pii_detected['risk'],
                'datetime': datetime.datetime.now().isoformat(),
                'type': pii_detected['type'],
                'detection': "sent",
                'models': "SDK - cohere",
                'cid': self._glaider_api_key
            }, headers={'Content-Type': 'application/json'})
            print('Backend notified, response status:', response.status_code)


cohere = CohereInterface()
