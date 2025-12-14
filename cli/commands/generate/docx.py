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
    token_id = get_new_id() if cid is None else cid

    if docx(token_id, strategy):
        if register_token(TokenType.DOCX, token_id, cid):
            click.echo(f"DOCX honeytoken registered with ID: {token_id}")
        else:
            click.echo(f"Failed to register honeytoken")
