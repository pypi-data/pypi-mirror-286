# tests/test_openai_wrapper.py
import pytest
from openai_wrapper import init, OpenAIWithLoggingAndAnalysis  # Adjust import path as needed


# Mock OpenAI client class
class MockOpenAIClient:
    def chat(self, completions):
        print("Mock response from OpenAI")


@pytest.fixture
def wrapper():
    """Fixture to initialize OpenAIWithLoggingAndAnalysis with a mock client."""
    client = MockOpenAIClient()
    return init(client)


@pytest.mark.parametrize("text, expected", [
    ("This is a normal request.", False),
    ("Please contact jane.doe@example.com for more info.", True),
    ("Call us at (123) 456-7890.", True),
    ("Our patent on quantum computing is pending approval.", True),
    ("John Doe's email is john.doe@example.com, regarding the trademark.", True)
])
def test_sensitive_info_detection(wrapper, capsys, text, expected):
    wrapper.chat_completions_create(text)
    captured = capsys.readouterr()
    assert ("Potential PII detected" in captured.out) == expected
    assert ("Potential IP-related content detected" in captured.out) == expected
