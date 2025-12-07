import click

from cli.client.api import register_token
from cli.enums.token_type import TokenType
from cli.token_strategies.epub import epub
import uuid

@click.command()
@click.pass_context
def generate_epub(ctx):
    click.echo("Generating EPUB honeytoken...")

    cid = ctx.obj.get("cid")
    token_uuid = register_token(TokenType.EPUB, cid)
    
    epub(token_uuid)
        
    click.echo(f"EPUB honeytoken generated with UUID: {token_uuid}")
