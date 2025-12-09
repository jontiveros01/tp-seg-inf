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
    token_uuid = get_new_id()

    if pdf(token_uuid, strategy):
        if register_token(TokenType.PDF, token_uuid, cid=cid):
            click.echo(f"PDF honeytoken generated with UUID: {token_uuid}")
        else:
            click.echo(f"Failed to register honeytoken")