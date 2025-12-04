import uuid
from pathlib import Path
import qrcode
from settings import get_settings
import tkinter.filedialog as fdialog


def qr(uuid: uuid.UUID):
    """Generate a QR honeytoken"""
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

    result_path = fdialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG image", "*.png")]
    )

    if result_path:
        img.save(result_path)
