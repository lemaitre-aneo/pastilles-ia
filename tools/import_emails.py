#!/usr/bin/env python3
"""Importe les pastilles diffusees (.eml) dans un dossier de travail exploitable.

Pour chaque courriel du dossier `emails/`, produit `work/<slug>/`:
  - meta.json        : sujet, numero de diffusion, fichier source, images
  - source.txt       : partie text/plain du courriel
  - source.html      : partie text/html du courriel (emphases d'origine)
  - image-1.png, ... : images liees, dans l'ordre d'apparition dans le HTML

Usage: python3 tools/import_emails.py [dossier_emails] [dossier_travail]
"""

from __future__ import annotations

import email
import json
import os
import re
import sys
import unicodedata
from email import policy

EXT_BY_TYPE = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/gif": ".gif",
    "image/webp": ".webp",
}


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(c for c in value if not unicodedata.combining(c))
    value = value.replace("'", " ").replace("’", " ")
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return re.sub(r"-{2,}", "-", value)[:60]


def parse_subject(subject: str) -> tuple[str, str]:
    """Renvoie (numero de diffusion, titre) a partir du sujet du courriel."""
    subject = " ".join(subject.split())
    match = re.search(r"#(\d+)\s*:\s*(.*)$", subject)
    if not match:
        return "", subject
    return match.group(1), match.group(2).strip()


def cid_order(html: str) -> list[str]:
    return re.findall(r'src="cid:([^"]+)"', html)


def import_email(path: str, workdir: str) -> dict:
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        msg = email.message_from_file(handle, policy=policy.default)

    subject = msg["subject"] or os.path.basename(path)
    number, title = parse_subject(subject)

    text_part = ""
    html_part = ""
    images: dict[str, tuple[str, bytes]] = {}
    for part in msg.walk():
        ctype = part.get_content_type()
        if ctype == "text/plain" and not text_part:
            text_part = part.get_content()
        elif ctype == "text/html" and not html_part:
            html_part = part.get_content()
        elif part.get_content_maintype() == "image":
            cid = (part.get("content-id") or "").strip("<>")
            images[cid] = (ctype, part.get_payload(decode=True))

    slug = f"{int(number):02d}-{slugify(title)}" if number else slugify(title)
    outdir = os.path.join(workdir, slug)
    os.makedirs(outdir, exist_ok=True)

    with open(os.path.join(outdir, "source.txt"), "w", encoding="utf-8") as handle:
        handle.write(text_part)
    with open(os.path.join(outdir, "source.html"), "w", encoding="utf-8") as handle:
        handle.write(html_part)

    written = []
    ordered = [cid for cid in cid_order(html_part) if cid in images]
    ordered += [cid for cid in images if cid not in ordered]
    for index, cid in enumerate(ordered, start=1):
        ctype, payload = images[cid]
        name = f"image-{index}{EXT_BY_TYPE.get(ctype, '.bin')}"
        with open(os.path.join(outdir, name), "wb") as handle:
            handle.write(payload)
        written.append({"file": name, "cid": cid, "type": ctype, "bytes": len(payload)})

    meta = {
        "slug": slug,
        "subject": " ".join(subject.split()),
        "numero_diffusion": number,
        "titre_diffuse": title,
        "source_eml": os.path.basename(path),
        "images": written,
    }
    with open(os.path.join(outdir, "meta.json"), "w", encoding="utf-8") as handle:
        json.dump(meta, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return meta


def main() -> None:
    emails_dir = sys.argv[1] if len(sys.argv) > 1 else "emails"
    workdir = sys.argv[2] if len(sys.argv) > 2 else "work"
    os.makedirs(workdir, exist_ok=True)
    for name in sorted(os.listdir(emails_dir)):
        if not name.lower().endswith(".eml"):
            continue
        meta = import_email(os.path.join(emails_dir, name), workdir)
        print(f"{meta['slug']}: {len(meta['images'])} image(s) - {meta['subject']}")


if __name__ == "__main__":
    main()
