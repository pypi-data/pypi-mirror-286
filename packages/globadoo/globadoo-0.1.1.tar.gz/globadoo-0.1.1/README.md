# Globadoo

Globadoo is a Python library for finding the country of a given city using OpenAI chat model.

## Installation

To install Globadoo, use the following command:

```
pip install globadoo
```

## Usage

Here's a basic example of how to use Globadoo:

```
pipx install globadoo
export OPENAI_API_KEY="your-api-key"
globadoo "New York"
```
This returns
    
    {"city":"New York","country":"United States","country_code":"US"}

## API Reference

The main function of Globadoo is `find_country(city, llm_config)`, which takes a city name and an LLMConfig model as arguments and returns the country of the city.

## Tests

To run the tests for Globadoo, use the following command:

```
pytest tests
```

## Contributing

Contributions to Globadoo are welcome. Please submit a pull request with your changes.

## License

Globadoo is licensed under the MIT License.

## Contact

For any questions or concerns, please open an issue on the GitHub repository.