import zipfile
import re
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fdialog
from cli.settings import get_settings
from lxml import etree

NS = {
    'w': "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    'r': "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    'wp': "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    'a': "http://schemas.openxmlformats.org/drawingml/2006/main",
    'pic': "http://schemas.openxmlformats.org/drawingml/2006/picture",
    'pkg': "http://schemas.openxmlformats.org/package/2006/relationships"
}

def E(tag, *children, **kwargs):
    elem = etree.Element(f"{{{NS['w']}}}{tag}", nsmap=NS, **kwargs)
    for child in children: elem.append(child)
    return elem

def WP(tag, *children, **kwargs):
    elem = etree.Element(f"{{{NS['wp']}}}{tag}", nsmap=NS, **kwargs)
    for child in children: elem.append(child)
    return elem

def A(tag, *children, **kwargs):
    elem = etree.Element(f"{{{NS['a']}}}{tag}", nsmap=NS, **kwargs)
    for child in children: elem.append(child)
    return elem

def PIC(tag, *children, **kwargs):
    elem = etree.Element(f"{{{NS['pic']}}}{tag}", nsmap=NS, **kwargs)
    for child in children: elem.append(child)
    return elem

def _get_next_rid(tree):
    rids = tree.xpath("//pkg:Relationship/@Id", namespaces=NS)
    ids = [int(re.search(r"\d+", rid).group()) for rid in rids if re.search(r"\d+", rid)]
    return f"rId{max(ids) + 1}" if ids else "rId1"


def _inject_image(zin, zout, alert_url):
    """
    Injects a standard inline image into the document body.
    """
    target_rid = None
    
    # 1. Update Relationships
    # Note: We use the 'pkg' namespace for reading Relationship tags in .rels files
    if "word/_rels/document.xml.rels" in zin.namelist():
        rels_tree = etree.fromstring(zin.read("word/_rels/document.xml.rels"))
        target_rid = _get_next_rid(rels_tree)
    else:
        target_rid = "rId1"
        rels_tree = etree.Element(f"{{{NS['pkg']}}}Relationships", nsmap={None: NS['pkg']})

    etree.SubElement(rels_tree, f"{{{NS['pkg']}}}Relationship", 
                     Id=target_rid, 
                     Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image", 
                     Target=alert_url, 
                     TargetMode="External")

    doc_tree = None
    if "word/document.xml" in zin.namelist():
        doc_tree = etree.fromstring(zin.read("word/document.xml"))
        body = doc_tree.find("w:body", namespaces=NS)
        
        if body is not None:
            SIZE = "12700" 
            
            drawing_xml = E("p",
                E("r",
                    E("drawing",
                        WP("inline",
                            WP("extent", cx=SIZE, cy=SIZE),
                            WP("docPr", id="666", name="HoneyToken"),
                            A("graphic",
                                A("graphicData", 
                                    PIC("pic",
                                        PIC("nvPicPr",
                                            PIC("cNvPr", id="0", name="HoneyToken"),
                                            PIC("cNvPicPr")
                                        ),
                                        PIC("blipFill",
                                            A("blip", **{f"{{{NS['r']}}}link": target_rid}),
                                            A("stretch", A("fillRect"))
                                        ),
                                        PIC("spPr",
                                            A("xfrm", 
                                                A("off", x="0", y="0"), 
                                                A("ext", cx=SIZE, cy=SIZE)
                                            ),
                                            A("prstGeom", A("avLst"), prst="rect")
                                        )
                                    ),
                                    uri="http://schemas.openxmlformats.org/drawingml/2006/picture"
                                )
                            ),
                            distT="0", distB="0", distL="0", distR="0"
                        )
                    )
                )
            )
            body.insert(0, drawing_xml)

    for item in zin.infolist():
        if item.filename == "word/_rels/document.xml.rels":
            zout.writestr(item, etree.tostring(rels_tree, xml_declaration=True, encoding="utf-8"))
        elif item.filename == "word/document.xml":
            zout.writestr(item, etree.tostring(doc_tree, xml_declaration=True, encoding="utf-8"))
        else:
            zout.writestr(item, zin.read(item.filename))

def _inject_template(zin, zout, alert_url):
    modified_files = {}
    file_list = zin.namelist()
    
    # 1. Content Types
    if "[Content_Types].xml" in file_list:
        ct_tree = etree.fromstring(zin.read("[Content_Types].xml"))
        # Using specific namespace map for ContentTypes
        CT_NS = {'c': "http://schemas.openxmlformats.org/package/2006/content-types"}
        if not ct_tree.xpath(f"//c:Override[@PartName='/word/settings.xml']", namespaces=CT_NS):
            etree.SubElement(ct_tree, f"{{{CT_NS['c']}}}Override", 
                             PartName="/word/settings.xml", 
                             ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml")
            modified_files["[Content_Types].xml"] = etree.tostring(ct_tree, xml_declaration=True, encoding="utf-8")


    if "word/_rels/document.xml.rels" in file_list:
        doc_rels_tree = etree.fromstring(zin.read("word/_rels/document.xml.rels"))
    else:
        doc_rels_tree = etree.Element(f"{{{NS['pkg']}}}Relationships", nsmap={None: NS['pkg']})
    
    settings_rid = None
    existing_rels = doc_rels_tree.xpath(f"//pkg:Relationship[@Target='settings.xml']", namespaces=NS)
    
    if existing_rels:
        settings_rid = existing_rels[0].get("Id")
    else:
        settings_rid = _get_next_rid(doc_rels_tree)
        etree.SubElement(doc_rels_tree, f"{{{NS['pkg']}}}Relationship", 
                         Id=settings_rid, 
                         Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings", 
                         Target="settings.xml")
        modified_files["word/_rels/document.xml.rels"] = etree.tostring(doc_rels_tree, xml_declaration=True, encoding="utf-8")

    if "word/_rels/settings.xml.rels" in file_list:
        sett_rels_tree = etree.fromstring(zin.read("word/_rels/settings.xml.rels"))
    else:
        sett_rels_tree = etree.Element(f"{{{NS['pkg']}}}Relationships", nsmap={None: NS['pkg']})

    template_rid = _get_next_rid(sett_rels_tree)
    etree.SubElement(sett_rels_tree, f"{{{NS['pkg']}}}Relationship", 
                     Id=template_rid, 
                     Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/attachedTemplate", 
                     Target=alert_url, 
                     TargetMode="External")
    modified_files["word/_rels/settings.xml.rels"] = etree.tostring(sett_rels_tree, xml_declaration=True, encoding="utf-8")


    if "word/settings.xml" in file_list:
        settings_tree = etree.fromstring(zin.read("word/settings.xml"))
    else:
        settings_tree = etree.Element(f"{{{NS['w']}}}settings", nsmap={'w': NS['w'], 'r': NS['r']})

    tmpl_node = settings_tree.find("w:attachedTemplate", namespaces=NS)
    if tmpl_node is not None:
        tmpl_node.set(f"{{{NS['r']}}}id", template_rid)
    else:
        tmpl_node = etree.Element(f"{{{NS['w']}}}attachedTemplate", nsmap={'r': NS['r']})
        tmpl_node.set(f"{{{NS['r']}}}id", template_rid)
        settings_tree.insert(0, tmpl_node)
        
    modified_files["word/settings.xml"] = etree.tostring(settings_tree, xml_declaration=True, encoding="utf-8")


    with zipfile.ZipFile(zout.filename, "w") as zfinal: 
        pass 
    for fname, content in modified_files.items():
        zout.writestr(fname, content)
    for item in zin.infolist():
        if item.filename not in modified_files:
            zout.writestr(item, zin.read(item.filename))

def docx(token_uuid, strategy):
    alert_base = f"{get_settings().API_BASE_URL}/resources/{token_uuid}"
    
    print("Select the source .docx file.")
    original_path = fdialog.askopenfilename(title="Select Base Word Doc", filetypes=[("Word Document", "*.docx")])
    if not original_path: return

    print("Select where to save the Honeytoken.")
    output_path = fdialog.asksaveasfilename(title="Save Word Honeytoken", defaultextension=".docx", filetypes=[("Word Document", "*.docx")])
    if not output_path: return


    try:
        with zipfile.ZipFile(original_path, "r") as zin:
            with zipfile.ZipFile(output_path, "w") as zout:
                match strategy:
                    case "image":
                        _inject_image(zin, zout, f"{alert_base}/logo.png")
                    case "template":
                        _inject_template(zin, zout, f"{alert_base}/global_styles.dotm")

        print(f"Word Honeytoken generated at: {output_path}")

        return True

    except Exception as e:
        print(f"Error generating honeytoken: {e}")
        return False