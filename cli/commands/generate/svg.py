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
    token_uuid = get_new_id()

    if svg(token_uuid):
        if register_token(TokenType.SVG, token_uuid, cid):
            click.echo(f"SVG honeytoken generated with UUID: {token_uuid}")
        else:
            click.echo(f"Failed to register honeytoken")