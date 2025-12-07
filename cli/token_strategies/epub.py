import zipfile
import shutil
import tkinter.filedialog as fdialog
from cli.settings import get_settings

def epub(token_uuid): 
    """
    Generates an EPUB honeytoken by injecting a remote reference resource call.
    """
    
    alert_url = f"{get_settings().API_BASE_URL}/api/tokens/alert/{token_uuid}"
    payload = f'<img src="{alert_url}" style="display:none;" alt="" />'

    print("Select EPUB file to use as base")
    original_path = fdialog.askopenfilename(
        title="Select base epub file",
        filetypes=[("eBook EPUB", "*.epub")]
    )
    
    if not original_path: 
        return

    print("Select where to save the resulting honeytoken")
    output_path = fdialog.asksaveasfilename(
        title="Save resulting honeytoken as...",
        defaultextension=".epub",
        filetypes=[("eBook EPUB", "*.epub")]
    )

    if not output_path:
        return

    try:
        with zipfile.ZipFile(original_path, "r") as zin:
            with zipfile.ZipFile(output_path, "w") as zout:
                for item in zin.infolist():
                    buffer = zin.read(item.filename)
                    
                    if item.filename.endswith((".html", ".xhtml")):
                        try:
                            content = buffer.decode("utf-8")
                            if "</body>" in content:
                                content = content.replace("</body>", payload + "</body>")
                                buffer = content.encode("utf-8")
                        except UnicodeDecodeError:
                            pass 
                    
                    zout.writestr(item, buffer)
                    
        print(f"Honeytoken succesfully generated at {output_path}")
        return True

    except Exception as e:
        print(f"Error generating honeytoken EPUB: {e}")
        return False