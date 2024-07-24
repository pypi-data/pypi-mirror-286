from glaider.authenticator import check_api_key
import requests


class DataProcessor:
    """Anonymizes data from personal identifiable information and sensitive data"""
    def __init__(self):
        self._glaider_api_key = None

    def _init(self, glaider_api_key):
        self._glaider_api_key = glaider_api_key

    @check_api_key
    def anonymize_pii(self, text: str):
        url = 'https://api.glaider.it/anonymize-pii'
        payload = {
            'prompt': text,
            'cid': self._glaider_api_key
        }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(url, json=payload, headers=headers)

        return response


data_processor = DataProcessor()
