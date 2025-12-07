import click

from cli.client.api import register_token
from cli.enums.token_type import TokenType
from cli.token_strategies.pdf import pdf
import uuid

@click.command()
@click.option(
    "--strategy",
    "-s",
    type=click.Choice(["link", "openaction"]),
    required=True,
    help="Honeytoken injection strategy",
)
def generate_pdf(strategy):
    click.echo("Generating PDF honeytoken...")

    token_uuid = uuid.uuid4()

    if pdf(token_uuid, strategy):
        register_token(TokenType.PDF, token_uuid)
        click.echo(f"PDF honeytoken generated with UUID: {token_uuid}")
