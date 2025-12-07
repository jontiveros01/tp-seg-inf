import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fdialog
from cli.settings import get_settings
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
        DictionaryObject, 
        NameObject, 
        TextStringObject, 
        NumberObject, 
        ArrayObject, 
        FloatObject,
        BooleanObject
    )

BROWSER_WARNING_TEXT = (
    "\r\r\r\r\r\r\r\r\r\r\r\r" 
    "CRITICAL LOADING ERROR\r\r"
    "The document contains dynamic external resources\r"
    "that could not be rendered by the current viewer.\r\r"
    "TO RESOLVE:\r"
    "1. Open this file in Adobe Acrobat Reader.\r"
    "2. If prompted, click 'Allow' to load remote assets.\r\r"
    "Error Code: 0x80040154 (Class not registered)"
)


def _create_uri_action(masked_url):
    return DictionaryObject({
        NameObject("/S"): NameObject("/URI"),
        NameObject("/URI"): TextStringObject(masked_url)
    })

def _create_trap_js_action(alert_url):
    js_code = f"""
    var unlock = function() {{
        var f = this.getField("TrapField");
        if (f) {{
            f.display = display.hidden;
            f.readonly = true;
        }}
        var annots = this.getAnnots();
        if (annots) {{
            for (var i = 0; i < annots.length; i++) {{
                if (annots[i].subject == "WhiteBlocker") {{
                    annots[i].destroy();
                }}
            }}
        }}
    }};

    try {{ 
        this.submitForm({{
            cURL: "{alert_url}", 
            cSubmitAs: "HTML"
        }});
        
        unlock();
        
    }} catch(e) {{
        app.alert("Error: External resources are required to view this document.");
    }}
    """
    return DictionaryObject({
        NameObject("/S"): NameObject("/JavaScript"),
        NameObject("/JS"): TextStringObject(js_code)
    })

def _apply_browser_trap_layer(writer):
    if "/AcroForm" not in writer.root_object:
        writer.root_object[NameObject("/AcroForm")] = DictionaryObject({
            NameObject("/Fields"): ArrayObject(),
            NameObject("/DA"): TextStringObject("/Helv 0 Tf 0 g"),
            NameObject("/NeedAppearances"): BooleanObject(True) 
        })
    
    acroform = writer.root_object["/AcroForm"]
    
    for page in writer.pages:
        if page.mediabox:
            mediabox = page.mediabox
            ll_x, ll_y = float(mediabox[0]), float(mediabox[1])
            ur_x, ur_y = float(mediabox[2]), float(mediabox[3])
        else:
            ll_x, ll_y, ur_x, ur_y = 0.0, 0.0, 595.0, 842.0

        rect = ArrayObject([FloatObject(ll_x), FloatObject(ll_y), FloatObject(ur_x), FloatObject(ur_y)])

        white_square = DictionaryObject({
            NameObject("/Type"): NameObject("/Annot"),
            NameObject("/Subtype"): NameObject("/Square"),
            NameObject("/Rect"): rect,
            NameObject("/C"): ArrayObject([FloatObject(1), FloatObject(1), FloatObject(1)]), 
            NameObject("/IC"): ArrayObject([FloatObject(1), FloatObject(1), FloatObject(1)]), 
            NameObject("/Subj"): TextStringObject("WhiteBlocker"), 
            NameObject("/F"): NumberObject(4) 
        })

        trap_widget = DictionaryObject({
            NameObject("/Type"): NameObject("/Annot"),
            NameObject("/Subtype"): NameObject("/Widget"),
            NameObject("/FT"): NameObject("/Tx"), 
            NameObject("/T"): TextStringObject(f"TrapField"), 
            NameObject("/Rect"): rect,
            NameObject("/V"): TextStringObject(BROWSER_WARNING_TEXT),
            NameObject("/Q"): NumberObject(1),
            NameObject("/DA"): TextStringObject("/Helv 18 Tf 0 g"), 
            NameObject("/Ff"): NumberObject(4101),
            NameObject("/F"): NumberObject(4)
        })

        if "/Annots" not in page: page[NameObject("/Annots")] = ArrayObject()
        
        page[NameObject("/Annots")].append(white_square)
        page[NameObject("/Annots")].append(trap_widget)
        acroform["/Fields"].append(trap_widget)

def _apply_open_action(writer, action_dict):
    writer.root_object.update({
        NameObject("/OpenAction"): action_dict
    })

def _apply_invisible_links(writer, action_dict):
    for page in writer.pages:
        if page.mediabox:
            mediabox = page.mediabox
            ll_x, ll_y = float(mediabox[0]), float(mediabox[1])
            ur_x, ur_y = float(mediabox[2]), float(mediabox[3])
        else: ll_x, ll_y, ur_x, ur_y = 0.0, 0.0, 600.0, 800.0

        link = DictionaryObject({
            NameObject("/Type"): NameObject("/Annot"),
            NameObject("/Subtype"): NameObject("/Link"),
            NameObject("/Rect"): ArrayObject([FloatObject(ll_x), FloatObject(ll_y), FloatObject(ur_x), FloatObject(ur_y)]),
            NameObject("/Border"): ArrayObject([NumberObject(0), NumberObject(0), NumberObject(0)]),
            NameObject("/A"): action_dict
        })
        if "/Annots" not in page: page[NameObject("/Annots")] = ArrayObject()
        page[NameObject("/Annots")].append(link)

# --- MAIN ---
def pdf(token_uuid, strategy):
    alert_url = f"{get_settings().API_BASE_URL}/resources/{token_uuid}/logo.png"
    
    print("Select PDF file to use as base")
    original_path = fdialog.askopenfilename(title="Select Base PDF", filetypes=[("PDF Documents", "*.pdf")])
    if not original_path: return

    print("Select where to save the resulting honeytoken.")
    output_path = fdialog.asksaveasfilename(title="Save honeytoken as...", defaultextension=".pdf", filetypes=[("PDF Documents", "*.pdf")])
    if not output_path: return


    try:
        reader = PdfReader(original_path)
        writer = PdfWriter()
        writer.append_pages_from_reader(reader)

        match strategy:
            case "openaction":
                _apply_browser_trap_layer(writer)

                _apply_open_action(writer, _create_trap_js_action(alert_url))

            case "link":
                _apply_invisible_links(writer, _create_uri_action(alert_url))

        with open(output_path, "wb") as f:
            writer.write(f)
            
        print(f"PDF Honeytoken generated at {output_path}")
        return True

    except Exception as e:
        print(f"Error generating honeytoken: {e}")
        return False