import click

from cli.client.api import register_token
from cli.enums.token_type import TokenType
from cli.token_strategies.pdf import pdf


@click.command()
def generate_pdf():
    """Generate a PDF honeytoken"""

    click.echo("🔄 Generating PDF honeytoken...")

    token_uuid = register_token(TokenType.PDF)

    pdf(token_uuid)

    click.echo(f"🍯 PDF honeytoken generated with UUID: {token_uuid}")
