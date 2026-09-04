#!/usr/bin/env python3
"""Reconstruit un courriel .eml diffusable a partir du HTML de la pastille et de ses images.

Attend un dossier de pastille contenant:
  - pastille.html    : le gabarit de diffusion rempli, avec src="cid:IMAGE_TITRE" et src="cid:IMAGE_SCHEMA"
  - image-titre.png  : l'illustration-titre
  - image-schema.png : le schema explicatif
  - meta.json        : au moins {"sujet": "..."} (sinon passer --sujet)

Produit `pastille.eml` dans le meme dossier: multipart/related, HTML plus images
liees par Content-ID, ouvrable directement dans un client de messagerie.

Usage: python3 tools/build_eml.py <dossier_pastille> [--sujet "..."]
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

CID_FILES = {
    "IMAGE_TITRE": ("image-titre.png", "image-titre.jpg"),
    "IMAGE_SCHEMA": ("image-schema.png", "image-schema.jpg"),
}


def find_image(folder: str, candidates: tuple[str, ...]) -> str:
    for name in candidates:
        path = os.path.join(folder, name)
        if os.path.exists(path):
            return path
    raise SystemExit(f"image absente dans {folder}: attendu l'un de {', '.join(candidates)}")


def strip_tags(html: str) -> str:
    text = re.sub(r"(?is)<(script|style).*?</\1>", " ", html)
    text = re.sub(r"(?i)<br\s*/?>|</(p|div|tr|li|table)>", "\n", text)
    text = re.sub(r"(?i)<li[^>]*>", "  * ", text)
    text = re.sub(r"<[^>]+>", "", text)
    replacements = {
        "&nbsp;": " ", "&middot;": "·", "&amp;": "&",
        "&lt;": "<", "&gt;": ">", "&quot;": '"', "&#39;": "'",
    }
    for needle, value in replacements.items():
        text = text.replace(needle, value)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    return "\n".join(line.strip() for line in text.splitlines()).strip()


def build(folder: str, sujet: str | None) -> str:
    html_path = os.path.join(folder, "pastille.html")
    if not os.path.exists(html_path):
        raise SystemExit(f"pastille.html absent dans {folder}")
    with open(html_path, "r", encoding="utf-8") as handle:
        html = handle.read()

    if sujet is None:
        meta_path = os.path.join(folder, "meta.json")
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as handle:
                sujet = json.load(handle).get("sujet")
    if not sujet:
        raise SystemExit("sujet introuvable: renseigner meta.json ou passer --sujet")

    images = {}
    for token, candidates in CID_FILES.items():
        path = find_image(folder, candidates)
        cid = make_msgid(idstring=token.lower())
        images[token] = (path, cid)
        html = html.replace(f"cid:{token}", f"cid:{cid.strip('<>')}")

    msg = EmailMessage()
    msg["Subject"] = sujet
    msg["Date"] = formatdate(localtime=True)
    msg["MIME-Version"] = "1.0"
    msg.set_content(strip_tags(html), subtype="plain", charset="utf-8")
    msg.add_alternative(
        "<html><head><meta charset=\"utf-8\"></head><body>\n" + html + "\n</body></html>",
        subtype="html",
        charset="utf-8",
    )

    html_part = msg.get_payload()[1]
    html_part.make_related()
    for path, cid in images.values():
        ctype, _ = mimetypes.guess_type(path)
        maintype, subtype = (ctype or "image/png").split("/", 1)
        with open(path, "rb") as handle:
            html_part.add_related(
                handle.read(),
                maintype=maintype,
                subtype=subtype,
                cid=cid,
                filename=os.path.basename(path),
            )

    out_path = os.path.join(folder, "pastille.eml")
    with open(out_path, "wb") as handle:
        handle.write(msg.as_bytes())
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    parser.add_argument("--sujet", default=None)
    args = parser.parse_args()
    print(build(args.folder, args.sujet))


if __name__ == "__main__":
    main()
