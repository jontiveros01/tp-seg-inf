import click

from cli.client.api import register_token
from cli.enums.token_type import TokenType
from cli.token_strategies.docx import docx
import uuid

@click.command()
@click.option(
    "--strategy",
    "-s",
    type=click.Choice(["image", "template"]),
    required=True,
    help="Honeytoken injection strategy",
)
def generate_docx(strategy):
    click.echo("Generating DOCX honeytoken...")

    token_uuid = uuid.uuid4()

    if docx(token_uuid, strategy):
        register_token(TokenType.DOCX, token_uuid)
        click.echo(f"DOCX honeytoken generated with UUID: {token_uuid}")
