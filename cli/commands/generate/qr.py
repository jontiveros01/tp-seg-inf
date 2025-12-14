import click

from cli.client.api import register_token, get_new_id
from cli.enums.token_type import TokenType
from cli.token_strategies.qr import qr
import uuid

@click.command()
@click.option("--message", "-m", help="Message or payload to embed (QR)")
@click.option("--redirect-url", "-r", help="URL to redirect when the token is accessed")
@click.pass_context
def generate_qr(ctx, message: str, redirect_url: str):
    click.echo("Generating QR honeytoken...")

    cid = ctx.obj.get("cid")
    token_id = get_new_id() if cid is None else cid

    if qr(token_id):
        if register_token(TokenType.QR, token_id, message, cid, redirect_url):
            click.echo(f"QR honeytoken generated with ID: {token_id}")
        else:
            click.echo(f"Failed to register honeytoken")