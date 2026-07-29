#!/usr/bin/env python3
"""Contrôle un .msg fabriqué: structure, propriétés, pièces jointes, typographie.

    python3 verify.py pastille-13.msg [image-titre.png image-schema.png]
                      [--html courriel.html] [--markdown pastille.md]
                      [--html-plat pastille-notion.html]
                      [--html-plat-autonome pastille-plat-autonome.html]

Un parseur indépendant (olefile) rouvre le fichier: c'est le seul moyen de
vérifier le conteneur sans Outlook. Le rendu visuel, lui, se contrôle avec
le HTML autonome et un navigateur.
"""
import hashlib
import os
import re
import struct
import sys

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


def images_voisines(chemin, cites, problemes, quoi):
    """Un artefact d'import ne trouve ses images que si elles sont à côté de lui,
    citées par leur seul nom: c'est la condition que Notion documente."""
    voisin = os.path.dirname(os.path.abspath(chemin))
    courts = [n if len(n) <= 60 else n[:57] + "..." for n in cites]
    print("  images citées              :", ", ".join(courts) or "aucune")
    if len(cites) != 2:
        problemes.append(f"{chemin}: {len(cites)} image(s) citée(s) au lieu de 2")
    for nom, court in zip(cites, courts):
        if os.path.dirname(nom):
            problemes.append(f"{chemin}: {court} porte un chemin; {quoi} importe "
                             "les images voisines, pas celles d'un autre dossier")
        elif not os.path.exists(os.path.join(voisin, nom)):
            problemes.append(f"{chemin}: {court} est cité mais absent du dossier")


def controler_artefacts(html_archive, markdown, html_plat, html_plat_autonome,
                        problemes):
    """Les artefacts conservés ne passent pas par Outlook, mais ils ont leurs
    propres règles: le HTML doit se suffire à lui-même (sinon il n'est pas
    archivable) et le Markdown doit trouver ses images à côté de lui (sinon
    l'import Notion arrive sans visuels)."""
    if html_archive:
        print("\nHTML d'archive")
        corps = open(html_archive, encoding="utf-8").read()
        incorporees = corps.count('src="data:image/png;base64,')
        residus = corps.count("cid:")
        print("  images incorporées         :", incorporees)
        print("  références cid: restantes  :", residus)
        if incorporees != 2:
            problemes.append(f"{html_archive}: {incorporees} image(s) incorporée(s) "
                             "au lieu de 2, le fichier n'est pas autonome")
        if residus:
            problemes.append(f"{html_archive}: {residus} référence(s) cid: restantes, "
                             "elles ne s'affichent que dans un client de messagerie")

    if markdown:
        print("\nMarkdown d'archive")
        corps = open(markdown, encoding="utf-8").read()
        images_voisines(markdown, re.findall(r"!\[[^\]]*\]\(([^)]+)\)", corps),
                        problemes, "Notion")

    for chemin, autonome in ((html_plat, False), (html_plat_autonome, True)):
        if not chemin:
            continue
        print("\nHTML aplati" + (" autonome" if autonome else " (images voisines)"))
        corps = open(chemin, encoding="utf-8").read()
        tables = len(re.findall(r"<table", corps, re.I))
        sources = re.findall(r'<img src="([^"]+)"', corps)
        print("  tables                     :", tables, "(1 attendue: le bandeau)")
        # Une table simple s'importe comme une table, ce qui est voulu pour le
        # bandeau. Ce qu'un importeur aplatit mal, ce sont les tables de mise en
        # page, imbriquées: c'est cela qu'on refuse, pas la table en soi.
        if tables > 1:
            problemes.append(f"{chemin}: {tables} tables; seul le bandeau en justifie "
                             "une, au-delà c'est de la mise en page, et c'est ce qu'un "
                             "importeur aplatit mal")
        if re.search(r"<table[^>]*>(?:(?!</table>).)*<table", corps, re.I | re.S):
            problemes.append(f"{chemin}: table imbriquée; le bandeau doit rester une "
                             "table simple, une ligne et deux cellules")
        if autonome:
            incorporees = sum(s.startswith("data:image/") for s in sources)
            print("  images incorporées         :", incorporees)
            if incorporees != len(sources) or incorporees != 2:
                problemes.append(f"{chemin}: {incorporees} image(s) incorporée(s) sur "
                                 f"{len(sources)} au lieu de 2; le fichier doit se "
                                 "suffire à lui-même")
            if "cid:" in corps:
                problemes.append(f"{chemin}: références cid: restantes")
        else:
            if any(s.startswith("data:") for s in sources):
                problemes.append(f"{chemin}: images incorporées en data:; cette "
                                 "variante les veut voisines, l'autre les incorpore")
            else:
                images_voisines(chemin, sources, problemes, "Notion")


def main():
    argv = sys.argv[1:]
    html_archive = markdown = html_plat = html_plat_autonome = None
    for drapeau in ("--html", "--markdown", "--html-plat-autonome", "--html-plat"):
        if drapeau in argv:
            i = argv.index(drapeau)
            valeur = argv[i + 1] if i + 1 < len(argv) else None
            if not valeur:
                raise SystemExit(f"{drapeau} attend un chemin")
            if drapeau == "--html":
                html_archive = valeur
            elif drapeau == "--markdown":
                markdown = valeur
            elif drapeau == "--html-plat-autonome":
                html_plat_autonome = valeur
            else:
                html_plat = valeur
            del argv[i:i + 2]
    if not argv:
        raise SystemExit("usage: verify.py fichier.msg [sources d'images...] "
                         "[--html courriel.html] [--markdown pastille.md]")
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

    controler_artefacts(html_archive, markdown, html_plat, html_plat_autonome,
                        problemes)

    print()
    if problemes:
        print("PROBLÈMES")
        for p in problemes:
            print(" -", p)
        sys.exit(1)
    print("aucun problème détecté")


if __name__ == "__main__":
    main()
