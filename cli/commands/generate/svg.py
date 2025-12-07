import click

from cli.client.api import register_token
from cli.enums.token_type import TokenType
from cli.token_strategies.svg import svg
import uuid

@click.command()
@click.pass_context
def generate_svg(ctx):
    click.echo("Generating SVG honeytoken...")

    cid = ctx.obj.get("cid")
    token_uuid = register_token(TokenType.SVG, cid)

    svg(token_uuid)

    click.echo(f"SVG honeytoken generated with UUID: {token_uuid}")
