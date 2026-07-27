#!/usr/bin/env python3
"""Fabrique le courriel d'une pastille à partir d'une fiche JSON.

    python3 build.py fiche.json --msg pastille-13.msg [--apercu apercu.html]
    python3 build.py --gabarit plugins/pastille-ia/shared/template-pastille.html

Le gabarit de diffusion est produit par le même code que le courriel réel, avec
un contenu de remplacement: il ne peut donc pas prendre du retard sur lui.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import msg as msgfile          # noqa: E402
import render                  # noqa: E402

OBLIGATOIRES = ("numero", "total", "titre", "prefixe_sujet", "essentiel",
                "paragraphes", "legende_schema", "alt_schema", "image_titre",
                "image_schema")

DEFAUTS = {
    "mention_ia": "Cette pastille peut contenir des traces d'IA. En cas de doute, "
                  "demandez à un humain.",
    "signature": "L'Alliance IA",
    "prefixe_sujet": "[Pastille IA de l'été]",
    "total": 45,
}

GABARIT = {
    "numero": "NN", "total": 45, "rubrique": "Rubrique", "temps_lecture": "X min",
    "titre": "Titre exact de la pastille",
    "prefixe_sujet": "[Pastille IA de l'été]",
    "essentiel": ["Puce 1. Une ligne, pas deux.", "Puce 2.",
                  "Puce 3. Trois puces au maximum."],
    "paragraphes": ["Paragraphe 1. 45 à 60 mots, 2 à 3 phrases, **gras** et "
                    "*italique* au format markdown.",
                    "Paragraphe 2. 45 à 60 mots.",
                    "Paragraphe 3. 45 à 60 mots.",
                    "Paragraphe 4, consacré à l'enjeu, lu après le schéma."],
    "schema_apres": 3,
    "legende_schema": "Légende du schéma, une phrase qui dit ce qu'il faut y voir.",
    "alt_schema": "Description du schéma, une phrase.",
    "annexe": {"etiquette": "À essayer", "style": "essayer",
               "texte": "Bloc actionnable facultatif, un seul au maximum: "
                        "À essayer, ou Le piège avec style piege."},
    "image_titre": "illustration-titre.png", "image_schema": "schema.png",
}


def charger(chemin):
    with open(chemin, encoding="utf-8") as f:
        fiche = json.load(f)
    for cle, valeur in DEFAUTS.items():
        fiche.setdefault(cle, valeur)
    manquantes = [c for c in OBLIGATOIRES if c not in fiche]
    if manquantes:
        raise SystemExit("champs manquants dans la fiche: " + ", ".join(manquantes))
    if len(fiche["essentiel"]) > 3:
        raise SystemExit("l'encadré L'essentiel est plafonné à trois puces")
    if not 3 <= len(fiche["paragraphes"]) <= 4:
        raise SystemExit("la pastille compte 3 ou 4 paragraphes")
    # Rubrique et temps de lecture se déduisent, plutôt que d'être réclamés:
    # le numéro de diffusion, lui, ne se déduit de rien.
    if "rubrique" not in fiche:
        position = fiche.get("position_liste")
        if not position:
            raise SystemExit("indiquez rubrique, ou position_liste (place du sujet "
                             "dans la liste des 45) pour la déduire")
        fiche["rubrique"] = render.rubrique_pour(position)
        print(f"rubrique déduite de la position {position}: {fiche['rubrique']}")
    if "temps_lecture" not in fiche:
        fiche["temps_lecture"] = render.temps_lecture(fiche)
        print("temps de lecture calculé:", fiche["temps_lecture"])
    return fiche


def preparer_image(chemin, base):
    """Normalise en PNG opaque: Outlook ne sait pas afficher le webp, et une
    transparence peut ressortir en noir selon le client."""
    donnees = open(chemin, "rb").read()
    if donnees[:8] == b"\x89PNG\r\n\x1a\n":
        try:
            from PIL import Image
            with Image.open(chemin) as im:
                if im.mode in ("RGBA", "LA", "P"):
                    fond = Image.new("RGB", im.size, (255, 255, 255))
                    im = im.convert("RGBA")
                    fond.paste(im, mask=im.split()[3])
                    sortie = os.path.join(os.path.dirname(os.path.abspath(chemin)),
                                          base + ".png")
                    fond.save(sortie, "PNG", optimize=True)
                    return open(sortie, "rb").read()
        except ImportError:
            pass
        return donnees
    try:
        from PIL import Image
    except ImportError:
        raise SystemExit(f"{chemin} n'est pas un PNG et Pillow est absent: "
                         "pip install pillow, ou convertissez l'image à la main")
    with Image.open(chemin) as im:
        sortie = os.path.join(os.path.dirname(os.path.abspath(chemin)), base + ".png")
        im.convert("RGB").save(sortie, "PNG", optimize=True)
    return open(sortie, "rb").read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fiche", nargs="?", help="fiche JSON de la pastille")
    ap.add_argument("--msg", help="chemin du .msg à écrire")
    ap.add_argument("--apercu", help="chemin d'un HTML autonome pour contrôle visuel")
    ap.add_argument("--gabarit", help="régénère le gabarit de diffusion à ce chemin")
    args = ap.parse_args()

    if args.gabarit:
        corps = render.html_pastille({**DEFAUTS, **GABARIT})
        for cid, jeton in (("IMAGE_TITRE", "IMAGE_TITRE"), ("IMAGE_SCHEMA", "IMAGE_SCHEMA")):
            corps = corps.replace(f"cid:{cid}", f"cid:{jeton}")
        with open(args.gabarit, "w", encoding="utf-8") as f:
            f.write(corps)
        print("gabarit écrit:", args.gabarit)
        return

    if not args.fiche or not args.msg:
        raise SystemExit("usage: build.py fiche.json --msg sortie.msg [--apercu a.html]")

    fiche = charger(args.fiche)
    dossier = os.path.dirname(os.path.abspath(args.fiche))
    corps = render.html_pastille(fiche)
    document = render.document_html(fiche, corps)
    texte = render.texte_pastille(fiche)

    images = []
    for cid, cle, base, court in (
            ("IMAGE_TITRE", "image_titre", f'pastille-{fiche["numero"]}-illustration-titre',
             f'P{fiche["numero"]}TITRE.PNG'),
            ("IMAGE_SCHEMA", "image_schema", f'pastille-{fiche["numero"]}-schema',
             f'P{fiche["numero"]}SCHEMA.PNG')):
        chemin = fiche[cle]
        if not os.path.isabs(chemin):
            chemin = os.path.join(dossier, chemin)
        images.append({"cid": cid, "nom": base + ".png", "nom_court": court[:12],
                       "type_mime": "image/png",
                       "donnees": preparer_image(chemin, base)})

    msgfile.ecrire(args.msg, render.sujet(fiche), document, texte, images)
    print("msg écrit:", args.msg, os.path.getsize(args.msg), "octets")
    print("sujet:", render.sujet(fiche))

    if args.apercu:
        apercu = corps
        for img, cle in zip(images, ("image_titre", "image_schema")):
            chemin = fiche[cle]
            if not os.path.isabs(chemin):
                chemin = os.path.join(dossier, chemin)
            apercu = apercu.replace(f'cid:{img["cid"]}', chemin)
        with open(args.apercu, "w", encoding="utf-8") as f:
            f.write(render.document_html(fiche, apercu))
        print("aperçu écrit:", args.apercu)


if __name__ == "__main__":
    main()
