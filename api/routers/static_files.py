"""
Router Static Files management
"""

import json
import logging
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional
from uuid import UUID
from resources import PDF_ICON_BYTES

from fastapi import APIRouter, Response
from settings import get_settings

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Static Files"])


@router.get("/api/static-files/honey-css/{token_id}")
async def honeytoken_css(token_id: str):
    alert_url = f"{get_settings().API_BASE_URL}/api/tokens/alert/{token_id}"

    css = f"""
body::before {{
    content: " ";
    position: absolute;
    width: 1px;
    height: 1px;
    left: -9999px;
    top: -9999px;
    background-image: url("{alert_url}");
}}
"""
    return Response(css, media_type="text/css")

@router.get("api/tokens/resources/{token_uuid}/favicon.ico")
async def browser_favico():
    return PDF_ICON_BYTES
