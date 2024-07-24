# Glaider

Glaider is a Python library designed to facilitate safe interactions with generative AI tools. It aims to empower developers by providing features that prevent the exposure of sensitive data, mitigate risks associated with large language models (LLMs), and ensure secure AI interactions.

## Features

- **Data Protection**: Ensures that sensitive data is not exposed during interactions with AI models.
- **Prompt Injection Prevention**: Protects against malicious inputs that could manipulate AI behavior.
- **Interaction Monitoring**: Keeps a record of all interactions to audit and review as needed.
- **Risk Mitigation**: Implements strategies to reduce general risks in using LLMs.

## Installation

Install Glaider using pip:

```bash
pip install glaider
```

## Usage

Here's a quick example of how you can use Glaider to interact with generative AI models safely:

```python
## Usage Example

Below is a practical example of how you can use the `glaider` package to interact securely with generative AI services like OpenAI and Cohere:

```python
import glaider
from glaider import openai
from glaider import cohere

# Initialize Glaider with an API key and anonymization enabled
glaider.init(api_key='', anonymize=True)

# Set the API key for Cohere
cohere.api_key = ""

# Generate a response from Cohere, handling sensitive information
chat = cohere.generate(message="my secret email is secret@gmail.com, and my ip is 192.168.1.1")

# Create a chat completion with OpenAI's GPT-3.5 Turbo
resp = openai.chat_completion_create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are an helpful assistant"
        },
        {
            "role": "user",
            "content": "Hello, my email is secret@gmail.com, whats my email?"
        }
    ],
)
```

## Requirements

Glaider requires the following Python packages:

- cohere==4.11.2
- openai==0.27.8
- pydantic==1.10.9
- requests==2.31.0

## Development Status

This project is currently in Alpha. It is still under development and more features and improvements are planned.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

If you have any questions or feedback, please contact Lorenzo Abati at:

 - Email: [lorenzo@glaider.it](mailto:lorenzo@glaider.it)


We appreciate your interest in Glaider and look forward to improving it with your feedback!
