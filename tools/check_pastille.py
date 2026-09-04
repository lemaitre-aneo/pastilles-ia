#!/usr/bin/env python3
"""Verifie qu'une pastille reexportee respecte le gel du corps et le gabarit.

Controles:
  1. chaque paragraphe de corps du courriel d'origine se retrouve mot pour mot
     dans le HTML reexporte (comparaison sur le texte rendu, hors balises);
  2. aucun crochet de gabarit ne subsiste;
  3. aucun tiret cadratin;
  4. les deux images portent un texte alternatif non vide;
  5. les jetons cid:IMAGE_TITRE et cid:IMAGE_SCHEMA sont presents;
  6. l'encadre L'essentiel est present, et un seul bloc annexe au maximum.

Usage: python3 tools/check_pastille.py work/<slug> pastilles/<slug>
       python3 tools/check_pastille.py --all
"""

from __future__ import annotations

import difflib
import json
import os
import re
import sys

MIN_BODY_WORDS = 25


BLOCK_TAGS = "div|p|br|tr|td|th|table|tbody|ul|ol|li|h[1-6]|blockquote|hr|img"


def render_text(html: str) -> str:
    """Texte rendu, balises retirees, espaces normalises.

    Les balises de bloc valent une separation, les balises en ligne (emphases)
    n'en valent aucune: sinon `<i>mot</i>,` deviendrait `mot ,` et toute
    emphase posee a cheval sur un espace passerait pour une modification.
    """
    text = re.sub(r"(?is)<(script|style).*?</\1>", " ", html)
    text = re.sub(rf"(?i)</?({BLOCK_TAGS})\b[^>]*>", " ", text)
    text = re.sub(r"<[^>]+>", "", text)
    replacements = {
        "&nbsp;": " ", "&#160;": " ", "&amp;": "&", "&lt;": "<",
        "&gt;": ">", "&quot;": '"', "&#39;": "'", "&middot;": "·",
    }
    for needle, value in replacements.items():
        text = text.replace(needle, value)
    return re.sub(r"\s+", " ", text).strip()


def source_paragraphs(html: str) -> list[str]:
    """Paragraphes de corps du courriel d'origine (hors intro, mention et signature)."""
    blocks = re.findall(r"(?is)<div[^>]*>(.*?)</div>", html)
    paragraphs = []
    for block in blocks:
        text = render_text(block)
        if len(text.split()) < MIN_BODY_WORDS:
            continue
        lowered = text.lower()
        if lowered.startswith("bonjour") or "pastille llm du jour" in lowered:
            continue
        if "peut contenir des traces d" in lowered:
            continue
        if text not in paragraphs:
            paragraphs.append(text)
    return paragraphs


def check(workdir: str, outdir: str) -> tuple[list[str], list[str]]:
    """Renvoie (problemes bloquants, avertissements).

    Une derogation au gel du corps tracee dans `gel-exceptions.json` a cote du
    livrable n'est pas un echec: elle est appliquee au texte d'origine avant
    comparaison, puis rappelee en avertissement pour rester visible.
    """
    problems: list[str] = []
    warnings: list[str] = []
    with open(os.path.join(workdir, "source.html"), encoding="utf-8") as handle:
        source = handle.read()
    html_path = os.path.join(outdir, "pastille.html")
    if not os.path.exists(html_path):
        return [f"{html_path} absent"], warnings
    with open(html_path, encoding="utf-8") as handle:
        exported = handle.read()

    rendered = render_text(exported)

    # Derogations au gel du corps, decidees explicitement et tracees a cote du
    # livrable. Elles sont appliquees au texte d'origine avant comparaison, et
    # rappelees en avertissement pour rester visibles a la relecture.
    exceptions = []
    exceptions_path = os.path.join(outdir, "gel-exceptions.json")
    if os.path.exists(exceptions_path):
        with open(exceptions_path, encoding="utf-8") as handle:
            exceptions = json.load(handle)
        for entry in exceptions:
            warnings.append(f"derogation au gel: {entry['raison']}")

    for index, paragraph in enumerate(source_paragraphs(source), start=1):
        for entry in exceptions:
            paragraph = paragraph.replace(entry["origine"], entry["reexport"])
        if paragraph in rendered:
            continue
        best = difflib.get_close_matches(paragraph, re.split(r"(?<=[.!?]) ", rendered), n=1)
        problems.append(
            f"paragraphe {index} modifie ou absent du reexport\n"
            f"    origine : {paragraph[:160]}...\n"
            f"    proche   : {(best[0][:160] + '...') if best else '(rien de proche)'}"
        )

    for token in re.findall(r"\[[A-Z][A-Z ÉÈÊÀÇ'0-9_.:-]{3,}\]", exported):
        problems.append(f"crochet de gabarit residuel: {token}")
    if "—" in exported:
        problems.append(
            "tiret cadratin present: le remplacer par des parentheses ou des virgules, et tracer "
            "la correction dans gel-exceptions.json si elle touche le corps gele"
        )
    for token in ("cid:IMAGE_TITRE", "cid:IMAGE_SCHEMA"):
        if token not in exported:
            problems.append(f"jeton {token} absent")
    for alt in re.findall(r'<img[^>]*alt="([^"]*)"', exported):
        if not alt.strip():
            problems.append("texte alternatif vide")
    if len(re.findall(r'<img\b', exported)) != 2:
        problems.append("le reexport ne porte pas exactement deux images")
    if "L'ESSENTIEL" not in exported:
        problems.append("encadre L'essentiel absent")
    annexes = sum(1 for label in ("A ESSAYER", "LE PIEGE", "LE PIÈGE", "À ESSAYER") if label in exported)
    if annexes > 1:
        problems.append("plus d'un bloc annexe")
    if not re.search(r"\d+ min de lecture", exported):
        problems.append("temps de lecture absent du bandeau")
    return problems, warnings


def main() -> None:
    if sys.argv[1:2] == ["--all"]:
        pairs = []
        for slug in sorted(os.listdir("pastilles")):
            if os.path.isdir(os.path.join("work", slug)):
                pairs.append((os.path.join("work", slug), os.path.join("pastilles", slug)))
    else:
        pairs = [(sys.argv[1], sys.argv[2])]

    failed = False
    for workdir, outdir in pairs:
        problems, warnings = check(workdir, outdir)
        label = os.path.basename(outdir)
        if problems:
            failed = True
            print(f"[KO] {label}")
        else:
            print(f"[OK] {label}")
        for problem in problems:
            print(f"  - {problem}")
        for warning in warnings:
            print(f"  ! {warning}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
