import click

from cli.client.api import register_token, get_new_id
from cli.enums.token_type import TokenType
from cli.token_strategies.html import html
import uuid

@click.command()
@click.option(
    "--strategy",
    "-s",
    type=click.Choice(["fetch-script", "css-bg", "remote-css"]),
    required=True,
    help="Honeytoken injection strategy",
)
@click.pass_context
def generate_html(ctx, strategy: str):

    cid = ctx.obj.get("cid")
    token_uuid = get_new_id()

    if html(token_uuid, strategy):
        if register_token(TokenType.HTML, token_uuid, cid=cid):
            click.echo(f"HTML honeytoken generated with UUID: {token_uuid}")
        else:
            click.echo(f"Failed to register honeytoken")