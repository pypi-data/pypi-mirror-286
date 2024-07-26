from openai import BaseModel


class CountryResponse(BaseModel):
    city: str
    country: str
    country_code: str


class LLMConfig(BaseModel):
    model: str
    max_tokens: int
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    response_format: dict = {"type": "json_object"}
    top_p: float = 0.01
    stop: int = 1
    n: int = 1
    tool_choice: str = "none"
    seed: int = 42
