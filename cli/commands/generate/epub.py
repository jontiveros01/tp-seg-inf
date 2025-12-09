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
    token_uuid = get_new_id()
    
    if epub(token_uuid):
        if register_token(TokenType.EPUB, token_uuid, cid):
            click.echo(f"EPUB honeytoken generated with UUID: {token_uuid}")
        else:
            click.echo(f"Failed to register honeytoken")