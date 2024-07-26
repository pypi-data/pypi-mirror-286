"""
Provides intelligence/AI services for the Lifsys Enterprise.

This module requires a 1Password Connect server to be available and configured.
The OP_CONNECT_TOKEN and OP_CONNECT_HOST environment variables must be set
for the onepasswordconnectsdk to function properly.
"""
__version__ = "0.2.0"
import os
import json
from time import sleep
from typing import Optional, Dict, List
from openai import OpenAI
from litellm import completion
from jinja2 import Template
from onepasswordconnectsdk import new_client_from_environment

def get_api(item: str, key_name: str, vault: str = "API") -> str:
    """
    Retrieve an API key from 1Password.

    This function connects to a 1Password vault using the onepasswordconnectsdk
    and retrieves a specific API key. It requires the OP_CONNECT_TOKEN and
    OP_CONNECT_HOST environment variables to be set for proper functionality.

    Args:
        item (str): The name of the item in 1Password containing the API key.
        key_name (str): The specific field name within the item that holds the API key.
        vault (str, optional): The name of the 1Password vault to search in. Defaults to "API".

    Returns:
        str: The retrieved API key as a string.

    Raises:
        Exception: If there's an error connecting to 1Password or retrieving the key.
            The exception message will include details about the specific error encountered.

    Example:
        >>> api_key = get_api("OpenAI", "API_KEY", "Development")
        >>> print(api_key)
        'sk-1234567890abcdef1234567890abcdef'
    """
    try:
        client = new_client_from_environment()
        item = client.get_item(item, vault)
        for field in item.fields:
            if field.label == key_name:
                return field.value
    except Exception as e:
        raise Exception(f"Connect Error: {e}")

def fix_json(json_string: str) -> str:
    """
    Fix and format a JSON string using an AI model.

    This function takes a potentially malformed JSON string and attempts to fix
    and format it using an AI model. It uses the 'gemini-flash' model to process
    the input and return a corrected JSON string.

    Args:
        json_string (str): The JSON string to fix and format. This can be a malformed
            or incorrectly formatted JSON string.

    Returns:
        str: The fixed and formatted JSON string. If the input is valid JSON,
            it will be returned in a standardized format. If the input is invalid,
            the function attempts to correct common errors and return a valid JSON string.

    Raises:
        Any exceptions raised by the underlying get_completion_api function.

    Example:
        >>> malformed_json = "{'key': 'value', 'nested': {'a':1, 'b': 2,}}"
        >>> fixed_json = fix_json(malformed_json)
        >>> print(fixed_json)
        '{"key": "value", "nested": {"a": 1, "b": 2}}'
    """
    prompt = f"You are a JSON formatter, fixing any issues with JSON formats. Review the following JSON: {json_string}. Return a fixed JSON formatted string but do not lead with ```json\n, without making changes to the content."
    return get_completion_api(prompt, "gemini-flash", "system", prompt)

def template_api_json(model: str, render_data: Dict, system_message: str, persona: str) -> Dict:
    """
    Get the completion response from the API using the specified model and return it as a JSON object.

    This function sends a request to an AI model API, using a templated system message
    and specified persona. It then processes the response to ensure it's in valid JSON format.

    Args:
        model (str): The name of the AI model to use for the API call (e.g., "gpt-4", "claude-3.5").
        render_data (Dict): A dictionary containing data to render the template. 
            For example: {"name": "John", "age": 30}.
        system_message (str): A Jinja2 template string to be used as the system message.
            This will be rendered with the render_data.
        persona (str): A string describing the persona or role the AI should adopt for this response.

    Returns:
        Dict: The API response parsed as a Python dictionary. The structure of this dictionary
        will depend on the specific response from the AI model.

    Raises:
        json.JSONDecodeError: If the API response cannot be parsed as valid JSON.
        Any exceptions raised by the underlying get_completion_api or json.loads functions.

    Example:
        >>> model = "gpt-4"
        >>> render_data = {"user_name": "Alice", "task": "summarize"}
        >>> system_message = "You are an AI assistant helping {{user_name}} to {{task}} a document."
        >>> persona = "helpful assistant"
        >>> response = template_api_json(model, render_data, system_message, persona)
        >>> print(response)
        {'summary': 'This is a summary of the document...', 'key_points': ['Point 1', 'Point 2']}
    """
    xtemplate = Template(system_message)
    prompt = xtemplate.render(render_data)
    response = get_completion_api(prompt, model, "system", persona)
    response = response.strip("```json\n").strip("```").strip()
    response = json.loads(response)
    return response

def template_api(model: str, render_data: Dict, system_message: str, persona: str) -> str:
    """
    Get the completion response from the API using the specified model.

    This function is similar to template_api_json, but returns the raw string response
    from the AI model instead of attempting to parse it as JSON.

    Args:
        model (str): The name of the AI model to use for the API call (e.g., "gpt-4", "claude-3.5").
        render_data (Dict): A dictionary containing data to render the template. 
            For example: {"name": "John", "age": 30}.
        system_message (str): A Jinja2 template string to be used as the system message.
            This will be rendered with the render_data.
        persona (str): A string describing the persona or role the AI should adopt for this response.

    Returns:
        str: The raw API response as a string. This could be in any format, depending on
        the AI model's output (e.g., plain text, markdown, or even JSON as a string).

    Raises:
        Any exceptions raised by the underlying get_completion_api function.

    Example:
        >>> model = "gpt-4"
        >>> render_data = {"topic": "artificial intelligence"}
        >>> system_message = "Explain {{topic}} in simple terms."
        >>> persona = "friendly teacher"
        >>> response = template_api(model, render_data, system_message, persona)
        >>> print(response)
        "Artificial Intelligence, or AI, is like teaching computers to think and learn..."
    """
    xtemplate = Template(system_message)
    prompt = xtemplate.render(render_data)
    response = get_completion_api(prompt, model, "system", persona)
    return response

def initialize_client() -> OpenAI:
    """
    Initialize the OpenAI client with the API key retrieved from 1Password.

    This function retrieves the OpenAI API key from 1Password using the get_api function,
    then initializes and returns an OpenAI client instance.

    Returns:
        OpenAI: An initialized OpenAI client instance ready for making API calls.

    Raises:
        Exception: If there's an error retrieving the API key or initializing the client.
            This could be due to issues with 1Password access or invalid API keys.

    Example:
        >>> client = initialize_client()
        >>> # Now you can use the client to make OpenAI API calls
        >>> response = client.completions.create(model="text-davinci-002", prompt="Hello, AI!")
    """
    api_key = get_api("OPEN-AI", "Mamba")
    return OpenAI(api_key=api_key)

def create_thread(client: OpenAI):
    """
    Create a new thread using the OpenAI client.

    Args:
        client (OpenAI): An initialized OpenAI client.

    Returns:
        Thread: A new thread object.
    """
    return client.beta.threads.create()

def send_message(client: OpenAI, thread_id: str, reference: str):
    """
    Send a message to the specified thread.

    Args:
        client (OpenAI): An initialized OpenAI client.
        thread_id (str): The ID of the thread to send the message to.
        reference (str): The content of the message to send.

    Returns:
        Message: The created message object.
    """
    return client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=reference,
    )

def run_assistant(client: OpenAI, thread_id: str, assistant_id: str):
    """
    Run the assistant for the specified thread.

    Args:
        client (OpenAI): An initialized OpenAI client.
        thread_id (str): The ID of the thread to run the assistant on.
        assistant_id (str): The ID of the assistant to run.

    Returns:
        Run: The created run object.
    """
    return client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=assistant_id
    )

def wait_for_run_completion(client: OpenAI, thread_id: str, run_id: str):
    """
    Wait for the assistant run to complete.

    Args:
        client (OpenAI): An initialized OpenAI client.
        thread_id (str): The ID of the thread.
        run_id (str): The ID of the run to wait for.

    Returns:
        Run: The completed run object.
    """
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    while run.status in ["queued", "in_progress"]:
        sleep(0.5)  # Add a delay to avoid rapid polling
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    return run

def get_assistant_responses(client: OpenAI, thread_id: str) -> List[str]:
    """
    Retrieve and clean the assistant's responses from the thread.

    Args:
        client (OpenAI): An initialized OpenAI client.
        thread_id (str): The ID of the thread to retrieve responses from.

    Returns:
        List[str]: A list of assistant responses.
    """
    message_list = client.beta.threads.messages.list(thread_id=thread_id)
    assistant_responses = [
        message.content[0].text.value
        for message in message_list.data
        if message.role == "assistant"
    ]
    return assistant_responses

def get_assistant(reference: str, assistant_id: str) -> List[str]:
    """
    Get the assistant's response for the given reference and assistant ID.

    Args:
        reference (str): The reference message to send to the assistant.
        assistant_id (str): The ID of the assistant to use.

    Returns:
        List[str]: A list of assistant responses.
    """
    client = initialize_client()
    thread = create_thread(client)
    send_message(client, thread.id, reference)
    run = run_assistant(client, thread.id, assistant_id)
    wait_for_run_completion(client, thread.id, run.id)
    responses = get_assistant_responses(client, thread.id)
    return responses

def get_completion_api(
    prompt: str,
    model_name: str,
    mode: str = "simple",
    system_message: Optional[str] = None,
) -> Optional[str]:
    """
    Get the completion response from the API using the specified model.

    Args:
        prompt (str): The prompt to send to the API.
        model_name (str): The name of the model to use for completion.
        mode (str, optional): The mode of message sending (simple or system). Defaults to "simple".
        system_message (Optional[str], optional): The system message to send if in system mode. Defaults to None.

    Returns:
        Optional[str]: The completion response content, or None if an error occurs.

    Raises:
        ValueError: If an unsupported model or mode is specified.
    """
    try:
        # Select the model and set the appropriate API key
        match model_name:
            case "gpt-4o-mini" | "gpt-4" | "gpt-4o":
                os.environ["OPENAI_API_KEY"] = get_api("OPEN-AI", "Mamba")
                selected_model = model_name
            case "claude-3.5":
                os.environ["ANTHROPIC_API_KEY"] = get_api("Anthropic", "CLI-Maya")
                selected_model = "claude-3-5-sonnet-20240620"
            case "gemini-flash":
                os.environ["GEMINI_API_KEY"] = get_api("Gemini", "CLI-Maya")
                selected_model = "gemini/gemini-1.5-flash"
            case "llama-3-70b":
                os.environ["TOGETHERAI_API_KEY"] = get_api("TogetherAI", "API")
                selected_model = "together_ai/meta-llama/Llama-3-70b-chat-hf"
            case "llama-3.1-large":
                os.environ["TOGETHERAI_API_KEY"] = get_api("TogetherAI", "API")
                selected_model = "together_ai/meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo"
            case "groq-llama":
                os.environ["GROQ_API_KEY"] = get_api("Groq", "Promptsys")
                selected_model = "groq/llama3-70b-8192"
            case "groq-fast":
                os.environ["GROQ_API_KEY"] = get_api("Groq", "Promptsys")
                selected_model = "groq/llama3-8b-8192"
            case "mistral-large":
                os.environ["MISTRAL_API_KEY"] = get_api("MistralAI", "API")
                selected_model = "mistral/mistral-large-latest"
            case _:
                raise ValueError(f"Unsupported model: {model_name}")

        # Select message type
        match mode:
            case "simple":
                print("Message Simple")
                messages = [{"content": prompt, "role": "user"}]
            case "system":
                if system_message is None:
                    raise ValueError("system_message must be provided in system mode")
                messages = [
                    {"content": system_message, "role": "system"},
                    {"content": prompt, "role": "user"},
                ]
            case _:
                raise ValueError(f"Unsupported mode: {mode}")

        # Make the API call
        response = completion(
            model=selected_model,
            messages=messages,
            temperature=0.1,
        )

        # Extract and return the response content
        return response["choices"][0]["message"]["content"]

    except KeyError as ke:
        print(f"Key error occurred: {ke}")
    except ValueError as ve:
        print(f"Value error occurred: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None

def fix_json(json_string):
    prompt = f"You are a JSON formatter, fixing any issues with JSON formats. Review the following JSON: {json_string}. Return a fixed JSON formatted string but do not lead with ```json\n, without making changes to the content."
    return get_completion_api(prompt, "gemini-flash", "system", prompt)
