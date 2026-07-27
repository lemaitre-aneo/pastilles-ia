"""Rendu du courriel d'une pastille: corps HTML et version texte.

Trois contraintes viennent du moteur de rendu de Word, qui affiche les .msg
ouverts dans Outlook pour Windows. Elles ne sont pas cosmétiques, chacune
correspond à un défaut constaté:

1. `color` est déclaré en premier dans chaque style et `font-family` en dernier.
   Un nom de police entre apostrophes casse l'analyse CSS de Word, qui abandonne
   la fin de la déclaration: la couleur doit être passée avant ce point de rupture.
2. Les noms de police ne sont jamais entre apostrophes, pour la même raison.
3. Chaque bloc double sa mise en forme en balises présentationnelles
   (<font color face>, <b>, <i>), que Word applique sans passer par le CSS.

Et une contrainte d'héritage: Word ne propage pas la couleur d'un <td> vers le
texte qu'il contient, il applique celle du thème de rédaction. Toute couleur est
donc portée par l'élément qui porte réellement le texte.
"""
import html as _html
import re as _re

FONT = "Aptos, Calibri, Segoe UI, Helvetica, Arial, sans-serif"
FACE = "Aptos, Calibri, Segoe UI, Helvetica, Arial"

MAX_W = 1000        # plafond de la colonne de texte, en pixels
W_TITRE = 600       # largeur fixe de l'illustration-titre
W_SCHEMA = 560      # largeur fixe du schéma

# --- palette -----------------------------------------------------------------
# Les trois couleurs officielles sont la source; tout le reste en est dérivé par
# mélange, pour qu'aucune teinte ne vive en double dans le fichier.
MARQUE_ORANGE = "#FE5100"
MARQUE_BLEU = "#000F9F"
MARQUE_ORANGE_CLAIR = "#FFB600"

NOIR = "#2B2B2B"
BLANC = "#FFFFFF"
GRIS = "#6B7280"


def melange(couleur_a, couleur_b, part_a):
    """Mélange linéaire de deux couleurs, part_a entre 0 et 1."""
    a = [int(couleur_a[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(couleur_b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x * part_a + y * (1 - part_a)):02X}"
                         for x, y in zip(a, b))


def eclaircir(couleur, part_blanc):
    return melange(BLANC, couleur, part_blanc)


def assombrir(couleur, part_noir):
    return melange("#000000", couleur, part_noir)


# Dérivés. L'orange de marque tombe à 3,2:1 sur blanc, insuffisant pour un texte
# de 12 pixels: les petits libellés prennent une version assombrie, qui remonte
# au delà de 5:1. Les fonds sont le même orange ou le même bleu, très éclaircis.
ORANGE_TEXTE = assombrir(MARQUE_ORANGE, 0.25)
BLEU_PALE = eclaircir(MARQUE_BLEU, 0.60)

# Encadré de synthèse: texte en gras sur teinte claire. Le gras est le seul poids
# fiable en courriel, Word ne rend pas les poids intermédiaires. La bordure pleine
# sur les quatre côtés le sépare des blocs annexes, qui n'ont qu'une barre latérale.
FOND_ESSENTIEL = eclaircir(MARQUE_BLEU, 0.96)
BORDURE_ESSENTIEL = f"1px solid {MARQUE_BLEU}"

ANNEXES = {
    "essayer": {"fond": eclaircir(MARQUE_ORANGE_CLAIR, 0.90),
                "barre": MARQUE_ORANGE,
                "etiquette": ORANGE_TEXTE,
                "texte": assombrir(MARQUE_ORANGE, 0.55)},
    "piege": {"fond": eclaircir(MARQUE_BLEU, 0.95),
              "barre": MARQUE_BLEU,
              "etiquette": MARQUE_BLEU,
              "texte": melange(MARQUE_BLEU, NOIR, 0.35)},
}


def table(extra="", fond=None):
    """Table de mise en page. Le fond est posé en attribut et en style: Word lit
    l'attribut, les clients modernes le style."""
    attribut = f' bgcolor="{fond}"' if fond else ""
    css = f" background-color:{fond};" if fond else ""
    return ('<table role="presentation" cellpadding="0" cellspacing="0" border="0" '
            f'width="100%"{attribut} style="width:100%; border-collapse:collapse; '
            f'mso-table-lspace:0pt; mso-table-rspace:0pt;{css}{extra}"><tr>\n')


# La rubrique suit la position du sujet dans la liste des 45, jamais le numéro
# de diffusion: les deux sont indépendants.
RUBRIQUES = ((range(1, 10), "Comprendre"), (range(10, 15), "Limites"),
             (range(15, 16), "Risques et cadre"), (range(16, 23), "Prompting"),
             (range(23, 30), "Au travail"), (range(30, 39), "Agents et outils"),
             (range(39, 46), "Risques et cadre"))

MOTS_PAR_MINUTE = 180


def rubrique_pour(position):
    for intervalle, nom in RUBRIQUES:
        if int(position) in intervalle:
            return nom
    raise ValueError(f"position hors de la liste des 45: {position}")


def temps_lecture(c):
    """Estimation à partir de tout le texte lu, encadrés compris."""
    morceaux = list(c["essentiel"]) + list(c["paragraphes"]) + [c["legende_schema"]]
    if c.get("annexe"):
        morceaux.append(c["annexe"]["texte"])
    mots = sum(len(m.split()) for m in morceaux)
    return f"{max(1, -(-mots // MOTS_PAR_MINUTE))} min"


# --- typographie française ---------------------------------------------------

def fr(texte):
    """Espace insécable avant : ; ! ? et apostrophe typographique.
    Le balisage et les entités HTML sont laissés intacts."""
    morceaux = _re.split(r"(<[^>]*>)", texte)
    sortie = []
    for i, bout in enumerate(morceaux):
        if i % 2:                       # une balise, on n'y touche pas
            sortie.append(bout)
            continue
        entites = []

        def _garder(m):
            entites.append(m.group(0))
            return f"\x00{len(entites) - 1}\x00"

        bout = _re.sub(r"&[a-zA-Z]+;|&#\d+;", _garder, bout)
        bout = bout.replace("'", "’")
        bout = _re.sub(r"[  ]*([;:!?])", lambda m: "&nbsp;" + m.group(1), bout)
        bout = _re.sub(r"\x00(\d+)\x00", lambda m: entites[int(m.group(1))], bout)
        sortie.append(bout)
    return "".join(sortie)


def sans_balises(texte):
    return _html.unescape(_re.sub(r"<[^>]*>", "", fr(emphases(texte, NOIR))))


def ascii_seul(html):
    """Échappe tout caractère non ASCII: un courriel dont le corps est en
    entités traverse n'importe quel client, quelle que soit sa détection
    d'encodage."""
    return html.encode("ascii", "xmlcharrefreplace").decode("ascii")


def emphases(texte, couleur):
    """**gras** et *italique* en balises, couleur redéclarée à chaque fois."""
    texte = _re.sub(r"\*\*(.+?)\*\*",
                    lambda m: f'<strong style="color:{couleur};">{m.group(1)}</strong>',
                    texte)
    return _re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)",
                   lambda m: f'<em style="color:{couleur};">{m.group(1)}</em>', texte)


# --- briques HTML ------------------------------------------------------------

def style(couleur, taille, interligne, extra=""):
    return (f"color:{couleur}; font-size:{taille}px; line-height:{interligne}px; "
            f"{extra}mso-line-height-rule:exactly; font-family:{FONT};")


def span(contenu, couleur, taille, interligne, extra="", gras=False, italique=False):
    interne = fr(emphases(contenu, couleur))
    if gras:
        interne = f"<b>{interne}</b>"
    if italique:
        interne = f"<i>{interne}</i>"
    st = style(couleur, taille, interligne, extra)
    return f'<font color="{couleur}" face="{FACE}"><span style="{st}">{interne}</span></font>'


def para(contenu, couleur=NOIR, taille=16, interligne=26, extra="", align="justify",
         gras=False, italique=False, marge="0"):
    st = style(couleur, taille, interligne, extra + (f"text-align:{align}; " if align else ""))
    corps = span(contenu, couleur, taille, interligne, extra, gras, italique)
    return f'<p style="margin:{marge}; padding:0; {st}">{corps}</p>'


def ligne(cellule, padding):
    return f'<tr>\n<td style="padding:{padding};">\n{cellule}\n</td>\n</tr>\n'


def image(cid, alt, largeur):
    return (f'<img src="cid:{cid}" width="{largeur}" alt="{fr(alt)}" '
            f'style="width:100%; max-width:{largeur}px; height:auto; display:block; '
            f'border:0; outline:none; text-decoration:none;">')


# --- assemblage --------------------------------------------------------------

def sujet(c):
    """[Prefixe] #NN : Titre. Typographie appliquée au préfixe comme au titre,
    mais en espaces ordinaires: les insécables et la recherche des messageries
    font mauvais ménage."""
    brut = f'{c["prefixe_sujet"]} #{c["numero"]} : {c["titre"]}'
    return sans_balises(brut).replace(" ", " ")


def html_pastille(c):
    out = [table(fond="#FFFFFF")]
    out.append('<td align="center" valign="top" style="padding:0;">\n')
    # Word ignore max-width: le plafond lui est donné en commentaire conditionnel,
    # que les autres clients traitent comme un commentaire ordinaire.
    out.append(f'<!--[if mso]><table role="presentation" cellpadding="0" cellspacing="0" '
               f'border="0" width="{MAX_W}" align="center" style="width:{MAX_W}px;"><tr>'
               f'<td style="padding:0;"><![endif]-->\n')
    out.append(table(extra=f" max-width:{MAX_W}px;"))

    bandeau = (
        table()
        + '<td align="left" valign="middle" style="padding:0;">\n'
        + f'<p style="margin:0; padding:0; {style(BLANC, 13, 24)}">'
        + span(str(c["numero"]), MARQUE_ORANGE, 22, 24, "font-weight:700; ", gras=True)
        + span(f'&nbsp;/&nbsp;{c["total"]}', BLEU_PALE, 12, 24)
        + span(f'&nbsp;&nbsp;&nbsp;PASTILLE IA&nbsp;&nbsp;&middot;&nbsp;&nbsp;'
               f'{c["rubrique"].upper()}', BLANC, 13, 24)
        + "</p>\n</td>\n"
        + '<td align="right" valign="middle" style="padding:0;">\n'
        + para(f'{c["temps_lecture"]} de lecture', BLEU_PALE, 12, 24,
               "white-space:nowrap; ", align=None)
        + "\n</td>\n</tr>\n</table>"
    )
    out.append(f'<tr>\n<td bgcolor="{MARQUE_BLEU}" style="background-color:{MARQUE_BLEU}; '
               f'padding:14px 20px;">\n{bandeau}\n</td>\n</tr>\n')

    out.append('<tr>\n<td align="center" style="padding:0; font-size:0; line-height:0;">\n'
               + image("IMAGE_TITRE", c["titre"], W_TITRE) + "\n</td>\n</tr>\n")

    puces = "".join(
        f'<li style="{style(MARQUE_BLEU, 16, 25, "font-weight:700; ")} margin:0; '
        f'padding:0 0 {6 if i < len(c["essentiel"]) - 1 else 0}px 0;">'
        + span(p, MARQUE_BLEU, 16, 25, "font-weight:700; ", gras=True) + "</li>\n"
        for i, p in enumerate(c["essentiel"]))
    essentiel = (
        table(extra=f" border:{BORDURE_ESSENTIEL};" if BORDURE_ESSENTIEL else "",
              fond=FOND_ESSENTIEL)
        + '<td style="padding:16px 18px;">\n'
        + para("L'ESSENTIEL", ORANGE_TEXTE, 12, 16,
               "font-weight:700; letter-spacing:0.6px; ", align=None, gras=True)
        + f'\n<ul style="margin:10px 0 0 0; padding:0 0 0 20px; {style(MARQUE_BLEU, 16, 25, "font-weight:700; ")}">\n'
        + puces + "</ul>\n</td>\n</tr>\n</table>"
    )
    out.append(ligne(essentiel, "24px 20px 0 20px"))

    apres = c.get("schema_apres", len(c["paragraphes"]) - 1)
    for i, p in enumerate(c["paragraphes"], start=1):
        out.append(ligne(para(p), f'{24 if i == 1 else 16}px 20px 0 20px'))
        if i == apres:
            out.append('<tr>\n<td align="center" style="padding:24px 20px 0 20px; '
                       'font-size:0; line-height:0;">\n'
                       + image("IMAGE_SCHEMA", c["alt_schema"], W_SCHEMA)
                       + "\n</td>\n</tr>\n")
            out.append(ligne(para(c["legende_schema"], GRIS, 13, 20, align=None),
                             "8px 20px 0 20px"))

    if c.get("annexe"):
        a = c["annexe"]
        teintes = ANNEXES[a.get("style", "essayer")]
        bloc = (
            table(fond=teintes["fond"])
            + f'<td width="4" bgcolor="{teintes["barre"]}" style="background-color:'
              f'{teintes["barre"]}; width:4px; font-size:0; line-height:0;">&nbsp;</td>\n'
            + '<td style="padding:16px 18px;">\n'
            + para(a["etiquette"].upper(), teintes["etiquette"], 12, 16,
                   "font-weight:700; letter-spacing:0.4px; ", align=None, gras=True)
            + "\n" + para(a["texte"], teintes["texte"], 15, 24, align=None,
                          marge="8px 0 0 0")
            + "\n</td>\n</tr>\n</table>"
        )
        out.append(ligne(bloc, "24px 20px 0 20px"))

    trait = (table()
             + '<td height="1" bgcolor="#DFE3E8" style="background-color:#DFE3E8; '
               'height:1px; font-size:0; line-height:0;">&nbsp;</td>\n</tr>\n</table>')
    out.append('<tr>\n<td style="padding:26px 20px 0 20px; font-size:0; line-height:0;">\n'
               + trait + "\n</td>\n</tr>\n")

    out.append(ligne(para(c["mention_ia"], GRIS, 13, 20, "font-style:italic; ",
                          align=None, italique=True), "16px 20px 0 20px"))
    out.append(ligne(para(c["signature"], MARQUE_BLEU, 14, 20, "font-weight:700; ",
                          align=None, gras=True), "12px 20px 28px 20px"))

    out.append("</table>\n<!--[if mso]></td></tr></table><![endif]-->\n")
    out.append("</td>\n</tr>\n</table>\n")
    return ascii_seul("".join(out))


def document_html(c, corps):
    """Document complet: Word veut un <html> en règle, et la couleur de base est
    redéclarée sur <body> et sur un conteneur, en plancher."""
    return (
        '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">'
        f"<title>{ascii_seul(_html.escape(sujet(c)))}</title></head>"
        f'<body style="margin:0; padding:0; background-color:#FFFFFF; color:{NOIR}; '
        f'font-family:{FONT}; font-size:16px;">\n'
        f'<div style="color:{NOIR}; font-family:{FONT}; font-size:16px;">\n'
        + corps + "\n</div>\n</body></html>\n"
    )


def texte_pastille(c):
    """Version texte du même contenu, pour les clients sans HTML."""
    lignes = [f'PASTILLE IA {c["numero"]} / {c["total"]}  .  {c["rubrique"].upper()}'
              f'  .  {c["temps_lecture"]} de lecture', "",
              sans_balises(c["titre"]).upper(), "", "L’ESSENTIEL"]
    lignes += ["- " + sans_balises(p) for p in c["essentiel"]]
    apres = c.get("schema_apres", len(c["paragraphes"]) - 1)
    for i, p in enumerate(c["paragraphes"], start=1):
        lignes += ["", sans_balises(p)]
        if i == apres:
            lignes += ["", "[Schéma] " + sans_balises(c["legende_schema"])]
    if c.get("annexe"):
        lignes += ["", c["annexe"]["etiquette"].upper(),
                   sans_balises(c["annexe"]["texte"])]
    lignes += ["", sans_balises(c["mention_ia"]), "", sans_balises(c["signature"]), ""]
    return "\n".join(lignes)
