from glaider.authenticator import check_api_key
import requests
import datetime


class Protection:
    """Verifies for prompt injections and communicates the results to backend for analytics"""
    def __init__(self):
        self._glaider_api_key = None

    def _init(self, glaider_api_key):
        self._glaider_api_key = glaider_api_key

    @check_api_key
    def detect_prompt_injection(self, prompt: str) -> bool:
        response = requests.post('https://api.glaider.it/detect-prompt-injection', json={
            'prompt': prompt,
            'cid': self._glaider_api_key
        }, headers={'Content-Type': 'application/json'})

        if response.json()['is_prompt_injection']:
            self._notify_backend("Prompt Injection")
        return response.json()

    def _notify_backend(self, _type):
        response = requests.post('https://api.glaider.it/log-prompt', json={
            'username': "untracked",
            'department': "untracked",
            'action': "Detected",
            'risk': "high",
            'datetime': datetime.datetime.now().isoformat(),
            'type': _type,
            'detection': "Active",
            'models': "SDK - openai",
            'cid': self._glaider_api_key
        }, headers={'Content-Type': 'application/json'})
        print('Backend notified, response status:', response.status_code)


protection = Protection()
