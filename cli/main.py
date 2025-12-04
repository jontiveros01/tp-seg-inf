"""
Honey Token CLI - Generation System
"""

import uuid
from typing import Optional

import click
import requests
from enums.token_type import TokenType
from settings import get_settings
from token_strategies.pdf import pdf
from token_strategies.qr import qr


@click.command()
@click.option(
    "--type",
    "-t",
    "token_type",
    required=True,
    type=click.Choice([t.value for t in TokenType]),
    help="Token type to generate",
)
@click.option(
    "--message",
    "-m",
    required=False,
    default=None,
    help="Message or payload to embed (QR)",
)
def generate(token_type: TokenType, message: Optional[str]):
    """Generate a honeytoken of specified parameters"""

    click.echo(f"🔄 Generating honeytoken for type {token_type}")

    token_uuid = _register_token(token_type, message)

    match token_type:
        case TokenType.QR:
            qr(token_uuid)
        case TokenType.PDF:
            pdf(token_uuid)

    click.echo(
        f"🍯 Honeytoken for type {token_type} generated successfully with UUID: {token_uuid}"
    )


def _register_token(token_type: TokenType, message: Optional[str]):
    click.echo(f"📥 Registering token in server...")
    try:
        register_payload = {
            "token_type": token_type,
            "message": message,
        }

        response = requests.post(
            f"{get_settings().API_BASE_URL}/api/tokens/register",
            json=register_payload,
            timeout=10,
        )
        response.raise_for_status()
        click.echo(f"🗃️ Token registered successfully")

        return response.json()["token_uuid"]

    except requests.exceptions.RequestException as e:
        raise click.ClickException(f"❌ Failed to register token: {e}") from e


if __name__ == "__main__":
    generate()
