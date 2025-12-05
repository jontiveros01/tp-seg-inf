import click

from cli.commands.generate.html import generate_html
from cli.commands.generate.pdf import generate_pdf
from cli.commands.generate.qr import generate_qr


@click.group()
def generate():
    """Generate different types of honeytokens"""
    pass


generate.add_command(generate_qr, name="qr")
generate.add_command(generate_pdf, name="pdf")
generate.add_command(generate_html, name="html")
