import tkinter.filedialog as fdialog
from pathlib import Path

from cli.settings import get_settings


def _inject_external_css(html: str, css_url: str) -> str:
    link_tag = f'<link rel="stylesheet" href="{css_url}">'
    lower = html.lower()
    idx = lower.find("</head>")

    if idx != -1:
        return html[:idx] + link_tag + "\n" + html[idx:]

    return link_tag + "\n" + html


def _inject_before_body_end(html: str, snippet: str) -> str:
    lower = html.lower()
    idx = lower.rfind("</body>")

    if idx != -1:
        return html[:idx] + snippet + "\n" + html[idx:]

    return html + "\n" + snippet


def _strategy_remote_css(original_html: str, token_id: str) -> str:
    fake_css_url = f"{get_settings().API_BASE_URL}/resources/{token_id}"
    return _inject_external_css(original_html, fake_css_url)


def _strategy_fetch_script(original_html: str, token_id: str) -> str:
    alert_url = f"{get_settings().API_BASE_URL}/api/tokens/alert/{token_id}"
    snippet = f"""
<script>
fetch("{alert_url}").catch(()=>{{}});
</script>
"""
    return _inject_before_body_end(original_html, snippet)


def _strategy_css_bg(original_html: str, token_id: str) -> str:
    alert_url = f"{get_settings().API_BASE_URL}/api/tokens/alert/{token_id}"
    safe_id = token_id.replace("-", "")[:8]
    element_id = f"htkn_{safe_id}"

    snippet = f"""
<style>
#{element_id} {{
    background-image: url("{alert_url}");
}}
</style>
<div id="{element_id}"></div>
"""
    return _inject_before_body_end(original_html, snippet)


STRATEGIES = {
    "remote-css": _strategy_remote_css,
    "fetch-script": _strategy_fetch_script,
    "css-bg": _strategy_css_bg,
}


def html(token_id: str, html_strategy: str):
    """
    Modifies an existing HTML based on the selected strategy.
    """

    if html_strategy not in STRATEGIES:
        print(f"Unknown HTML strategy: {html_strategy}")
        return

    print("Please select an HTML file to use as a basis")
    base_html_file = fdialog.askopenfile()

    if base_html_file is None:
        print("No file selected, aborting.")
        return

    try:
        original_html = base_html_file.read()

        strategy_fn = STRATEGIES[html_strategy]
        modified_html = strategy_fn(original_html, token_id)

        print("Honeytoken HTML generated. Select save location")
        result_file = fdialog.asksaveasfile(defaultextension=".html")

        if result_file is None: return

        result_file.write(modified_html)
        print("HTML honeytoken created successfully.")
        return True

    except Exception as e:
        print(f"Error generating honeytoken: {e}")
        return False
