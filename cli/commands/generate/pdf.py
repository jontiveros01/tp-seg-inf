import click

from cli.client.api import register_token, get_new_id
from cli.enums.token_type import TokenType
from cli.token_strategies.pdf import pdf
import uuid

@click.command()
@click.option(
    "--strategy",
    "-s",
    type=click.Choice(["link", "openaction"]),
    required=True,
    help="Honeytoken injection strategy",
)
@click.pass_context
def generate_pdf(ctx, strategy):
    click.echo("Generating PDF honeytoken...")

    cid = ctx.obj.get("cid")
    token_id = get_new_id() if cid is None else cid

    if pdf(token_id, strategy):
        if register_token(TokenType.PDF, token_id, cid=cid):
            click.echo(f"PDF honeytoken generated with ID: {token_id}")
        else:
            click.echo(f"Failed to register honeytoken")