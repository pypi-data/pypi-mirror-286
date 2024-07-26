import openai
from openai.types.chat import ChatCompletion

from globadoo.models import LLMConfig


def chat(client: openai.Client, config: LLMConfig, prompt: str) -> ChatCompletion:
    return client.chat.completions.create(
        model=config.model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=config.max_tokens,
        top_p=config.top_p,
        n=config.n,
        presence_penalty=config.presence_penalty,
        frequency_penalty=config.frequency_penalty,
        response_format=config.response_format,
        seed=config.seed,
    )
