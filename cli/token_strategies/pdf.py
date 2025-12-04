import datetime
import os
import tkinter.filedialog as fdialog
import uuid

from settings import get_settings

try:
    from pypdf import PdfReader, PdfWriter, generic
    from pypdf.generic import TextString
except ImportError:
    print(
        "ERROR: 'pypdf' library not found. Please run 'pip install pypdf' to enable this feature."
    )


def pdf(uuid: uuid):
    """
    Modifies an existing PDF to execute a JavaScript payload on open and ping the server.
    """

    alert_url = f"{get_settings().API_BASE_URL}/api/tokens/alert/{uuid}"

    js_payload = f"""
    try {{
        this.getURL("{alert_url}", false);
    }} catch(e) {{
        console.println("PDF JS Error: " + e.message);
    }}
    """

    print(f"Please select a file to use as a basis")
    base_pdf = fdialog.askopenfile()

    try:
        reader = PdfReader(base_pdf)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        js_action = generic.DictionaryObject(
            {
                generic.NameObject("/S"): generic.NameObject("/JavaScript"),
                generic.NameObject("/JS"): TextString(js_payload),
            }
        )

        writer.set_open_action(js_action)

        print(f"Honeytoken file generated. Select save location")

        result_file = fdialog.asksaveasfile()
        writer.write(result_file)

        print(f"PDF Honeytoken created")

    except Exception as e:
        print(f"Error modifying PDF: {e}")
