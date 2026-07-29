#!/usr/bin/env python3
"""Rouvre l'artefact HTML d'une pastille et en ressort son dossier complet.

    python3 dossier.py "pastille 13 les tokens.html" [--dossier repertoire]

Sans `--dossier`, affiche le dossier en JSON sur la sortie standard, ce qui
suffit pour lire un prompt d'images, un axe ou des sources.

Avec `--dossier`, écrit dans ce répertoire une fiche `fiche.json` et les visuels
extraits du fichier: de quoi refabriquer le courriel et l'artefact avec
`build.py`, sans rien redemander ni reconstituer. Une archive provisoire, faite
avant que les visuels existent, en porte moins de deux: la fiche ressort alors
sans le champ correspondant, ce qui suffit à refabriquer l'archive mais pas le
courriel.

C'est ce qui fait de l'artefact HTML la référence pour reprendre une pastille:
il porte à la fois ce qui se lit (le texte mis en forme), ce qui se voit (les
visuels en base64) et ce qui se retravaille (la fiche, le prompt d'images et
l'aperçu de ce qu'ils montrent, le titre canonique, l'axe, les sources, les
notes d'échange).
"""
import argparse
import base64
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render                     # noqa: E402


def visuels(html, declares):
    """Les images incorporées, appariées aux visuels que le dossier déclare.

    Une archive peut être provisoire et n'en porter qu'une, ou aucune, quand la
    pastille a été conservée avant d'être illustrée. On apparie donc les images
    trouvées aux champs déclarés dans le dossier, dans l'ordre du document
    (illustration puis schéma), et jamais à une position supposée: sur une
    archive sans illustration, la première image du document est le schéma.
    """
    trouves = re.findall(r'<img src="data:image/([a-z]+);base64,([^"]+)"', html)
    if len(trouves) != len(declares):
        raise SystemExit(f"{len(trouves)} image(s) incorporée(s) pour "
                         f"{len(declares)} déclarée(s) dans le dossier: cet "
                         "artefact est incohérent")
    return [(cle, ext, base64.b64decode(donnees))
            for cle, (ext, donnees) in zip(declares, trouves)]


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
    declares = [c for c in ("image_titre", "image_schema") if fiche.get(c)]
    for cle, ext, donnees in visuels(html, declares):
        base = "illustration-titre" if cle == "image_titre" else "schema"
        nom = f'pastille-{fiche.get("numero", "NN")}-{base}.{ext}'
        with open(os.path.join(args.dossier, nom), "wb") as f:
            f.write(donnees)
        fiche[cle] = nom
        print("visuel écrit:", nom, len(donnees), "octets")

    # Une archive provisoire ne porte pas tous ses visuels: la fiche ressort donc
    # sans le champ correspondant, ce qui suffit à refabriquer l'archive mais pas
    # le courriel. Il vaut mieux le dire ici que de le découvrir dans build.py.
    if len(declares) < 2:
        print("archive provisoire:",
              ", ".join(c for c in ("image_titre", "image_schema")
                        if c not in declares),
              "absent(s) de l'artefact",
              "\n  (générez le ou les visuels avant toute diffusion, le courriel "
              "exige les deux)")
    fiche.pop("_format", None)
    chemin = os.path.join(args.dossier, "fiche.json")
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(fiche, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("fiche écrite:", chemin)
    manquants = [c for c in ("titre_canonique", "axe", "prompt_image",
                             "apercu_visuels", "sources")
                 if not fiche.get(c)]
    if manquants:
        print("absents du dossier:", ", ".join(manquants),
              "\n  (l'artefact a été fabriqué sans eux; demande-les si la retouche "
              "en dépend)")


if __name__ == "__main__":
    main()
