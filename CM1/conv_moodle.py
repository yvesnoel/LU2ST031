import re
import xml.etree.ElementTree as ET
from xml.dom import minidom


def parse_markdown(md_text):
    """
    Convertit le markdown en structure :
    [
        {
            "title": "...",
            "content": "...",
            "subchapters": [
                {"title": "...", "content": "..."}
            ]
        }
    ]
    """
    chapters = []
    current_chapter = None
    current_sub = None

    lines = md_text.split("\n")

    buffer = []

    def flush_buffer():
        nonlocal buffer, current_chapter, current_sub
        content = "\n".join(buffer).strip()
        buffer = []

        if not content:
            return

        if current_sub is not None:
            current_sub["content"] += "\n" + content
        elif current_chapter is not None:
            current_chapter["content"] += "\n" + content

    for line in lines:
        if line.startswith("## "):
            flush_buffer()
            title = line.replace("## ", "").strip()

            current_chapter = {
                "title": title,
                "content": "",
                "subchapters": []
            }
            chapters.append(current_chapter)
            current_sub = None

        elif line.startswith("### "):
            flush_buffer()
            title = line.replace("### ", "").strip()

            current_sub = {
                "title": title,
                "content": ""
            }
            current_chapter["subchapters"].append(current_sub)

        else:
            buffer.append(line)

    flush_buffer()
    return chapters


def convert_admonitions(md):
    """
    Convertit les admonitions MyST en HTML simple
    """
    pattern = re.compile(
        r"```{admonition} (.*?)\n:class: (.*?)\n(.*?)```",
        re.DOTALL
    )

    def repl(match):
        title = match.group(1)
        klass = match.group(2)
        content = match.group(3).strip()

        color = {
            "note": "#d9edf7",
            "warning": "#fcf8e3",
            "caution": "#f2dede",
            "tip": "#dff0d8"
        }.get(klass, "#eeeeee")

        return f"""
<div style="border-left: 5px solid #999; background:{color}; padding:10px; margin:10px 0;">
<strong>{title}</strong><br>
{content}
</div>
"""

    return pattern.sub(repl, md)


def markdown_to_html(md):
    """
    Conversion très simple Markdown → HTML
    (tu peux améliorer plus tard avec markdown2 ou mistune)
    """
    md = convert_admonitions(md)

    # gras
    md = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", md)

    # italique
    md = re.sub(r"\*(.*?)\*", r"<em>\1</em>", md)

    # code inline
    md = re.sub(r"`(.*?)`", r"<code>\1</code>", md)

    # sauts de ligne
    md = md.replace("\n", "<br>")

    return md


def build_moodle_xml(chapters):
    root = ET.Element("BOOK")

    id_counter = 1

    for ch in chapters:
        ch_elem = ET.SubElement(root, "CHAPTER")
        ET.SubElement(ch_elem, "ID").text = str(id_counter)
        ET.SubElement(ch_elem, "TITLE").text = ch["title"]
        ET.SubElement(ch_elem, "PARENT").text = "0"
        ET.SubElement(ch_elem, "CONTENT").text = markdown_to_html(ch["content"])

        parent_id = id_counter
        id_counter += 1

        for sub in ch["subchapters"]:
            sub_elem = ET.SubElement(root, "CHAPTER")
            ET.SubElement(sub_elem, "ID").text = str(id_counter)
            ET.SubElement(sub_elem, "TITLE").text = sub["title"]
            ET.SubElement(sub_elem, "PARENT").text = str(parent_id)
            ET.SubElement(sub_elem, "CONTENT").text = markdown_to_html(sub["content"])

            id_counter += 1

    return root


def save_pretty_xml(element, filename):
    rough = ET.tostring(element, "utf-8")
    reparsed = minidom.parseString(rough)
    pretty = reparsed.toprettyxml(indent="  ")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(pretty)


# =========================
# UTILISATION
# =========================

if __name__ == "__main__":
    with open("Les_expressions.md", "r", encoding="utf-8") as f:
        md_text = f.read()

    chapters = parse_markdown(md_text)
    xml_tree = build_moodle_xml(chapters)

    save_pretty_xml(xml_tree, "moodle_book.xml")

    print("✅ Livre Moodle généré : moodle_book.xml")
