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


@router.get("api/tokens/resources/{token_uuid}/favicon.ico")
async def browser_favico():
    return PDF_ICON_BYTES
