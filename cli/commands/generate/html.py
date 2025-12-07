import click

from cli.client.api import register_token
from cli.enums.token_type import TokenType
from cli.token_strategies.html import html
import uuid

@click.command()
@click.option(
    "--strategy",
    "-s",
    type=click.Choice(["fetch-script", "css-bg", "remote-css"]),
    required=True,
    help="Honeytoken injection strategy",
)
def generate_html(strategy: str):
    click.echo("Generating HTML honeytoken...")

    token_uuid = uuid.uuid4()

    if html(token_uuid, strategy):
        register_token(TokenType.HTML, token_uuid)
        click.echo(f"HTML honeytoken generated with UUID: {token_uuid}")
