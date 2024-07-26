import typer
from dotenv import load_dotenv

from globadoo.find_country import find_country


def main():
    """CLI entrypoint for finding the country of a city using the OpenAI Language Model."""
    load_dotenv()
    typer.run(find_country)


if __name__ == "__main__":
    main()
