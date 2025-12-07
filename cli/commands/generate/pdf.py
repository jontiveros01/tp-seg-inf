import click

from cli.client.api import register_token
from cli.enums.token_type import TokenType
from cli.token_strategies.pdf import pdf


@click.command()
@click.pass_context
def generate_pdf(ctx):
    """Generate a PDF honeytoken"""

    click.echo("🔄 Generating PDF honeytoken...")

    cid = ctx.obj.get("cid")
    token_uuid = register_token(TokenType.PDF, cid=cid)

    pdf(token_uuid)

    click.echo(f"🍯 PDF honeytoken generated with UUID: {token_uuid}")
