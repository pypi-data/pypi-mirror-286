


from typing import Union, Tuple, List, Dict
import glaider


def scrub_all(text: Union[str, Dict[str, Union[str, Dict]]]) -> Tuple[Union[str, Dict], List[Dict[str, str]]]:
    """
    Scrub all PII in text using predefined patterns and report the types of PII found and their risks.

    :param text: Input to be scrubbed of PII
    :type text: str | dict
    :return: Tuple containing the scrubbed input text and a list of detected PII types with their risks
    :rtype: Tuple[Union[str, dict], List[Dict[str, str]]]
    """

    response_json = glaider.data_processor.anonymize_pii(text['content']).json()
    print(response_json)

    anonymized_message = text

    anonymized_message['content'] = response_json['anonymized_text']

    entities = [{'type': key.strip('[]'), 'risk': 'Low'} for key in response_json['entities']]

    print(anonymized_message, entities)

    return anonymized_message, entities

