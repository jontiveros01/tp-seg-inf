import click

from cli.client.api import register_token
from cli.enums.token_type import TokenType
from cli.token_strategies.html import html


@click.command()
@click.option(
    "--strategy",
    "-s",
    type=click.Choice(["fetch-script", "css-bg", "remote-css"]),
    required=True,
    help="Honeytoken injection strategy",
)
def generate_html(strategy: str):
    """Generate an HTML honeytoken"""

    click.echo("🔄 Generating HTML honeytoken...")

    token_uuid = register_token(TokenType.HTML)

    html(token_uuid, strategy)

    click.echo(f"🍯 HTML honeytoken generated with UUID: {token_uuid}")
