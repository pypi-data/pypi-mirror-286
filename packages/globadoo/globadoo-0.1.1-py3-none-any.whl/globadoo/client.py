import os

from openai import OpenAI


def get_openai_client() -> OpenAI:
    """Get an OpenAI client with the API key from the environment."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set OPENAI_API_KEY environment variable.")
    return OpenAI(api_key=api_key)
