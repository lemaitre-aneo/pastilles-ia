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
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import msg as msgfile          # noqa: E402
import render                  # noqa: E402

OBLIGATOIRES = ("numero", "total", "titre", "essentiel",
                "paragraphes", "legende_schema", "alt_schema")

# Le bloc annexe est systématique dans la série, mais son absence ne bloque pas
# la fabrication: les fiches d'avant cette règle n'en portent pas, et une archive
# ne se prend pas en otage pour un bloc de deux phrases. Le script le signale donc
# et propose de quoi l'écrire, comme il le fait des visuels manquants; c'est au
# skill, qui a le texte sous les yeux, de le rédiger et de le faire valider.
PROPOSITION_ANNEXE = (
    '  à ajouter dans la fiche, une seule des deux lignes, l\'étiquette se déduisant '
    'du style:\n'
    '    "annexe": {"style": "essayer", "texte": "le geste que le lecteur peut faire '
    'aujourd\'hui, prompt à copier ou méthode courte"}\n'
    '    "annexe": {"style": "piege", "texte": "l\'erreur que le sujet rend facile, '
    'et ce qui l\'évite"}\n'
    "  une à deux phrases, cinquante mots au maximum, et rien qui redise l'enjeu "
    "ni les puces")

# Les visuels ne sont obligatoires que pour le courriel. L'archive s'écrit sans
# eux, avec un emplacement décrit à leur place: une pastille peut être conservée
# avant d'être illustrée, et une reprise ancienne les a parfois perdus. Le
# courriel n'a pas cette latitude, le schéma étant systématique dans la série.
VISUELS = ("image_titre", "image_schema")

DEFAUTS = {
    "mention_ia": "Cette pastille peut contenir des traces d'IA. En cas de doute, "
                  "demandez à un humain.",
    "signature": "L'Alliance IA",
    "total": 45,
}

GABARIT = {
    "numero": "NN", "total": 45, "rubrique": "Rubrique", "temps_lecture": "X min",
    "titre": "Titre exact de la pastille",
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
               "texte": "Bloc de clôture, systématique et unique: À essayer pour un "
                        "geste applicable tout de suite, ou Le piège avec style "
                        "piege pour l'erreur que le sujet rend facile."},
    "image_titre": "illustration-titre.png", "image_schema": "schema.png",
}


# Caractères que la spec refuse dans le texte d'une pastille (section
# « Caractères »): typographie importée, ou invisible et donc invérifiable à
# l'œil. Les accents, la cédille et l'e-dans-l'o n'y sont pas et n'y seront
# jamais: ce sont ceux que le français exige, les signaler reviendrait à
# signaler du français correct.
REFUSES = {"—": "un tiret cadratin, à remplacer par une virgule, un deux-points "
                     "ou une parenthèse",
           "–": "un demi-cadratin, même remplacement",
           " ": "une espace fine", " ": "une espace fine insécable",
           "​": "une espace de largeur nulle", "­": "un trait conditionnel"}


def caracteres_refuses(fiche):
    """Les caractères refusés présents dans le texte, avec leur libellé."""
    morceaux = ([fiche["titre"], fiche["legende_schema"], fiche["alt_schema"]]
                + list(fiche["essentiel"]) + list(fiche["paragraphes"])
                + ([fiche["annexe"]["texte"]] if fiche.get("annexe") else []))
    texte = " ".join(morceaux)
    trouves = {nom for c, nom in REFUSES.items() if c in texte}
    # Un accent décomposé se lit comme son équivalent composé mais sort de
    # cp1252, donc devient un « ? » visible dans le sujet du courriel.
    if any(unicodedata.combining(c) for c in texte):
        trouves.add("un accent décomposé (un e suivi d'un diacritique "
                    "combinant, au lieu d'un é)")
    return sorted(trouves)


def controler_annexe(fiche):
    """Le bloc de clôture: signalé s'il manque, contrôlé s'il est là.

    Absent ou vide, il n'arrête rien: le fichier se fabrique sans lui, avec de
    quoi l'écrire. Présent, il tient dans l'une des deux catégories de la série,
    et un style inconnu arrête, lui: ce n'est pas un héritage mais une faute de
    saisie dans un champ qu'on vient d'écrire."""
    annexe = fiche.get("annexe")
    if not annexe or not annexe.get("texte", "").strip():
        print("attention: " + ("bloc annexe vide, donc pas rendu" if annexe else
                               "pas de bloc annexe")
              + ', alors qu\'il ferme systématiquement la pastille (spec, section '
                '"Le bloc annexe"); le fichier est produit sans lui\n'
              + PROPOSITION_ANNEXE)
        fiche.pop("annexe", None)
        return
    style = annexe.get("style", "essayer")
    if style not in render.LIBELLES_ANNEXE:
        raise SystemExit(f"style d'annexe inconnu: {style!r}; la série en compte deux, "
                         + ", ".join(render.LIBELLES_ANNEXE))
    # Le libellé fait partie de la catégorie: on le pose faute de mieux, et on
    # signale toute variante, un libellé inventé cassant le repère de la série.
    attendu = render.LIBELLES_ANNEXE[style]
    annexe.setdefault("etiquette", attendu)
    if annexe["etiquette"] != attendu:
        print(f"attention: étiquette d'annexe {annexe['etiquette']!r} pour le style "
              f"{style!r}; la série écrit {attendu!r}, sans variante")
    mots = len(annexe["texte"].split())
    if mots > 50:
        print(f"attention: le bloc annexe fait {mots} mots (borne 50): c'est une prise "
              "à donner en une ou deux phrases, pas un paragraphe de plus")


def charger(chemin):
    with open(chemin, encoding="utf-8") as f:
        fiche = json.load(f)
    for cle, valeur in DEFAUTS.items():
        fiche.setdefault(cle, valeur)
    # Le préfixe du sujet est une norme de série, pas un réglage de pastille: il
    # vit dans render.PREFIXE_SUJET. Les fiches et les dossiers d'avant le portent
    # encore, on le retire donc ici plutôt que de le réécrire dans le dossier, ce
    # qui le ferait passer pour configurable une fois de plus.
    ancien = fiche.pop("prefixe_sujet", None)
    if ancien is not None and ancien != render.PREFIXE_SUJET:
        print(f"prefixe_sujet ignoré ({ancien!r}): le préfixe de la série n'est pas "
              f"configurable, le sujet portera {render.PREFIXE_SUJET!r}")
    manquantes = [c for c in OBLIGATOIRES if c not in fiche]
    if manquantes:
        raise SystemExit("champs manquants dans la fiche: " + ", ".join(manquantes))
    controler_annexe(fiche)
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
    for refuse in caracteres_refuses(fiche):
        print("attention: le texte porte", refuse)
    if fiche["alt_schema"].strip() == fiche["legende_schema"].strip():
        print("attention: alt_schema reprend la légende mot pour mot; l'alt doit "
              "dire ce que le schéma montre, sa structure et ses libellés, là où la "
              "légende dit ce qu'il faut en retenir")
    # La rubrique suit l'axe traité et le contenu, elle ne se calcule pas: elle est
    # donc écrite dans la fiche dès qu'elle a été arbitrée, et seulement contrôlée
    # ici. Faute de mieux, on retombe sur le classement d'inventaire, en disant que
    # c'en est un: c'est le cas où une pastille dont l'axe a bougé se retrouve
    # rangée d'après un sujet qu'elle ne traite plus.
    if "rubrique" in fiche:
        if fiche["rubrique"] not in render.RUBRIQUES_CONNUES:
            raise SystemExit(f"rubrique inconnue: {fiche['rubrique']!r}; la série en "
                             "compte six, " + ", ".join(render.RUBRIQUES_CONNUES))
    else:
        position = fiche.get("position_liste")
        if not position:
            raise SystemExit("indiquez rubrique (celle décidée sur l'axe et le "
                             "contenu), ou position_liste (place du sujet dans la "
                             "liste des 45) pour retomber sur le classement "
                             "d'inventaire")
        fiche["rubrique"] = render.rubrique_pour(position)
        print(f"rubrique absente de la fiche: classement d'inventaire de la position "
              f"{position} retenu par défaut, {fiche['rubrique']}"
              "\n  (la rubrique suit l'axe et le contenu: vérifiez qu'elle "
              "correspond encore à ce que la pastille dit)")
    # Le temps de lecture, lui, se déduit vraiment. Le numéro de diffusion, jamais.
    if "temps_lecture" not in fiche:
        fiche["temps_lecture"] = render.temps_lecture(fiche)
        print("temps de lecture calculé:", fiche["temps_lecture"])
    return fiche


TOLERANCE_BLANC = 6      # un pixel plus clair que ça compte comme fond
MARGE_CONSERVEE = 16     # respiration gardée autour du contenu, en pixels source
BANDE_MINIMALE = 0.02    # en deçà, la bande ne vaut pas un rognage
ROGNAGE_MAXIMAL = 0.60   # au-delà, on suspecte une fausse détection et on s'abstient


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

    # Un courriel sans schéma n'est pas conforme à la série, et l'illustration
    # porte le titre: on refuse donc de le fabriquer plutôt que de livrer un
    # visuel manquant à des destinataires. L'archive, elle, sait attendre.
    absents = [c for c in VISUELS if not fiche.get(c)]
    if args.msg and absents:
        raise SystemExit(
            "le courriel exige les deux visuels, or " + ", ".join(absents)
            + " manque(nt) à la fiche: le schéma est systématique dans la série. "
            "Générez les visuels, ou produisez l'archive seule en attendant, avec "
            "--html et sans --msg.")

    images = []
    for cid, cle, base, court in (
            ("IMAGE_TITRE", "image_titre", f'pastille-{fiche["numero"]}-illustration-titre',
             f'P{fiche["numero"]}TITRE.PNG'),
            ("IMAGE_SCHEMA", "image_schema", f'pastille-{fiche["numero"]}-schema',
             f'P{fiche["numero"]}SCHEMA.PNG')):
        chemin = fiche.get(cle)
        if not chemin:
            continue
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
        # Par cid et non par position: un visuel peut manquer, et c'est alors le
        # second qui glisserait à la place du premier.
        sources = dict(zip((img["cid"] for img in images), sources_data(images)))
        with open(args.html, "w", encoding="utf-8") as f:
            f.write(render.html_plat_pastille(fiche, sources.get("IMAGE_TITRE"),
                                              sources.get("IMAGE_SCHEMA")))
        print("html écrit:", args.html, os.path.getsize(args.html), "octets")
        if absents:
            print("  archive provisoire:", ", ".join(absents), "absent(s) de la "
                  "fiche, l'artefact porte à leur place un emplacement décrit")
            print("  (refabriquez-la une fois les visuels générés; le courriel, "
                  "lui, ne peut pas être produit d'ici là)")
        rappeler_nom(args.html, ".html")
        alerter_taille(args.html)
        # Le dossier incorporé est ce qui fait de cet artefact la référence pour
        # reprendre la pastille: on vérifie tout de suite qu'il se relit.
        try:
            render.lire_dossier(open(args.html, encoding="utf-8").read())
        except ValueError as erreur:
            raise SystemExit(f"dossier incorporé illisible: {erreur}")
        absents_reprise = [c for c in ("titre_canonique", "axe", "prompt_image",
                                       "apercu_visuels", "sources")
                           if not fiche.get(c)]
        if absents_reprise:
            print("  dossier incomplet, champs absents:", ", ".join(absents_reprise),
                  "\n  (une reprise ultérieure devra les redemander)")


if __name__ == "__main__":
    main()
