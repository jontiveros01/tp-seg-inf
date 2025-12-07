import click

from cli.client.api import register_token
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
    token_uuid = register_token(TokenType.PDF, cid=cid)

    pdf(token_uuid, strategy)

    click.echo(f"PDF honeytoken generated with UUID: {token_uuid}")
