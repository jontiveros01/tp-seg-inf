import uuid
from typing import Optional

import click
import requests

from cli.enums.token_type import TokenType
from cli.settings import get_settings


def register_token(
    token_type: TokenType, token_uuid: str, message: Optional[str] = None, cid: Optional[str] = None
):
    click.echo(f"Registering token in server...")
    try:
        register_payload = {
            "token_type": token_type,
            "token_uuid": token_uuid,
            "message": message,
            "custom_id": cid,
        }

        response = requests.post(
            url=f"{get_settings().API_BASE_URL}/api/tokens/register",
            json=register_payload,
            timeout=10,
        )
        response.raise_for_status()
        click.echo(f"Token registered successfully")

        return response.json()["status"] == "ok"

    except requests.exceptions.HTTPError as e:
        status = response.status_code
        error_body = response.text

        raise click.ClickException(
            f"Failed to register token. (HTTP Status Code {status}): {error_body}"
        ) from e

    except requests.exceptions.RequestException as e:
        raise click.ClickException(f"Failed to register token: {e}") from e

def get_new_id():
    try:
        response = requests.get(f"{get_settings().API_BASE_URL}/api/tokens/new_uuid", timeout=10)
        response.raise_for_status()
        return response.json()["uuid"]
    except requests.exceptions.HTTPError as e:
        status = response.status_code
        error_body = response.text

        raise click.ClickException(
            f"Failed to obtain UUID. (HTTP Status Code {status}): {error_body}"
        ) from e

    except requests.exceptions.RequestException as e:
        raise click.ClickException(f"Failed to obtain UUID: {e}") from e