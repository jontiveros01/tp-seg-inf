import uuid
from pathlib import Path

import click
import qrcode
from settings import get_settings


def qr(message: str, output: str, uuid: uuid.UUID):
    """Generate a QR honeytoken with a personalized message"""
    alert_url = f"{get_settings().API_BASE_URL}/api/tokens/alert/{uuid}"

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
