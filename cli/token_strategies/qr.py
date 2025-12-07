import tkinter.filedialog as fdialog
import uuid
from pathlib import Path

import qrcode

from cli.settings import get_settings


def qr(uuid: uuid.UUID):
    """Generates a QR honeytoken"""
    alert_url = f"{get_settings().API_BASE_URL}/api/tokens/alert/{uuid}"

    try:
        qr_obj = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr_obj.add_data(alert_url)
        qr_obj.make(fit=True)

        img = qr_obj.make_image(fill_color="black", back_color="white")

        result_path = fdialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG image", "*.png")]
        )

        if not result_path: return

        img.save(result_path)
        return True 
    except Exception as e:
        print(f"Error generating honeytoken: {e}")
        return False