import click
import requests
import json
from dotenv import load_dotenv
import os
from usl.utils.db import get_config

# Load environment variables from .env file
load_dotenv()

# Get the base URL from environment variables
BASE_URL = os.getenv('BASE_URL', 'https://api.minakilabs.dev')

@click.command(name='feedback')
@click.option('-n', '--name', prompt='Your name', help='The name of the feedback submitter.')
@click.option('-e', '--email', prompt='Your email', help='The email of the feedback submitter.')
@click.option('-f', '--feedback', prompt='Your feedback', help='The feedback to submit.')
def feedback(name, email, feedback):
    """Submit feedback to the MinakiLabs Spider Project."""
    url = f"{BASE_URL}/freemium/submit-feedback/"
    freemium_api_key = get_config('freemium_api_key')
    if not freemium_api_key:
        click.echo("Freemium API key not found. Please set it using the `login_freemium` command.")
        return

    headers = {
        "Content-Type": "application/json",
        "apikey": freemium_api_key
    }
    data = {
        "name": name,
        "email": email,
        "feedback": feedback
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        click.echo("Thank you for your feedback!")
    except requests.RequestException as e:
        click.echo(f"Failed to submit feedback: {e}", err=True)

if __name__ == "__main__":
    feedback()
