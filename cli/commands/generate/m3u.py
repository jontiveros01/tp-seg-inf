import click

from cli.client.api import register_token, get_new_id
from cli.enums.token_type import TokenType
from cli.token_strategies.m3u import m3u


@click.command()
@click.pass_context
def generate_m3u(ctx):
    click.echo("Generating M3U honeytoken...")

    cid = ctx.obj.get("cid")
    token_uuid = get_new_id()

    if m3u(token_uuid):
        if register_token(TokenType.M3U, token_uuid, cid=cid):
            click.echo(f"M3U honeytoken generated with UUID: {token_uuid}")
        else:
            click.echo(f"Failed to register honeytoken")
    else:
        click.echo(f"Failed to generate M3U honeytoken")