"""
Honey Token CLI - Generation System
"""

import uuid

import click
import requests
from enums.token_type import TokenType
from settings import get_settings
from token_strategies import qr, pdf


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
    required=True,
    help="Message or payload to embed (QR) or describe (SVG)",
)
@click.option(
    "--output", "-o", required=True, help="Output file path (PNG for qr, .svg for svg)."
)
def generate(token_type: TokenType, message: str, output: str):
    """Generate a honeytoken of specified parameters"""

    token_uuid = uuid.uuid4()
    click.echo(f"🔄 Generating honeytoken {token_uuid} as {token_type}...")

    _register_token(token_type, token_uuid, message)

    match token_type:
        case TokenType.QR:
            qr(message, output, token_uuid)
        case TokenType.PDF:
            pdf(token_uuid)

    click.echo(
        f"🍯 Honeytoken {token_uuid} as {token_type} generated successfully in {output}"
    )


def _register_token(token_type: TokenType, token_uuid: uuid.UUID, message: str):
    click.echo(f"📥 Registering token {token_uuid} in server...")
    try:
        register_payload = {
            "token_uuid": str(token_uuid),
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

    except requests.exceptions.RequestException as e:
        raise click.ClickException(
            f"❌ Failed to register token {token_uuid}: {e}"
        ) from e


if __name__ == "__main__":
    generate()
