"""
Honey Token CLI - Generation System
"""

import uuid
from pathlib import Path

import click
import qrcode
import requests

API_BASE_URL = "http://localhost:8080"


@click.command()
@click.option("--type", "-t", "token_type", type=click.Choice(["qr"]), default="qr", help="Type of token to generate")
@click.option("--message", "-m", required=True, help="Message or payload to embed (QR) or describe (SVG)")
@click.option("--output", "-o", required=True, default=None, help="Output file path (PNG for qr, .svg for svg).")
def generate(token_type, message, output):
    """Generate a honeytoken of specified type with a personalized message"""
    if token_type == "qr":
        qr(message, output)
    elif token_type == "other":
        #generate_other_token(message, output)
        return
    else:
        click.echo(f"✗ Unsupported token type: {token_type}", err=True)


def qr(message, output):
    """Generate a QR honeytoken with a personalized message"""

    click.echo("🍯 Generating Honey Token QR...")

    token_uuid = str(uuid.uuid4())

    click.echo(f"   UUID: {token_uuid}")

    try:
        register_payload = {
            "token_uuid": token_uuid,
            "token_type": "qr",
            "message": message,
        }

        response = requests.post(
            f"{API_BASE_URL}/api/tokens/register", json=register_payload, timeout=10
        )
        response.raise_for_status()
        click.echo(f"✓ Token Generated")

    except requests.exceptions.RequestException as e:
        click.echo(f"✗ Error In registering token: {e}", err=True)

    alert_url = f"{API_BASE_URL}/api/tokens/alert/{token_uuid}"

    qr_obj = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr_obj.add_data(alert_url)
    qr_obj.make(fit=True)

    img = qr_obj.make_image(fill_color="black", back_color="white")

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)

    click.echo(f"✓ QR generated: {output_path}")



if __name__ == "__main__":
    generate()
