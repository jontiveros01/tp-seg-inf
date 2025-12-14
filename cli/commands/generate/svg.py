import click

from cli.client.api import register_token, get_new_id
from cli.enums.token_type import TokenType
from cli.token_strategies.svg import svg
import uuid

@click.command()
@click.pass_context
def generate_svg(ctx):
    click.echo("Generating SVG honeytoken...")

    cid = ctx.obj.get("cid")
    token_id = get_new_id() if cid is None else cid

    if svg(token_id):
        if register_token(TokenType.SVG, token_id, cid, redirect_url=None):
            click.echo(f"SVG honeytoken generated with ID: {token_id}")
        else:
            click.echo(f"Failed to register honeytoken")