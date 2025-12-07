import click

from cli.commands.generate.html import generate_html
from cli.commands.generate.pdf import generate_pdf
from cli.commands.generate.qr import generate_qr
from cli.commands.generate.svg import generate_svg
from cli.commands.generate.epub import generate_epub
from cli.commands.generate.docx import generate_docx


@click.group()
def generate():
    """Generate different types of honeytokens"""
    pass


generate.add_command(generate_qr, name="qr")
generate.add_command(generate_pdf, name="pdf")
generate.add_command(generate_html, name="html")
generate.add_command(generate_svg, name="svg")
generate.add_command(generate_epub, name="epub")
generate.add_command(generate_docx, name="docx")
