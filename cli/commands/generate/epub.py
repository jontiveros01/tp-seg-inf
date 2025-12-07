import click

from cli.client.api import register_token
from cli.enums.token_type import TokenType
from cli.token_strategies.epub import epub
import uuid

@click.command()

def generate_epub():
    click.echo("Generating EPUB honeytoken...")

    token_uuid = uuid.uuid4()

    if epub(token_uuid):
        register_token(TokenType.EPUB, token_uuid)
        click.echo(f"EPUB honeytoken generated with UUID: {token_uuid}")
