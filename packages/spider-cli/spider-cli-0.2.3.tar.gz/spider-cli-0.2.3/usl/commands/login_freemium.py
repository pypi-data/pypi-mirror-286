import click
import webbrowser
import os
from dotenv import load_dotenv
from usl.utils.db import set_config

# Load environment variables from .env file
load_dotenv()

# This needs to be .com not .dev by default
# Get the SPIDER_URL from environment variables
SPIDER_URL = os.getenv("SPIDER_URL", "https://spider.minakilabs.com")

LOGIN_URL = f"{SPIDER_URL}/login"

@click.command()
def login_freemium():
    """
    Guide the user through the login process for the freemium API key.
    """
    click.echo(f"Please log in at the following URL: {LOGIN_URL}")
    webbrowser.open(LOGIN_URL)
    api_key = click.prompt("Enter your Freemium API key")

    # Save the freemium API key to the database
    set_config("freemium_api_key", api_key)

    click.echo("Freemium API key saved successfully.")

if __name__ == "__main__":
    login_freemium()
