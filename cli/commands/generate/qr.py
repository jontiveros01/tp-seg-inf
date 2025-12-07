import click

from cli.client.api import register_token
from cli.enums.token_type import TokenType
from cli.token_strategies.qr import qr
import uuid

@click.command()
@click.option("--message", "-m", help="Message or payload to embed (QR)")
def generate_qr(message):
    click.echo("Generating QR honeytoken...")

    token_uuid = uuid.uuid4()

    if qr(token_uuid):
        register_token(TokenType.QR, token_uuid, message)
        click.echo(f"QR honeytoken generated with UUID: {token_uuid}")
