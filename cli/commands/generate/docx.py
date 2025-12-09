import click

from cli.client.api import register_token, get_new_id
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
    token_uuid = get_new_id()

    if docx(token_uuid, strategy):
        if register_token(TokenType.DOCX, token_uuid, cid):
            click.echo(f"DOCX honeytoken registered with UUID: {token_uuid}")
        else:
            click.echo(f"Failed to register honeytoken")
