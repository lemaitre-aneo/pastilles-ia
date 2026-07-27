#!/usr/bin/env python3
"""Contrôle un .msg fabriqué: structure, propriétés, pièces jointes, typographie.

    python3 verify.py pastille-13.msg [image-titre.png image-schema.png]

Un parseur indépendant (olefile) rouvre le fichier: c'est le seul moyen de
vérifier le conteneur sans Outlook. Le rendu visuel, lui, se contrôle avec
l'aperçu HTML et un navigateur.
"""
import hashlib
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


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: verify.py fichier.msg [sources d'images...]")
    chemin = sys.argv[1]
    sources = sys.argv[2:]
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

    print()
    if problemes:
        print("PROBLÈMES")
        for p in problemes:
            print(" -", p)
        sys.exit(1)
    print("aucun problème détecté")


if __name__ == "__main__":
    main()
