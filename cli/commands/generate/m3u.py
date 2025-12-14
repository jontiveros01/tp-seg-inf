import click

from cli.client.api import register_token, get_new_id
from cli.enums.token_type import TokenType
from cli.token_strategies.m3u import m3u


@click.command()
@click.option(
    "--format",
    "-f",
    type=click.Choice(["m3u", "m3u8", "both"]),
    default="both",
    help="Playlist format to generate (default: both)",
)
@click.pass_context
def generate_m3u(ctx, format):
    click.echo(f"Generating MP3 playlist honeytoken(s)...")

    cid = ctx.obj.get("cid")
    token_id = get_new_id() if cid is None else cid

    if m3u(token_id, format):
        if register_token(TokenType.M3U, token_id, cid=cid):
            click.echo(f"MP3 playlist honeytoken(s) registered with ID: {token_id}")
        else:
            click.echo(f"Failed to register honeytoken")
    else:
        click.echo(f"Failed to generate MP3 playlist honeytoken")