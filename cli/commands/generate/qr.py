import click

from cli.client.api import register_token, get_new_id
from cli.enums.token_type import TokenType
from cli.token_strategies.qr import qr
import uuid

@click.command()
@click.option("--message", "-m", help="Message or payload to embed (QR)")
@click.pass_context
def generate_qr(ctx, message: str):
    click.echo("Generating QR honeytoken...")

    cid = ctx.obj.get("cid")
    token_uuid = get_new_id()

    if qr(token_uuid):
        if register_token(TokenType.QR, token_uuid, message, cid):
            click.echo(f"QR honeytoken generated with UUID: {token_uuid}")
        else:
            click.echo(f"Failed to register honeytoken")