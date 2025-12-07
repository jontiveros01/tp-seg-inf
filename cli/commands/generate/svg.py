import click

from cli.client.api import register_token
from cli.enums.token_type import TokenType
from cli.token_strategies.svg import svg
import uuid

@click.command()
def generate_svg():
    click.echo("Generating SVG honeytoken...")

    token_uuid = uuid.uuid4()

    if svg(token_uuid):
        register_token(TokenType.SVG, token_uuid)
        click.echo(f"SVG honeytoken generated with UUID: {token_uuid}")
