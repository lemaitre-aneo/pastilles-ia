#!/usr/bin/env python3
"""Fabrique le courriel d'une pastille à partir d'une fiche JSON.

    python3 build.py fiche.json --msg "pastille 13 les tokens.msg" \
                     --html "pastille 13 les tokens.html"
    python3 build.py --gabarit plugins/pastille-ia/shared/template-pastille.html

Le gabarit de diffusion est produit par le même code que le courriel réel, avec
un contenu de remplacement: il ne peut donc pas prendre du retard sur lui.
"""
import argparse
import base64
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
    for i, puce in enumerate(fiche["essentiel"], 1):
        mots, signes = len(puce.split()), len(puce)
        if mots > 12 or signes > 70:
            print(f"attention: puce {i} de L'essentiel, {mots} mots et {signes} signes "
                  "(borne 12 mots, 70 signes): elle passera sur deux lignes en volet "
                  "étroit, et porte peut-être deux idées")
    if not 3 <= len(fiche["paragraphes"]) <= 4:
        raise SystemExit("la pastille compte 3 ou 4 paragraphes")
    # L'alt et la légende ne font pas le même travail: l'alt décrit ce qui est
    # dessiné, pour qui ne voit pas l'image, la légende dit ce qu'il faut en
    # retenir. Recopier l'une dans l'autre prive le lecteur d'écran du contenu du
    # schéma, le seul visuel de la pastille qui porte de l'information.
    if fiche["alt_schema"].strip() == fiche["legende_schema"].strip():
        print("attention: alt_schema reprend la légende mot pour mot; l'alt doit "
              "dire ce que le schéma montre, sa structure et ses libellés, là où la "
              "légende dit ce qu'il faut en retenir")
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


TOLERANCE_BLANC = 6      # un pixel plus clair que ça compte comme fond
MARGE_CONSERVEE = 16     # respiration gardée autour du contenu, en pixels source
BANDE_MINIMALE = 0.02    # en deçà, la bande ne vaut pas un rognage
ROGNAGE_MAXIMAL = 0.60   # au delà, on suspecte une fausse détection et on s'abstient


def mesurer_marges(im):
    """Bandes de fond quasi blanc autour du contenu: (gauche, haut, droite, bas).

    Renvoie aussi la boîte du contenu. None si l'image est entièrement blanche,
    cas où il n'y a rien à mesurer."""
    from PIL import Image, ImageChops
    rgb = im.convert("RGB")
    fond = Image.new("RGB", rgb.size, (255, 255, 255))
    ecart = ImageChops.difference(rgb, fond).convert("L")
    boite = ecart.point(lambda v: 255 if v > TOLERANCE_BLANC else 0).getbbox()
    if boite is None:
        return None, None
    marges = (boite[0], boite[1], im.width - boite[2], im.height - boite[3])
    return marges, boite


def rogner_marges(im, etiquette):
    """Retire les bandes de fond, en gardant une respiration.

    Le rognage se fait ici plutôt que dans le client de messagerie: rogner une
    image dans Outlook réécrit ses dimensions en dur et emporte le max-width,
    ce qui donne au bloc une largeur minimale qu'il ne sait plus réduire."""
    marges, boite = mesurer_marges(im)
    if marges is None:
        print(f"attention: {etiquette} semble entièrement blanche, pas de rognage")
        return im
    seuils = (im.width * BANDE_MINIMALE, im.height * BANDE_MINIMALE) * 2
    if not any(m > s for m, s in zip(marges, seuils)):
        return im

    boite = (max(0, boite[0] - MARGE_CONSERVEE), max(0, boite[1] - MARGE_CONSERVEE),
             min(im.width, boite[2] + MARGE_CONSERVEE),
             min(im.height, boite[3] + MARGE_CONSERVEE))
    aire = (boite[2] - boite[0]) * (boite[3] - boite[1])
    if aire < (1 - ROGNAGE_MAXIMAL) * im.width * im.height:
        print(f"attention: {etiquette}, le rognage retirerait plus de "
              f"{int(ROGNAGE_MAXIMAL * 100)}% de l'image, abstention: vérifiez le "
              "visuel, ou rognez-le à la main avant de reconstruire")
        return im

    rogne = im.crop(boite)
    cotes = ", ".join(f"{nom} {int(m)} px" for nom, m in
                      zip(("gauche", "haut", "droite", "bas"), marges) if m > 1)
    print(f"{etiquette}: bandes de fond rognées ({cotes}), "
          f"{im.width}x{im.height} -> {rogne.width}x{rogne.height}")
    return rogne


def preparer_image(chemin, base, rognage=True):
    """Normalise en PNG opaque, retire les bandes de fond, renvoie le chemin écrit.

    Outlook ne sait pas afficher le webp, et une transparence peut ressortir en
    noir selon le client. Le fichier produit est celui que porte le courriel:
    c'est donc lui que les artefacts affichent et que la vérification compare."""
    etiquette = os.path.basename(chemin)
    try:
        from PIL import Image
    except ImportError:
        with open(chemin, "rb") as f:
            entete = f.read(8)
        if entete == b"\x89PNG\r\n\x1a\n":
            print(f"attention: Pillow est absent, {etiquette} est reprise telle "
                  "quelle, sans rognage des bandes de fond (pip install pillow)")
            return os.path.abspath(chemin)
        raise SystemExit(f"{chemin} n'est pas un PNG et Pillow est absent: "
                         "pip install pillow, ou convertissez l'image à la main")

    with Image.open(chemin) as source:
        im = source
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            aplat = Image.new("RGB", im.size, (255, 255, 255))
            aplat.paste(im, mask=im.split()[3])
            im = aplat
        else:
            im = im.convert("RGB")
        if rognage:
            im = rogner_marges(im, etiquette)
        else:
            marges, _ = mesurer_marges(im)
            seuils = (im.width * BANDE_MINIMALE, im.height * BANDE_MINIMALE) * 2
            if marges and any(m > s for m, s in zip(marges, seuils)):
                print(f"{etiquette}: bandes de fond détectées, rognage désactivé. "
                      "Ne les rognez pas dans Outlook, cela fige la largeur de "
                      "l'image et le bloc ne sait plus se réduire")
        sortie = os.path.join(os.path.dirname(os.path.abspath(chemin)), base + ".png")
        im.save(sortie, "PNG", optimize=True)
    return sortie


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fiche", nargs="?", help="fiche JSON de la pastille")
    ap.add_argument("--msg", help="chemin du .msg à écrire")
    ap.add_argument("--html", help="chemin de l'artefact conservé: HTML sémantique "
                                   "aux teintes de la série, visuels incorporés, "
                                   "importable dans Notion tel quel")
    ap.add_argument("--gabarit", help="régénère le gabarit de diffusion à ce chemin")
    ap.add_argument("--sans-rognage", action="store_true",
                    help="conserve les bandes de fond des visuels, au lieu de les "
                         "retirer; les bandes détectées sont alors seulement signalées")
    args = ap.parse_args()

    if args.gabarit:
        corps = render.html_pastille({**DEFAUTS, **GABARIT})
        for cid, jeton in (("IMAGE_TITRE", "IMAGE_TITRE"), ("IMAGE_SCHEMA", "IMAGE_SCHEMA")):
            corps = corps.replace(f"cid:{cid}", f"cid:{jeton}")
        with open(args.gabarit, "w", encoding="utf-8") as f:
            f.write(corps)
        print("gabarit écrit:", args.gabarit)
        return

    # Le courriel n'est pas toujours demandé: archiver une pastille et la diffuser
    # sont deux gestes distincts, et une reprise qui ne sera pas rediffusée n'a
    # aucune raison de fabriquer un .msg que personne n'enverra. L'un des deux
    # chemins de sortie suffit donc.
    if not args.fiche or not (args.msg or args.html):
        raise SystemExit('usage: build.py fiche.json --msg "pastille NN accroche.msg" '
                         '[--html "pastille NN accroche.html"]\n'
                         '       build.py fiche.json --html "pastille NN accroche.html"'
                         '   (archive seule, sans courriel)')

    fiche = charger(args.fiche)
    dossier = os.path.dirname(os.path.abspath(args.fiche))

    images = []
    for cid, cle, base, court in (
            ("IMAGE_TITRE", "image_titre", f'pastille-{fiche["numero"]}-illustration-titre',
             f'P{fiche["numero"]}TITRE.PNG'),
            ("IMAGE_SCHEMA", "image_schema", f'pastille-{fiche["numero"]}-schema',
             f'P{fiche["numero"]}SCHEMA.PNG')):
        chemin = fiche[cle]
        if not os.path.isabs(chemin):
            chemin = os.path.join(dossier, chemin)
        produit = preparer_image(chemin, base, rognage=not args.sans_rognage)
        images.append({"cid": cid, "nom": base + ".png", "nom_court": court[:12],
                       "type_mime": "image/png", "fichier": produit,
                       "donnees": open(produit, "rb").read()})

    # Les deux fichiers portent le même nom, à l'extension près: l'accroche les
    # rend reconnaissables dans un dossier, et côté HTML c'est le nom du fichier
    # qui nomme la page importée, Notion ne lisant pas le h1 du document.
    def rappeler_nom(chemin, extension):
        attendu = render.limace(fiche["titre"], fiche["numero"]) + extension
        if chemin and os.path.basename(chemin) != attendu:
            print(f'  à renommer en "{attendu}"'
                  + (": c'est le nom du fichier qui nomme la page importée"
                     if extension == ".html" else ""))

    if args.msg:
        corps = render.html_pastille(fiche)
        document = render.document_html(fiche, corps)
        texte = render.texte_pastille(fiche)
        objet = render.sujet(fiche)
        msgfile.ecrire(args.msg, objet, document, texte, images)
        print("msg écrit:", args.msg, os.path.getsize(args.msg), "octets")
        print("sujet:", objet)

        # Un objet entièrement décodable dans un codage sur deux octets sera
        # affiché de travers: on le signale ici, à la fabrication, plutôt que de
        # le découvrir dans la boîte de réception. C'est au préfixe de série de
        # porter la rupture qui l'évite, puisqu'il est sur tous les courriels.
        ambigus = dict(render.objet_ambigu(objet))
        if render.CODAGE_CONSTATE in ambigus:
            print(f"  ALERTE objet ambigu ({render.CODAGE_CONSTATE}): Outlook (new) "
                  "affichera")
            print("   ", ambigus[render.CODAGE_CONSTATE])
            print("    la rupture d'encodage entre le préfixe et le numéro a sauté")
        hors = render.hors_cp1252(objet)
        if hors:
            print("  ALERTE l'objet porte",
                  ", ".join(f"U+{ord(c):04X}" for c in hors),
                  "hors cp1252: un client qui rabat l'objet en octets les remplacera "
                  "par des « ? » visibles")

        rappeler_nom(args.msg, ".msg")

    def sources_data(images):
        return [f'data:{img["type_mime"]};base64,'
                f'{base64.b64encode(img["donnees"]).decode("ascii")}' for img in images]

    def alerter_taille(chemin):
        # Notion plafonne l'import à 5 Mo sur le plan gratuit, 50 Mo sinon, et le
        # base64 gonfle les visuels d'un tiers: un fichier autonome peut donc
        # passer la limite sans que personne ne l'ait vu venir.
        mo = os.path.getsize(chemin) / 1_048_576
        if mo > 4.5:
            print(f"attention: {chemin} pèse {mo:.1f} Mo, au-delà de la limite "
                  "d'import de 5 Mo du plan gratuit de Notion")

    if args.html:
        sources = sources_data(images)
        with open(args.html, "w", encoding="utf-8") as f:
            f.write(render.html_plat_pastille(fiche, sources[0], sources[1]))
        print("html écrit:", args.html, os.path.getsize(args.html), "octets")
        rappeler_nom(args.html, ".html")
        alerter_taille(args.html)
        # Le dossier incorporé est ce qui fait de cet artefact la référence pour
        # reprendre la pastille: on vérifie tout de suite qu'il se relit.
        try:
            render.lire_dossier(open(args.html, encoding="utf-8").read())
        except ValueError as erreur:
            raise SystemExit(f"dossier incorporé illisible: {erreur}")
        absents = [c for c in ("titre_canonique", "axe", "prompt_image",
                               "apercu_visuels", "sources")
                   if not fiche.get(c)]
        if absents:
            print("  dossier incomplet, champs absents:", ", ".join(absents),
                  "\n  (une reprise ultérieure devra les redemander)")


if __name__ == "__main__":
    main()
