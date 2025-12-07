import uuid
from typing import Optional

import click
import requests

from cli.enums.token_type import TokenType
from cli.settings import get_settings


def register_token(
    token_type: TokenType, message: Optional[str] = None, cid: Optional[str] = None
):
    click.echo(f"Registering token in server...")
    try:
        register_payload = {
            "token_type": token_type,
            "message": message,
            "custom_id": cid,
        }

        response = requests.post(
            f"{get_settings().API_BASE_URL}/api/tokens/register",
            json=register_payload,
            timeout=10,
        )
        response.raise_for_status()
        click.echo(f"🗃️ Token registered successfully")

        return response.json()["token_id"]

    except requests.exceptions.HTTPError as e:
        status = response.status_code
        error_body = response.text

        raise click.ClickException(
            f"❌ Failed to register token. (HTTP Status Code {status}): {error_body}"
        ) from e

    except requests.exceptions.RequestException as e:
        raise click.ClickException(f"❌ Failed to register token: {e}") from e
