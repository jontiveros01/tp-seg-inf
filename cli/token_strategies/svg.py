import xml.etree.ElementTree as ET
import tkinter.filedialog as fdialog
from cli.settings import get_settings

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"

ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", XLINK_NS)

def svg(token_uuid):
    """
    Generates an SVG Honeytoken by injecting a remote <image> tag that triggers a callback when rendered.
    """
    
    alert_url = f"{get_settings().API_BASE_URL}/resources/{token_uuid}"

    print("Select the source SVG file.")
    original_path = fdialog.askopenfilename(
        title="Select Base SVG",
        filetypes=[("SVG Image", "*.svg")]
    )
    
    if not original_path: return

    print("Select where to save the Honeytoken.")
    output_path = fdialog.asksaveasfilename(
        title="Save Honeytoken as...",
        defaultextension=".svg",
        filetypes=[("SVG Image", "*.svg")]
    )

    if not output_path: return

    try:
        tree = ET.parse(original_path)
        root = tree.getroot()

        trap = ET.Element(f"{{{SVG_NS}}}image")
        
        trap.set("width", "1")
        trap.set("height", "1")
        trap.set("opacity", "0") 
        trap.set("x", "0")
        trap.set("y", "0")
    
        trap.set("href", alert_url)
        trap.set(f"{{{XLINK_NS}}}href", alert_url)

        root.append(trap)

        tree.write(output_path, encoding="utf-8", xml_declaration=True)
            
        print(f"SVG Honeytoken generated successfully at: {output_path}")
        return True

    except Exception as e:
        print(f"Error generating honeytoken: {e}")
        return False