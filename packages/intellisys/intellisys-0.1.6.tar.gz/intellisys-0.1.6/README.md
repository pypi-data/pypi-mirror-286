# Intellisys

Intellisys is a Python library that provides intelligence/AI services for the Lifsys Enterprise. It offers a unified interface to interact with various AI models and services, including OpenAI, Anthropic, Google, and more.

## Installation

You can install Intellisys using pip:

```
pip install intellisys
```

For the latest development version, you can install directly from GitHub:

```
pip install git+https://github.com/lifsys/intellisys.git
```

## Requirements

- Python 3.6 or higher
- A 1Password Connect server (for API key management)
- Environment variables:
  - `OP_CONNECT_TOKEN`: Your 1Password Connect token
  - `OP_CONNECT_HOST`: The URL of your 1Password Connect server

**Note**: If no local 1Password Connect server is available, the library will fail to retrieve API keys.

## Features

- Support for multiple AI models (OpenAI, Anthropic, Google, TogetherAI, Groq, MistralAI)
- Secure API key management using 1Password Connect
- JSON formatting and template rendering
- Asynchronous assistant interactions
- Template-based API calls

## Usage

Here's a quick example of how to use Intellisys:

```python
from intellisys import get_completion_api

# Make sure OP_CONNECT_TOKEN and OP_CONNECT_HOST are set in your environment

response = get_completion_api("Hello, how are you?", "gpt-4")
print(response)
```

### Advanced Usage

```python
from intellisys import template_api_json, get_assistant

# Using a template for API calls
render_data = {"user_name": "Alice"}
system_message = "You are a helpful assistant. Greet {{user_name}}."
response = template_api_json("gpt-4", render_data, system_message, "friendly_assistant")
print(response)

# Using an OpenAI assistant
assistant_id = "your_assistant_id"
reference = "What's the weather like today?"
responses = get_assistant(reference, assistant_id)
for response in responses:
    print(response)
```

## Supported Models

Intellisys supports a variety of AI models:

- OpenAI: gpt-4o-mini, gpt-4, gpt-4o
- Anthropic: claude-3.5
- Google: gemini-flash
- TogetherAI: llama-3-70b, llama-3.1-large
- Groq: groq-llama, groq-fast
- MistralAI: mistral-large

## API Reference

For detailed information on available functions and their usage, please refer to the docstrings in the source code.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
