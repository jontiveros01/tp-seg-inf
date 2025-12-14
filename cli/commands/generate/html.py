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
    token_id = get_new_id() if cid is None else cid

    if html(token_id, strategy):
        if register_token(TokenType.HTML, token_id, cid=cid, redirect_url=None):
            click.echo(f"HTML honeytoken generated with ID: {token_id}")
        else:
            click.echo(f"Failed to register honeytoken")