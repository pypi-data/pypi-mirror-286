import json
import logging
import re
import string
from html import escape, unescape
from pathlib import Path

import mkdocs
from bs4 import BeautifulSoup
from lxml import etree
from mkdocs.plugins import BasePlugin


# ------------------------
# Plugin
# ------------------------
class DrawioPlugin(BasePlugin):
    """
    Plugin for embedding Drawio Diagrams into your MkDocs
    """

    config_scheme = (
        (
            "viewer_js",
            mkdocs.config.config_options.Type(
                str, default="https://viewer.diagrams.net/js/viewer-static.min.js"
            ),
        ),
    )

    def __init__(self):
        self.log = logging.getLogger("mkdocs.plugins.diagrams")
        self.pool = None

    def on_post_page(self, output_content, config, page, **kwargs):
        return self.render_drawio_diagrams(output_content, page)

    def render_drawio_diagrams(self, output_content, page):
        if ".drawio" not in output_content.lower():
            # Skip unecessary HTML parsing
            return output_content

        plugin_config = self.config.copy()

        soup = BeautifulSoup(output_content, "html.parser")

        # search for images using drawio extension
        diagrams = soup.findAll("img", src=re.compile(r".*\.drawio$", re.IGNORECASE))
        if len(diagrams) == 0:
            return output_content

        # add drawio library to body
        lib = soup.new_tag("script", src=plugin_config["viewer_js"])
        soup.body.append(lib)

        # substitute images with embedded drawio diagram
        path = Path(page.file.abs_dest_path).parent

        for diagram in diagrams:
            diagram.replace_with(
                BeautifulSoup(
                    DrawioPlugin.substitute_image(path, diagram["src"], diagram["alt"]),
                    "html.parser",
                )
            )

        return str(soup)

    @staticmethod
    def substitute_image(path: Path, src: str, alt: str):

        config = {
            "highlight": "#0000ff",
            "nav": True,
            "resize": True,
            "toolbar": "zoom layers tags lightbox tab",
            "edit": "_blank",
            "url": src,
        }

        data = f'<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{escape(json.dumps(config))}"></div>'
        return data
