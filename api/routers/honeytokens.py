"""
Router Honeytokens management
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/tokens", tags=["Honeytokens"])

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
TOKENS_FILE = DATA_DIR / "tokens.json"
ALERTS_FILE = DATA_DIR / "alerts.json"
DATA_DIR.mkdir(exist_ok=True)


def load_json(path):
    if path.exists():
        try:
            with open(path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {} if "tokens" in path.name else []
    return {} if "tokens" in path.name else []


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


class TokenRegister(BaseModel):
    token_uuid: str
    token_type: str
    message: str


@router.post("/register")
async def register_token(token: TokenRegister):
    """
    Register a new honeytoken in the system
    """
    tokens_db = load_json(TOKENS_FILE)

    if token.token_uuid in tokens_db:
        raise HTTPException(status_code=400, detail="Token ya existe")

    tokens_db[token.token_uuid] = {
        "token_uuid": token.token_uuid,
        "token_type": token.token_type,
        "registered_at": datetime.utcnow().isoformat(),
        "triggered": False,
        "message": token.message,
    }

    save_json(TOKENS_FILE, tokens_db)
    logger.info(
        f"🍯 Nuevo token registrado: {token.token_uuid} (tipo: {token.token_type})"
    )

    return {"status": "registered", "token_uuid": token.token_uuid}


@router.get("/alert/{token_uuid}")
async def alert_token_accessed(token_uuid: str, request: Request):
    """
    Endpoint triggered when someone access the honeytoken
    """

    tokens_db = load_json(TOKENS_FILE)
    alerts_db = load_json(ALERTS_FILE)

    client_ip = request.client.host
    if "x-forwarded-for" in request.headers:
        client_ip = request.headers["x-forwarded-for"].split(",")[0].strip()

    alert = {
        "token_uuid": token_uuid,
        "accessed_from_ip": client_ip,
        "accessed_at": datetime.utcnow().isoformat(),
        "user_agent": request.headers.get("user-agent", "unknown"),
        "referer": request.headers.get("referer", "none"),
        "accept_language": request.headers.get("accept-language", "unknown"),
    }

    alerts_db.append(alert)
    save_json(ALERTS_FILE, alerts_db)

    token_info = tokens_db.get(token_uuid)

    if token_info:
        tokens_db[token_uuid]["triggered"] = True
        tokens_db[token_uuid]["last_trigger"] = alert["accessed_at"]
        save_json(TOKENS_FILE, tokens_db)

    logger.warning("=" * 70)
    logger.warning("🚨 ¡ALERT! HONEY TOKEN ACTIVE 🚨")
    logger.warning("=" * 70)
    logger.warning(f"Token UUID:      {token_uuid}")
    logger.warning(f"IP Access:       {client_ip}")
    logger.warning(f"Timestamp:       {alert['accessed_at']}")
    logger.warning(f"User-Agent:      {alert['user_agent']}")
    if token_info:
        logger.warning(f"Token type:      {token_info['token_type']}")
        logger.warning(f"Message:         {token_info.get('message', 'N/A')}")
    else:
        logger.warning("⚠️  Token not found in database")
    logger.warning("=" * 70)

    return {
        "status": "ok",
        "message": (
            token_info.get("message", "Registered Access")
            if token_info
            else "Registered Access"
        ),
    }
