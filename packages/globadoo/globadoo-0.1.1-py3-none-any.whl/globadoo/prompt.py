from typing import Type

from globadoo.models import CountryResponse


def create_prompt(model: Type[CountryResponse], city: str) -> str:
    question = f"Can you find the name of the country with the city {city}"
    return f"""
You are a Country Finder Agent (CFA).
It is your job to accomplish the following task: {question}
All your answers must be in json format and follow the following schema json schema:
{model.schema()}

If unsure about the city, then country is unknown.
Let's begin to answer the question: {question}
Do not write anything else than json!
"""
