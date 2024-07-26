from rich import print

from globadoo.chat import chat
from globadoo.client import get_openai_client
from globadoo.models import CountryResponse, LLMConfig
from globadoo.prompt import create_prompt


def find_country(city: str, model: str = "gpt-4o-mini"):
    """Find the country of a city using the OpenAI Language Model."""
    # Create the LLM configuration. We are using the gpt-4o-mini model,
    # because it is the cheapest model that can handle the prompt.
    llm_config = LLMConfig(
        model=model,
        max_tokens=100,
    )

    # Create the prompt with question about which country a city is in
    prompt = create_prompt(CountryResponse, city)

    client = get_openai_client()

    # Send the prompt to the LLM model
    message = chat(client=client, config=llm_config, prompt=prompt)

    if not message.choices:
        raise ValueError("No response from the model. Please try again...")

    # Validate the response from the model
    cr = CountryResponse.model_validate_json(message.choices[0].message.content)

    # Print the response
    print(cr.json())
