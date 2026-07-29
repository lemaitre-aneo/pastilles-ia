#!/usr/bin/env python3
"""Rouvre l'artefact HTML d'une pastille et en ressort son dossier complet.

    python3 dossier.py "pastille 13 les tokens.html" [--dossier repertoire]

Sans `--dossier`, affiche le dossier en JSON sur la sortie standard, ce qui
suffit pour lire un prompt d'images, un axe ou des sources.

Avec `--dossier`, écrit dans ce répertoire une fiche `fiche.json` et les deux
visuels extraits du fichier: de quoi refabriquer le courriel et l'artefact avec
`build.py`, sans rien redemander ni reconstituer.

C'est ce qui fait de l'artefact HTML la référence pour reprendre une pastille:
il porte à la fois ce qui se lit (le texte mis en forme), ce qui se voit (les
visuels en base64) et ce qui se retravaille (la fiche, le prompt d'images, le
titre canonique, l'axe, les sources, les notes d'échange).
"""
import argparse
import base64
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render                     # noqa: E402


def visuels(html):
    """Les deux images incorporées, dans l'ordre du document."""
    trouves = re.findall(r'<img src="data:image/([a-z]+);base64,([^"]+)"', html)
    if len(trouves) != 2:
        raise SystemExit(f"{len(trouves)} image(s) incorporée(s) au lieu de 2: "
                         "cet artefact n'est pas complet")
    return [(ext, base64.b64decode(donnees)) for ext, donnees in trouves]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html", help="artefact HTML d'une pastille")
    ap.add_argument("--dossier", help="répertoire où écrire la fiche et les visuels")
    args = ap.parse_args()

    with open(args.html, encoding="utf-8") as f:
        html = f.read()
    try:
        fiche = render.lire_dossier(html)
    except ValueError as erreur:
        raise SystemExit(f"{args.html}: {erreur}. Un artefact produit avant "
                         "l'introduction du dossier ne peut pas être relu ainsi: "
                         "il faut repartir du texte affiché.")

    if not args.dossier:
        json.dump(fiche, sys.stdout, ensure_ascii=False, indent=1)
        print()
        return

    os.makedirs(args.dossier, exist_ok=True)
    images = visuels(html)
    noms = []
    for (ext, donnees), cle in zip(images, ("image_titre", "image_schema")):
        base = "illustration-titre" if cle == "image_titre" else "schema"
        nom = f'pastille-{fiche.get("numero", "NN")}-{base}.{ext}'
        with open(os.path.join(args.dossier, nom), "wb") as f:
            f.write(donnees)
        noms.append(nom)
        print("visuel écrit:", nom, len(donnees), "octets")

    fiche["image_titre"], fiche["image_schema"] = noms
    fiche.pop("_format", None)
    chemin = os.path.join(args.dossier, "fiche.json")
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(fiche, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("fiche écrite:", chemin)
    manquants = [c for c in ("titre_canonique", "axe", "prompt_image", "sources")
                 if not fiche.get(c)]
    if manquants:
        print("absents du dossier:", ", ".join(manquants),
              "\n  (l'artefact a été fabriqué sans eux; demande-les si la retouche "
              "en dépend)")


if __name__ == "__main__":
    main()
