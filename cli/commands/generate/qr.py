import click

from cli.client.api import register_token
from cli.enums.token_type import TokenType
from cli.token_strategies.qr import qr
import uuid

@click.command()
@click.option("--message", "-m", help="Message or payload to embed (QR)")
@click.pass_context
def generate_qr(ctx, message: str):
    click.echo("Generating QR honeytoken...")

    cid = ctx.obj.get("cid")
    token_uuid = register_token(TokenType.QR, message, cid)

    qr(token_uuid)

    click.echo(f"QR honeytoken generated with UUID: {token_uuid}")
