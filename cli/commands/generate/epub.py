import click

from cli.client.api import register_token, get_new_id
from cli.enums.token_type import TokenType
from cli.token_strategies.epub import epub
import uuid

@click.command()
@click.pass_context
def generate_epub(ctx):
    click.echo("Generating EPUB honeytoken...")

    cid = ctx.obj.get("cid")
    token_id = get_new_id() if cid is None else cid

    if epub(token_id):
        if register_token(TokenType.EPUB, token_id, cid):
            click.echo(f"EPUB honeytoken generated with ID: {token_id}")
        else:
            click.echo(f"Failed to register honeytoken")