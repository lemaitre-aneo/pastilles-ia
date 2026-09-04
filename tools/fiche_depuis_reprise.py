#!/usr/bin/env python3
"""Construit une fiche officielle du skill `email` depuis une reprise deja faite.

La premiere passe de reprise (branche partie d'un commit anterieur au skill
`email`) avait produit un HTML au gabarit et un markdown de travail. Ce script
en derive la fiche JSON attendue par `build.py`, sans retranscrire le texte:
les paragraphes viennent du HTML deja verifie caractere par caractere contre le
courriel d'origine, les emphases HTML repassent en markdown, et la typographie
est laissee au renderer officiel, qui l'applique lui-meme.

Deux champs de reprise ne sont pas derivables d'un fichier et restent a
remplir par un relecteur qui regarde les visuels: `axe` et `apercu_visuels`.

Usage: python3 tools/fiche_depuis_reprise.py <slug> <dossier de sortie>
       python3 tools/fiche_depuis_reprise.py --tous <racine de sortie>
"""

from __future__ import annotations

import html as _html
import json
import os
import re
import shutil
import sys

TOTAL_SERIE = 45

# Numero d'envoi -> position dans la liste des 45, titre canonique, rubrique.
# Le numero d'envoi prime sur la liste, qui est un inventaire de sujets et non
# un ordre de diffusion; la rubrique, elle, suit le sujet reel.
CANONIQUE = {
    1: (1, "Au fait, c'est quoi un LLM ?", "Comprendre"),
    2: (16, "Anatomie d'un bon prompt : la recette de base", "Prompting"),
    3: (23, "Zéro syndrome de la page blanche : rédiger et reformuler ses mails ou CR", "Au travail"),
    4: (3, "Dans les coulisses : comment une IA apprend (sans vraiment comprendre)", "Comprendre"),
    6: (14, "L'art du Fact-Checking : comment ne pas gober les hallucinations de l'IA", "Limites"),
    7: (39, "Responsabilité : vous êtes le seul signataire de ce que produit l'IA", "Risques et cadre"),
    8: (4, 'Le contexte : la "mémoire vive" de l\'IA (ce qu\'elle voit à un instant T)', "Comprendre"),
    9: (18, "L'art de la discussion : pourquoi il faut itérer plutôt que tout demander d'un coup", "Prompting"),
    10: (17, "Les pièges du prompt : flou artistique et overdose d'instructions", "Prompting"),
    11: (28, "Mise en situation : préparer une réunion ou un brief client avec l'IA", "Au travail"),
    12: (40, "Confidentialité : où vont vraiment les données que vous tapez ?", "Risques et cadre"),
    13: (5, "Pourquoi l'IA oublie : la vérité sur la mémoire d'une session à l'autre", "Comprendre"),
    14: (12, "Zéro pointé : pourquoi l'IA est structurellement nulle en calcul mental", "Limites"),
}

STYLE_ANNEXE = {"A ESSAYER": ("À essayer", "essayer"), "À ESSAYER": ("À essayer", "essayer"),
                "LE PIEGE": ("Le piège", "piege"), "LE PIÈGE": ("Le piège", "piege")}


def en_markdown(fragment: str) -> str:
    """Texte d'un bloc HTML, emphases converties en markdown.

    Le gras d'Outlook arrive tantot en <b>, tantot en <span font-weight:600>;
    les deux comptent. Les balises restantes disparaissent sans laisser
    d'espace, sinon une emphase collee a la ponctuation ecarterait le signe.
    """
    texte = re.sub(r"(?is)<span[^>]*font-weight:\s*(?:600|700|bold)[^>]*>(.*?)</span>", r"<b>\1</b>", fragment)
    texte = re.sub(r"(?is)<(?:b|strong)>(.*?)</(?:b|strong)>", r"**\1**", texte)
    texte = re.sub(r"(?is)<(?:i|em)>(.*?)</(?:i|em)>", r"*\1*", texte)
    texte = re.sub(r"(?i)<br\s*/?>", " ", texte)
    texte = re.sub(r"<[^>]+>", "", texte)
    texte = _html.unescape(texte)
    # Le renderer officiel pose lui-meme les espaces insecables et les
    # apostrophes typographiques: on lui rend un texte en caracteres simples.
    texte = texte.replace(" ", " ").replace(" ", " ")
    return re.sub(r"\s+", " ", texte).strip()


def cellules_corps(html: str) -> list[tuple[str, str]]:
    """Les cellules du gabarit, dans l'ordre, sous forme (nature, contenu)."""
    blocs = []
    # Les attributs comptent autant que le contenu: c'est le style en ligne de
    # la cellule qui distingue un paragraphe de corps d'une legende.
    for attributs, cellule in re.findall(r"(?is)<td([^>]*)>(.*?)</td>", html):
        style = attributs
        if "L'ESSENTIEL" in cellule:
            puces = re.findall(r"(?is)<li[^>]*>(.*?)</li>", cellule)
            blocs.append(("essentiel", json.dumps([en_markdown(p) for p in puces], ensure_ascii=False)))
        elif re.search(r"<img[^>]*IMAGE_SCHEMA", cellule):
            alt = re.search(r'alt="([^"]*)"', cellule)
            blocs.append(("schema", _html.unescape(alt.group(1)) if alt else ""))
        elif any(label in cellule for label in STYLE_ANNEXE):
            label = next(l for l in STYLE_ANNEXE if l in cellule)
            corps = re.split(r"(?is)</div>", cellule)[-2] if "</div>" in cellule else cellule
            blocs.append(("annexe", f"{label}\n{en_markdown(corps)}"))
        elif "font-size:16px" in style and "line-height:26px" in style and "<img" not in cellule:
            blocs.append(("paragraphe", en_markdown(cellule)))
        elif "font-size:13px" in style and "color:#6B7280" in style and "italic" not in style:
            blocs.append(("legende", en_markdown(cellule)))
    return blocs


def sources_depuis_markdown(markdown: str) -> list:
    """Les sources de la section Sources, en objets titre plus url."""
    section = re.search(r"##\s*Sources(.*?)(?=\n##|\Z)", markdown, re.S)
    if not section:
        return []
    sources = []
    for ligne in section.group(1).splitlines():
        ligne = ligne.strip()
        if not ligne or not re.match(r"^([-*]|\d+\.)\s", ligne):
            continue
        lien = re.search(r"\[([^\]]+)\]\((https?://[^\)]+)\)", ligne)
        if lien:
            sources.append({"titre": lien.group(1).strip(), "url": lien.group(2).strip()})
            continue
        brut = re.search(r"(https?://\S+)", ligne)
        titre = re.sub(r"^([-*]|\d+\.)\s*", "", ligne)
        if brut:
            titre = titre.replace(brut.group(1), "").strip(" :,-()[]")
            sources.append({"titre": titre, "url": brut.group(1).rstrip(".,;)")})
        elif titre:
            sources.append(titre)
    return sources


def prompt_depuis_markdown(markdown: str) -> str:
    bloc = re.search(r"##\s*Prompt image[^\n]*\n+```\n(.*?)\n```", markdown, re.S)
    return bloc.group(1).strip() if bloc else ""


def notes_depuis_markdown(markdown: str) -> list[str]:
    """Les points de vigilance de la reprise deviennent les notes du dossier."""
    section = re.search(r"##\s*Points de vigilance(.*?)(?=\n##|\Z)", markdown, re.S)
    if not section:
        return []
    notes = []
    for ligne in section.group(1).splitlines():
        ligne = ligne.strip()
        if re.match(r"^([-*]|\d+\.)\s", ligne):
            notes.append(re.sub(r"^([-*]|\d+\.)\s*", "", ligne))
        elif notes and ligne:
            notes[-1] += " " + ligne
    return notes


def accroche(titre: str) -> str:
    """L'accroche du nom de fichier: le titre jusqu'au deux-points."""
    tete = titre.split(":", 1)[0].strip().lower()
    tete = tete.replace("'", " ").replace("’", " ")
    tete = "".join(c for c in tete if c.isalnum() or c.isspace())
    return re.sub(r"\s+", " ", tete).strip()


def construire(slug: str, racine: str) -> str:
    numero = int(slug.split("-", 1)[0])
    position, titre_canonique, rubrique = CANONIQUE[numero]
    source = os.path.join("pastilles", slug)
    with open(os.path.join(source, "pastille.html"), encoding="utf-8") as handle:
        html = handle.read()
    with open(os.path.join(source, "pastille.md"), encoding="utf-8") as handle:
        markdown = handle.read()

    blocs = cellules_corps(html)
    essentiel = next(json.loads(c) for nature, c in blocs if nature == "essentiel")
    paragraphes = [c for nature, c in blocs if nature == "paragraphe"]
    alt_schema = next(c for nature, c in blocs if nature == "schema")
    legende = next((c for nature, c in blocs if nature == "legende"), "")
    brut_annexe = next((c for nature, c in blocs if nature == "annexe"), None)
    rangs = [i for i, (nature, _) in enumerate(blocs) if nature in ("paragraphe", "schema")]
    schema_apres = [blocs[i][0] for i in rangs].index("schema")

    titre = re.search(r'<img[^>]*alt="([^"]*)"', html)
    fiche = {
        "numero": numero,
        "total": TOTAL_SERIE,
        "position_liste": position,
        "rubrique": rubrique,
        "titre": _html.unescape(titre.group(1)),
        "essentiel": essentiel,
        "paragraphes": paragraphes,
        "schema_apres": schema_apres,
        "legende_schema": legende,
        "alt_schema": alt_schema,
        "image_titre": "illustration-titre.png",
        "image_schema": "schema.png",
        "sources": sources_depuis_markdown(markdown),
        "titre_canonique": titre_canonique,
        "axe": "",
        "prompt_image": prompt_depuis_markdown(markdown),
        "apercu_visuels": "",
        "notes": ["Pastille deja diffusee, reprise au gabarit actuel: le corps du texte est "
                  "inchange, seuls les cadres, les textes alternatifs, les sources et le prompt "
                  "d'images ont ete produits a la reprise."] + notes_depuis_markdown(markdown),
    }
    if brut_annexe:
        label, corps = brut_annexe.split("\n", 1)
        etiquette, style = STYLE_ANNEXE[label]
        fiche["annexe"] = {"etiquette": etiquette, "style": style, "texte": corps}

    dossier = os.path.join(racine, f"pastille-{numero:02d}-{accroche(fiche['titre']).replace(' ', '-')}")
    os.makedirs(dossier, exist_ok=True)
    shutil.copy(os.path.join(source, "image-titre.png"), os.path.join(dossier, "illustration-titre.png"))
    shutil.copy(os.path.join(source, "image-schema.png"), os.path.join(dossier, "schema.png"))
    with open(os.path.join(dossier, "fiche.json"), "w", encoding="utf-8") as handle:
        json.dump(fiche, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return dossier


def main() -> None:
    if sys.argv[1:2] == ["--tous"]:
        racine = sys.argv[2]
        slugs = sorted(s for s in os.listdir("pastilles") if os.path.isdir(os.path.join("pastilles", s)))
    else:
        slugs, racine = [sys.argv[1]], sys.argv[2]
    for slug in slugs:
        dossier = construire(slug, racine)
        with open(os.path.join(dossier, "fiche.json"), encoding="utf-8") as handle:
            fiche = json.load(handle)
        print(f"{dossier}: {len(fiche['paragraphes'])} paragraphes, "
              f"{len(fiche['essentiel'])} puces, schema apres {fiche['schema_apres']}, "
              f"{len(fiche['sources'])} sources, annexe {fiche.get('annexe', {}).get('etiquette', 'ABSENTE')}")


if __name__ == "__main__":
    main()
