#!/usr/bin/env python3
"""Contrôle un .msg fabriqué: structure, propriétés, pièces jointes, typographie.

    python3 verify.py pastille-13.msg [image-titre.png image-schema.png]
                      [--html "pastille 13 les tokens.html"]

Un parseur indépendant (olefile) rouvre le fichier: c'est le seul moyen de
vérifier le conteneur sans Outlook. Le rendu visuel, lui, se contrôle avec
l'artefact HTML et un navigateur.
"""
import hashlib
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render                     # noqa: E402

try:
    import olefile
except ImportError:
    raise SystemExit("olefile est requis: pip install olefile")


def lire(ole, chemin):
    return ole.openstream(chemin).read()


def proprietes(ole, chemin, taille_entete):
    corps = lire(ole, chemin)[taille_entete:]
    table = {}
    for i in range(0, len(corps) - 15, 16):
        tag, _, = struct.unpack("<II", corps[i:i + 8])
        table[tag] = corps[i + 8:i + 16]
    return table


def controler_artefact(chemin, problemes):
    """L'artefact conservé ne passe pas par Outlook, mais il a ses propres règles:
    il doit se suffire à lui-même (sinon il n'est ni archivable ni importable
    seul) et rester sans mise en page en tables (sinon un importeur l'aplatit)."""
    print("\nHTML conservé")
    corps = open(chemin, encoding="utf-8").read()
    sources = re.findall(r'<img src="([^"]+)"', corps)
    incorporees = sum(s.startswith("data:image/") for s in sources)
    tables = len(re.findall(r"<table", corps, re.I))
    print("  images incorporées         :", incorporees)
    print("  tables                     :", tables, "(1 attendue: le bandeau)")
    if incorporees != len(sources) or incorporees != 2:
        problemes.append(f"{chemin}: {incorporees} image(s) incorporée(s) sur "
                         f"{len(sources)} au lieu de 2; le fichier doit se suffire "
                         "à lui-même")
    if "cid:" in corps:
        problemes.append(f"{chemin}: références cid: restantes, elles ne "
                         "s'affichent que dans un client de messagerie")
    # Une table simple s'importe comme une table, ce qui est voulu pour le
    # bandeau. Ce qu'un importeur aplatit mal, ce sont les tables de mise en
    # page, imbriquées: c'est cela qu'on refuse, pas la table en soi.
    if tables > 1:
        problemes.append(f"{chemin}: {tables} tables; seul le bandeau en justifie "
                         "une, au-delà c'est de la mise en page, et c'est ce qu'un "
                         "importeur aplatit mal")
    if re.search(r"<table[^>]*>(?:(?!</table>).)*<table", corps, re.I | re.S):
        problemes.append(f"{chemin}: table imbriquée; le bandeau doit rester une "
                         "table simple, une ligne et trois cellules")
    # Sans son dossier, l'artefact se lit encore mais ne se reprend plus: il
    # cesse d'être la référence pour retravailler la pastille.
    try:
        dossier = render.lire_dossier(corps)
        champs = [c for c in ("titre", "paragraphes", "essentiel") if c in dossier]
        print("  dossier incorporé          : relu,", len(dossier), "champs")
        if len(champs) < 3:
            problemes.append(f"{chemin}: dossier incomplet, il manque le texte même "
                             "de la pastille")
        absents = [c for c in ("titre_canonique", "axe", "prompt_image", "sources")
                   if not dossier.get(c)]
        if absents:
            print("    champs de reprise absents :", ", ".join(absents))
    except ValueError as erreur:
        problemes.append(f"{chemin}: {erreur}; l'artefact ne pourra pas servir de "
                         "référence pour reprendre la pastille")


def main():
    argv = sys.argv[1:]
    # Attention au nom: `html` désigne plus bas le corps HTML lu dans le .msg.
    artefact = None
    if "--html" in argv:
        i = argv.index("--html")
        artefact = argv[i + 1] if i + 1 < len(argv) else None
        if not artefact:
            raise SystemExit("--html attend un chemin")
        del argv[i:i + 2]
    if not argv:
        raise SystemExit('usage: verify.py fichier.msg [sources d\'images...] '
                         '[--html "pastille NN accroche.html"]')
    chemin = argv[0]
    sources = argv[1:]
    if not olefile.isOleFile(chemin):
        raise SystemExit("ce fichier n'est pas un conteneur OLE valide")
    ole = olefile.OleFileIO(chemin)
    problemes = []

    entete = lire(ole, "__properties_version1.0")[:32]
    _, _, destinataires, pieces = struct.unpack("<IIII", entete[8:24])
    sujet = lire(ole, "__substg1.0_0037001F").decode("utf-16-le")
    html = lire(ole, "__substg1.0_10130102").decode("utf-8")
    texte = lire(ole, "__substg1.0_1000001F").decode("utf-16-le")
    haut = proprietes(ole, "__properties_version1.0", 32)

    print("conteneur OLE      : valide")
    print("sujet              :", sujet)
    print("destinataires      :", destinataires, "(0 attendu pour un brouillon)")
    print("pièces jointes     :", pieces)
    print("corps HTML         :", len(html), "octets")
    print("corps texte        :", len(texte), "caractères")
    for pid, nom, attendu in ((0x5909, "MessageEditorFormat", 2),
                              (0x0E07, "MessageFlags", 9),
                              (0x340D, "StoreSupportMask", 0x00040000),
                              (0x3FDE, "InternetCodepage", 65001)):
        valeur = struct.unpack("<i", haut[(pid << 16) | 0x0003][:4])[0]
        print(f"{nom:19}:", valeur)
        if valeur != attendu:
            problemes.append(f"{nom} vaut {valeur}, attendu {attendu}")

    print("\ncontraintes de rendu Word")
    quotes = html.count("'Segoe")
    print("  polices entre apostrophes  :", quotes)
    if quotes:
        problemes.append("un nom de police est entre apostrophes: Word jettera la "
                         "fin de la déclaration")
    inverses = [d for d in re.findall(r'style="([^"]*)"', html)
                if "color:" in d and "font-family" in d
                and d.index("font-family") < d.index("color:")]
    print("  font-family avant color    :", len(inverses))
    if inverses:
        problemes.append(f"{len(inverses)} déclarations placent font-family avant color")
    cellules = [t for t in re.findall(r"<td[^>]*>", html)
                if re.search(r"(?<!background-)color:#", t)]
    print("  couleur portée par un <td>  :", len(cellules))
    if cellules:
        problemes.append(f"{len(cellules)} cellules portent une couleur de texte, "
                         "que Word n'hérite pas")
    # Word ne peint pas un fond de table: chaque table colorée doit avoir une
    # cellule colorée juste derrière, sinon le bloc ressort blanc dans Outlook.
    orphelines = [m.group(1) for m in re.finditer(
        r'<table[^>]*bgcolor="(#[0-9A-Fa-f]{6})"[^>]*>\s*<tr>\s*(<td[^>]*>)', html)
        if "bgcolor" not in m.group(2) and m.group(1).upper() != "#FFFFFF"]
    print("  fond de table sans fond de cellule:", len(orphelines))
    if orphelines:
        problemes.append(f"{len(orphelines)} blocs colorés ne posent leur fond que "
                         "sur la table: Word les affichera en blanc")
    print("  balises <font color>       :", html.count("<font color="))

    print("\ntypographie")
    droites = len(re.findall(r">[^<]*'[^<]*<", html))
    print("  apostrophes droites        :", droites)
    if droites:
        problemes.append(f"{droites} apostrophes droites dans le texte visible")
    print("  espaces insécables         :", len(re.findall(r"&(?:nbsp|#160);[;:!?]", html)))

    print("\npièces jointes")
    empreintes = {hashlib.sha256(open(s, "rb").read()).hexdigest(): s for s in sources}
    for i in range(pieces):
        st = f"__attach_version1.0_#{i:08X}"
        cid = lire(ole, f"{st}/__substg1.0_3712001F").decode("utf-16-le")
        nom = lire(ole, f"{st}/__substg1.0_3707001F").decode("utf-16-le")
        data = lire(ole, f"{st}/__substg1.0_37010102")
        pj = proprietes(ole, f"{st}/__properties_version1.0", 8)
        drapeaux = struct.unpack("<i", pj[(0x3714 << 16) | 0x0003][:4])[0]
        png = data[:8] == b"\x89PNG\r\n\x1a\n"
        source = empreintes.get(hashlib.sha256(data).hexdigest())
        print(f"  {nom}  cid={cid}  {len(data)} octets  PNG={png}  AttachFlags={drapeaux}")
        if sources:
            print("    identique à la source :", source or "NON, aucune source ne correspond")
            if not source:
                problemes.append(f"{nom} ne correspond à aucune source fournie")
        if f"cid:{cid}" not in html:
            problemes.append(f"le cid {cid} n'est pas référencé dans le corps")
        if not png:
            problemes.append(f"{nom} n'est pas un PNG")
        if drapeaux != 4:
            problemes.append(f"{nom}: AttachFlags devrait valoir 4 (ATT_MHTML_REF)")
    ole.close()

    if artefact:
        controler_artefact(artefact, problemes)

    print()
    if problemes:
        print("PROBLÈMES")
        for p in problemes:
            print(" -", p)
        sys.exit(1)
    print("aucun problème détecté")


if __name__ == "__main__":
    main()
