import click

from cli.client.api import register_token
from cli.enums.token_type import TokenType
from cli.token_strategies.docx import docx
import uuid

@click.command()
@click.option(
    "--strategy",
    "-s",
    type=click.Choice(["image", "template"]),
    required=True,
    help="Honeytoken injection strategy",
)
@click.pass_context
def generate_docx(ctx, strategy):
    click.echo("Generating DOCX honeytoken...")

    cid = ctx.obj.get("cid")
    token_uuid = register_token(TokenType.DOCX, cid)

    docx(token_uuid, strategy)
        
    click.echo(f"DOCX honeytoken generated with UUID: {token_uuid}")
