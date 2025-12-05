import click

from cli.commands.generate import generate


@click.group()
def cli():
    """Honeytoken CLI"""
    pass


cli.add_command(generate)


if __name__ == "__main__":
    cli()
