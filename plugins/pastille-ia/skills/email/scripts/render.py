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
import json as _json
import re as _re
import unicodedata as _unicodedata

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
    l'attribut, les clients modernes le style. Attention: Word ne peint jamais un
    fond de table, seulement un fond de cellule. Un bloc coloré doit donc aussi
    porter son fond sur son <td>, via cellule(); le fond de table ne sert qu'aux
    autres clients."""
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


def cellule(padding, fond=None, extra=""):
    """Cellule de contenu. C'est ici que le fond d'un bloc coloré doit vivre pour
    que Word le peigne."""
    attribut = f' bgcolor="{fond}"' if fond else ""
    css = f"background-color:{fond}; " if fond else ""
    return f'<td{attribut} style="{css}padding:{padding};{extra}">\n'


def ligne(contenu, padding):
    return f'<tr>\n<td style="padding:{padding};">\n{contenu}\n</td>\n</tr>\n'


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


# Codages sur deux octets. Ce sont eux qui font disparaître des caractères quand
# un détecteur se trompe, et c'est sur l'un d'eux qu'Outlook (new) trébuche.
CODAGES_DEUX_OCTETS = ("cp936", "cp932", "cp949", "cp950")


def hors_cp1252(sujet):
    """Caractères de l'objet absents de cp1252, dans leur ordre d'apparition.

    Ils sont un risque à part: là où Outlook (new) rabat l'objet en octets
    cp1252, un caractère absent de cette table devient un « ? » bien visible.
    Une espace fine ou insécable Unicode, un tiret cadratin, un emoji tombent
    dans ce cas.
    """
    manquants = []
    for c in sujet:
        try:
            c.encode("cp1252")
        except UnicodeEncodeError:
            if c not in manquants:
                manquants.append(c)
    return manquants


def objet_ambigu(sujet):
    """Rendus erronés possibles de l'objet, chez un client qui rabat l'objet
    Unicode en octets 8 bits avant de le relire.

    Outlook (new) reconvertit le .msg en MIME: l'objet redevient de l'octet
    cp1252, puis est relu dans un codage sur deux octets, avec repli sur cp1252
    quand ce décodage échoue. Or il n'échoue que si la chaîne s'y prête mal: un
    seul accent suivi d'un espace ou d'une ponctuation (octet < 0x40) suffit à
    le faire échouer, et le repli protège alors l'objet entier. D'où le
    contrôle: un objet qui se décode de bout en bout dans un de ces codages
    sera affiché de travers, un objet qui les fait échouer est sain.

    Les caractères hors cp1252 sont remplacés par « ? » comme le ferait le
    client, plutôt qu'ignorés: c'est ce « ? » qui casse alors le décodage sur
    deux octets, et il faut le voir venir. Utiliser hors_cp1252 en plus, pour
    ne pas guérir un objet illisible par un objet ponctué de « ? ».

    Rend la liste des (codage, rendu erroné). Vide quand l'objet ne risque
    rien, ce qui est notamment le cas dès qu'il est en ASCII pur.
    """
    octets = sujet.encode("cp1252", errors="replace")
    ambigus = []
    for codage in CODAGES_DEUX_OCTETS:
        try:
            rendu = octets.decode(codage)
        except UnicodeDecodeError:
            continue
        if rendu != sujet:
            ambigus.append((codage, rendu))
    return ambigus


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
        + cellule("16px 18px", fond=FOND_ESSENTIEL)
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
            # La légende se cale sur la largeur du schéma, pas sur celle de la
            # colonne: une phrase qui dépasse l'image qu'elle décrit ne se
            # rattache plus visuellement à elle. Même plafond que l'image, donné
            # en plus à Word par commentaire conditionnel, puisqu'il ignore
            # max-width; la largeur reste fluide en dessous.
            legende = (
                f'<!--[if mso]><table role="presentation" cellpadding="0" '
                f'cellspacing="0" border="0" width="{W_SCHEMA}" align="center" '
                f'style="width:{W_SCHEMA}px;"><tr><td style="padding:0;">'
                f'<![endif]-->\n'
                + table(extra=f" max-width:{W_SCHEMA}px;")
                + '<td style="padding:0;">\n'
                + para(c["legende_schema"], GRIS, 13, 20, align=None)
                + "\n</td>\n</tr>\n</table>\n"
                + "<!--[if mso]></td></tr></table><![endif]-->")
            out.append('<tr>\n<td align="center" style="padding:8px 20px 0 20px;">\n'
                       + legende + "\n</td>\n</tr>\n")

    if c.get("annexe"):
        a = c["annexe"]
        teintes = ANNEXES[a.get("style", "essayer")]
        bloc = (
            table(fond=teintes["fond"])
            + f'<td width="4" bgcolor="{teintes["barre"]}" style="background-color:'
              f'{teintes["barre"]}; width:4px; font-size:0; line-height:0;">&nbsp;</td>\n'
            + cellule("16px 18px", fond=teintes["fond"])
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


MARQUE_DOSSIER = "pastille:dossier"
FIN_DOSSIER = "pastille:fin"
FORMAT_DOSSIER = 1


def dossier_incorpore(c):
    """Le dossier de la pastille, en JSON, dans un commentaire HTML.

    L'artefact conservé est la référence pour reprendre une pastille des mois
    plus tard: il doit donc porter de quoi la reconstruire, et pas seulement de
    quoi la lire. Tout ce que la fiche contient part avec lui, prompt d'images,
    titre canonique, axe, sources et notes d'échange compris.

    Un commentaire plutôt qu'un `<script>` ou des `<meta>`: un analyseur HTML
    supprime les commentaires par définition, alors qu'un importeur naïf peut
    recracher le contenu d'un script au milieu de la page, comme il le ferait
    d'une feuille de style. Les visuels, eux, sont déjà dans le fichier en
    base64: l'artefact suffit donc à tout refabriquer, courriel compris.
    """
    dossier = {"_format": FORMAT_DOSSIER, **{k: v for k, v in c.items()
                                             if not k.startswith("_")}}
    texte = _json.dumps(dossier, ensure_ascii=False, indent=1, sort_keys=False)
    # Un `--` fermerait le commentaire par accident. Le second tiret part en
    # échappement JSON, que json.loads rend à l'identique: aller-retour exact.
    texte = texte.replace("--", "-\\u002d")
    return f"<!--{MARQUE_DOSSIER}\n{texte}\n{FIN_DOSSIER}-->"


def lire_dossier(html):
    """Inverse de dossier_incorpore: rend la fiche telle qu'elle a été écrite."""
    debut = html.find(f"<!--{MARQUE_DOSSIER}")
    fin = html.find(f"{FIN_DOSSIER}-->", debut + 1)
    if debut < 0 or fin < 0:
        raise ValueError("aucun dossier de pastille dans ce fichier")
    brut = html[debut + len(MARQUE_DOSSIER) + 4:fin]
    return _json.loads(brut)


def limace(titre, numero=None):
    """Nom de fichier lisible tiré du titre.

    Notion nomme une page importée d'après le nom du fichier, pas d'après le h1
    qu'il contient: le nom de l'artefact est donc le titre de la page, et il
    mérite d'être choisi.
    """
    texte = sans_balises(titre)
    # Les titres de la série sont en « accroche : glose »: l'accroche suffit à
    # nommer la page, et elle est autrement plus lisible que le titre entier
    # tronqué au milieu d'une subordonnée.
    accroche = _re.split(r"\s*[:?]\s*", texte, maxsplit=1)[0]
    if len(accroche.split()) >= 2:
        texte = accroche
    base = _unicodedata.normalize("NFKD", texte)
    base = base.encode("ascii", "ignore").decode("ascii").lower()
    # Séparateur: l'espace. Les tirets ne survivent pas à toutes les chaînes de
    # téléchargement, qui les suppriment et recollent les mots; l'espace, lui,
    # passe, et il donne un titre de page lisible côté Notion.
    base = _re.sub(r"[^a-z0-9]+", " ", base).strip()
    while len(base) > 48 and " " in base:
        base = base.rsplit(" ", 1)[0]
    return " ".join(([f"pastille {numero}"] if numero is not None else []) + [base])


def fr_texte(texte):
    """Typographie française en caractères réels, pas en entités: pour tout ce
    qui n'est pas du HTML de courriel (version texte, Markdown)."""
    return _html.unescape(fr(texte))


def emphases_simples(texte):
    """**gras** et *italique* en balises nues, sans style: le HTML aplati n'a
    pas à porter les contournements de Word."""
    texte = _re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", texte)
    return _re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", texte)


def _inline(texte):
    """Typographie, puis échappement, puis emphases: dans cet ordre, sinon
    l'échappement se fait défaire par l'unescape de la typographie."""
    return emphases_simples(_html.escape(fr_texte(texte), quote=False))


def html_plat_pastille(c, source_image_titre, source_image_schema):
    """HTML sémantique, sans table de mise en page, habillé aux teintes de la série.

    Le courriel est bâti en tables imbriquées parce que Word ne sait rien faire
    d'autre; c'est précisément ce qu'un importeur aplatit mal. Ici chaque bloc
    est la balise qui le décrit: un titre est un h1, une synthèse est une
    citation à puces, une légende est une figcaption. Un import garde donc la
    structure, et un navigateur retrouve l'allure du courriel.

    Deux choix expliquent la forme du code:

    1. Les styles sont en ligne, pas dans une feuille `<style>`. Un importeur
       qui ne lit pas le CSS ignore une feuille sans dommage, mais un importeur
       naïf peut aussi en recracher le contenu au milieu de la page. En ligne,
       ce risque n'existe pas, et c'est accessoirement la seule chose que le
       courriel sait faire, donc le même vocabulaire sert deux fois.
    2. Le titre ouvre le fichier, avant le bandeau, parce qu'à l'import il ouvre
       alors la page. Il reste masqué visuellement, l'illustration le portant
       déjà comme dans le courriel, et le masquage est visuel plutôt qu'un
       `display:none` qui l'aurait aussi retiré aux lecteurs d'écran.
    3. Le bandeau est la seule table de cet artefact, et c'est délibéré: une
       table simple s'importe comme une table, donc la rubrique et le temps de
       lecture ne se retrouvent pas collés en une seule ligne de texte.
    4. Les couleurs sont dérivées de la palette de la série, jamais réécrites:
       le bandeau, l'encadré et les blocs annexes reprennent exactement les
       teintes du courriel, y compris les versions assombries des petits
       libellés, qui existent pour le contraste.

    Les deux sources d'images sont des chemins tels quels: l'appelant passe soit
    un nom de fichier voisin (l'artefact voyage dans un dossier ou une archive),
    soit une URL `data:` (l'artefact se suffit à lui-même). Le balisage ne change
    pas, seule la portabilité du fichier change.
    """
    def st(couleur, taille, interligne, extra=""):
        return (f"color:{couleur}; font-size:{taille}px; line-height:{interligne}px; "
                f"{extra}font-family:{FONT};")

    p_corps = (f'margin:0 0 16px 0; {st(NOIR, 16, 26, "text-align:justify; ")}')
    out = [
        # Titre en tête, avant le bandeau: à l'import il ouvre la page, ce qui se
        # lit mieux qu'un titre glissé après le bandeau. Il reste masqué au rendu,
        # l'illustration le portant déjà comme dans le courriel. Le masquage est
        # visuel et non un display:none, qui l'aurait aussi retiré aux lecteurs
        # d'écran. Il ne nomme pas la page importée pour autant: Notion la nomme
        # d'après le nom du fichier, d'où la convention de nommage de l'artefact.
        f'<h1 style="position:absolute; width:1px; height:1px; margin:-1px; '
        f'padding:0; overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap; '
        f'border:0;">{_inline(c["titre"])}</h1>',

        # Bandeau de série: une table d'une ligne et deux cellules, seule table de
        # cet artefact et seule exception assumée à son balisage sans tables. La
        # raison est l'import: une table simple arrive dans Notion comme une
        # table, donc la rubrique et le temps de lecture restent dans deux
        # cellules distinctes au lieu d'être collés en une seule ligne de texte.
        # Le repli est prévu si l'importeur l'aplatit quand même: la cellule de
        # droite commence par une espace insécable, invisible en cellule alignée
        # à droite, mais qui évite le mot-valise si la table tombe.
        f'<table style="width:100%; border-collapse:collapse; margin:0 0 24px 0; '
        f'background-color:{MARQUE_BLEU};">'
        f'<tr>'
        # Les cellules extérieures se réduisent à leur contenu (width:1%), la
        # cellule du milieu prend le reste: sans cela les trois colonnes se
        # partagent la largeur et le numéro s'éloigne de la rubrique, alors que
        # le courriel les garde côte à côte.
        f'<td style="width:1%; padding:14px 4px 14px 20px; white-space:nowrap; '
        f'{st(BLANC, 13, 24)}">'
        f'<strong style="{st(MARQUE_ORANGE, 22, 24, "font-weight:700; ")}">'
        f'{c["numero"]}</strong>'
        f'<span style="{st(BLEU_PALE, 12, 24)}">&nbsp;/&nbsp;{c["total"]}</span>'
        f'</td>'
        f'<td style="width:98%; padding:14px 20px; {st(BLANC, 13, 24)}">'
        f'PASTILLE IA&nbsp;&nbsp;&middot;&nbsp;&nbsp;'
        f'{_html.escape(fr_texte(c["rubrique"])).upper()}</td>'
        f'<td align="right" style="width:1%; padding:14px 20px; '
        f'white-space:nowrap; {st(BLEU_PALE, 12, 24, "text-align:right; ")}">'
        f'&nbsp;{c["temps_lecture"]} de lecture</td>'
        f'</tr></table>',

        f'<p style="margin:0 0 24px 0;">'
        f'<img src="{source_image_titre}" '
        f'alt="{_html.escape(sans_balises(c["titre"]))}" '
        f'style="max-width:{W_TITRE}px; width:100%; height:auto; display:block; '
        f'margin:0 auto;"></p>',

        f'<blockquote style="margin:0 0 24px 0; padding:16px 18px; '
        f'background-color:{FOND_ESSENTIEL}; border:{BORDURE_ESSENTIEL};">',
        f'<p style="margin:0; {st(ORANGE_TEXTE, 12, 16, "font-weight:700; letter-spacing:0.6px; ")}">'
        f'<strong>L’ESSENTIEL</strong></p>',
        f'<ul style="margin:10px 0 0 0; padding:0 0 0 20px; '
        f'{st(MARQUE_BLEU, 16, 25, "font-weight:700; ")}">',
    ]
    out += [f'<li style="margin:0 0 6px 0; {st(MARQUE_BLEU, 16, 25, "font-weight:700; ")}">'
            f'<strong>{_inline(p)}</strong></li>' for p in c["essentiel"]]
    out += ["</ul>", "</blockquote>"]

    apres = c.get("schema_apres", len(c["paragraphes"]) - 1)
    for i, para_texte in enumerate(c["paragraphes"], start=1):
        out.append(f'<p style="{p_corps}">{_inline(para_texte)}</p>')
        if i == apres:
            out += [
                # La figure porte le plafond de largeur, et non l'image seule:
                # la légende se cale ainsi sur la largeur du schéma au lieu de
                # s'étaler sur toute la colonne.
                f'<figure style="max-width:{W_SCHEMA}px; margin:0 auto 16px auto;">',
                f'<img src="{source_image_schema}" '
                f'alt="{_html.escape(fr_texte(c["alt_schema"]))}" '
                f'style="width:100%; height:auto; display:block;">',
                f'<figcaption style="margin:8px 0 0 0; {st(GRIS, 13, 20)}">'
                f'{_inline(c["legende_schema"])}</figcaption>',
                "</figure>"]

    if c.get("annexe"):
        a = c["annexe"]
        teintes = ANNEXES[a.get("style", "essayer")]
        out += [
            f'<blockquote style="margin:8px 0 24px 0; padding:16px 18px; '
            f'background-color:{teintes["fond"]}; '
            f'border-left:4px solid {teintes["barre"]};">',
            f'<p style="margin:0; '
            f'{st(teintes["etiquette"], 12, 16, "font-weight:700; letter-spacing:0.4px; ")}">'
            f'<strong>{_inline(a["etiquette"]).upper()}</strong></p>',
            f'<p style="margin:8px 0 0 0; {st(teintes["texte"], 15, 24)}">'
            f'{_inline(a["texte"])}</p>',
            "</blockquote>"]

    out += [
        f'<hr style="border:0; border-top:1px solid {eclaircir(GRIS, 0.70)}; '
        f'margin:24px 0 16px 0;">',
        f'<p style="margin:0 0 8px 0; {st(GRIS, 13, 20, "font-style:italic; ")}">'
        f'<em>{_inline(c["mention_ia"])}</em></p>',
        f'<p style="margin:0; {st(MARQUE_BLEU, 15, 24, "font-weight:700; ")}">'
        f'<strong>{_inline(c["signature"])}</strong></p>']

    # Sources: dans l'archive, pas dans le courriel. La norme les réserve à la
    # vérification et ne les publie pas, mais un artefact conservé sans ses
    # références perd ce qui permet de le rejuger plus tard.
    #
    # Elles vivent dans un <details>, replié. Ce choix règle la question de leur
    # visibilité sans recourir au CSS, qu'un importeur ignore: un navigateur
    # replie nativement l'élément, et Notion exporte ses blocs dépliants sous
    # cette forme, donc il devrait les relire comme tels. Si un importeur ne
    # connaissait pas <details>, le repli est bénin: les sources s'afficheraient
    # simplement en liste, ce qui reste correct pour une archive.
    if c.get("sources"):
        out += [f'<details style="margin:24px 0 0 0;">',
                f'<summary style="{st(GRIS, 12, 18, "font-weight:700; letter-spacing:0.6px; cursor:pointer; ")}">'
                f'SOURCES</summary>',
                f'<ul style="margin:8px 0 0 0; padding:0 0 0 20px; {st(GRIS, 13, 20)}">']
        for source in c["sources"]:
            if isinstance(source, str):
                libelle, url = source, None
            else:
                libelle, url = source.get("titre", source.get("url", "")), source.get("url")
            corps_source = _inline(libelle)
            if url and url != libelle:
                corps_source += (f' &ndash; <a href="{_html.escape(url, quote=True)}" '
                                 f'style="{st(GRIS, 13, 20)}">{_html.escape(url)}</a>')
            out.append(f'<li style="margin:0 0 4px 0; {st(GRIS, 13, 20)}">'
                       f'{corps_source}</li>')
        out += ["</ul>", "</details>"]

    corps = "\n".join(out)
    return ('<html><head><meta charset="utf-8">'
            f"<title>{_html.escape(sans_balises(c['titre']))}</title></head>\n"
            f'<body style="margin:0 auto; padding:24px 20px; max-width:{MAX_W}px; '
            f'background-color:{BLANC}; {st(NOIR, 16, 26)}">\n'
            f"{corps}\n{dossier_incorpore(c)}\n</body></html>\n")


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
