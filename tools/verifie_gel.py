#!/usr/bin/env python3
"""Verifie que le corps d'une pastille reprise est reste celui du courriel d'origine.

C'est le seul controle que la chaine officielle ne peut pas faire: `verify.py`
juge l'artefact produit, pas sa fidelite a un courriel envoye il y a des mois.

La comparaison ignore exactement ce que la chaine normalise legitimement, et
rien d'autre: emphases (markdown dans la fiche, balises dans le courriel),
apostrophes droites ou typographiques, espaces insecables, blancs multiples.
Une reformulation, un mot retire, une ponctuation deplacee ressortent.

Usage: python3 tools/verifie_gel.py <fiche.json> <courriel.eml>
       python3 tools/verifie_gel.py --tous
"""

from __future__ import annotations

import difflib
import email
import glob
import html as _html
import json
import os
import re
import sys
import unicodedata
from email import policy

BLOCK_TAGS = "div|p|br|tr|td|th|table|tbody|ul|ol|li|h[1-6]|blockquote|hr|img"
MIN_MOTS_CORPS = 25

# Mots que le francais accentue toujours. Leur forme nue dans un champ de la
# fiche trahit une perte d'accents, defaut que ni build.py ni verify.py ne
# voient (ils controlent les caracteres refuses, pas les caracteres manquants)
# et qui a effectivement traverse la premiere passe de reprise.
MOTS_ACCENTUES = (
    "reponse", "reponses", "etape", "etapes", "memoire", "generique", "generiques",
    "verite", "modele", "modeles", "donnee", "donnees", "resultat", "resultats",
    "precis", "precise", "apres", "tres", "deja", "meme", "schema", "legende",
    "requete", "cle", "cles", "verification", "verifiez", "verifier", "citees",
    "reperage", "independante", "independant", "confirme", "deforme", "chiffree",
    "datee", "laterale", "sourcee", "iteration", "cible", "declenche", "decoupez",
    "rediger", "premiere", "securite", "confidentialite", "responsabilite",
    "controle", "procede", "frequent", "complet", "concret", "enonce", "genere",
)


def accents_manquants(texte: str) -> list[str]:
    """Les mots du texte qui devraient porter un accent et n'en portent pas."""
    if any(unicodedata.combining(c) for c in unicodedata.normalize("NFD", texte)):
        return []
    mots = set(re.findall(r"[a-zA-Z'-]+", texte.lower()))
    return sorted(mot for mot in MOTS_ACCENTUES if mot in mots)


def normalise(texte: str) -> str:
    """Reduit un texte a ce que la chaine officielle ne doit pas changer."""
    texte = unicodedata.normalize("NFC", texte)
    for signe in ("’", "ʼ", "‘"):
        texte = texte.replace(signe, "'")
    for blanc in (" ", " ", " "):
        texte = texte.replace(blanc, " ")
    texte = texte.replace("**", "").replace("*", "")
    return re.sub(r"\s+", " ", texte).strip()


def texte_rendu(html: str) -> str:
    html = re.sub(r"(?is)<(script|style).*?</\1>", " ", html)
    html = re.sub(rf"(?i)</?({BLOCK_TAGS})\b[^>]*>", " ", html)
    html = re.sub(r"<[^>]+>", "", html)
    return normalise(_html.unescape(html))


def blocs_courriel(chemin: str) -> list[str]:
    """Les blocs de texte du courriel d'origine, corps et encadres.

    Les courriels anciens sont une suite de <div> Outlook; les deux derniers,
    deja diffuses au gabarit, sont une suite de cellules. On ratisse les deux,
    et c'est l'appariement avec la fiche qui distingue ensuite un paragraphe de
    corps d'une puce ou d'un bloc annexe.
    """
    with open(chemin, encoding="utf-8", errors="replace") as handle:
        message = email.message_from_file(handle, policy=policy.default)
    html = ""
    for part in message.walk():
        if part.get_content_type() == "text/html":
            html = part.get_content()
            break
    paragraphes = []
    for bloc in re.findall(r"(?is)<(?:div|td)[^>]*>(.*?)</(?:div|td)>", html):
        texte = texte_rendu(bloc)
        minuscule = texte.lower()
        if len(texte.split()) < MIN_MOTS_CORPS:
            continue
        if minuscule.startswith("bonjour") or "pastille llm du jour" in minuscule:
            continue
        if "peut contenir des traces d" in minuscule:
            continue
        if texte not in paragraphes:
            paragraphes.append(texte)
    return paragraphes


def verifie(fiche_chemin: str, eml_chemin: str) -> list[str]:
    with open(fiche_chemin, encoding="utf-8") as handle:
        fiche = json.load(handle)
    attendus = blocs_courriel(eml_chemin)
    obtenus = [normalise(p) for p in fiche["paragraphes"]]

    # Derogations au gel, decidees explicitement et tracees a cote de la fiche:
    # appliquees au texte d'origine avant comparaison, puis rappelees.
    derogations = []
    chemin_derogations = os.path.join(os.path.dirname(fiche_chemin), "gel-exceptions.json")
    if os.path.exists(chemin_derogations):
        with open(chemin_derogations, encoding="utf-8") as handle:
            derogations = json.load(handle)
    for entree in derogations:
        avant, apres = normalise(entree["origine"]), normalise(entree["reexport"])
        attendus = [bloc.replace(avant, apres) for bloc in attendus]

    # Un bloc du courriel peut avoir atterri ailleurs que dans le corps: une
    # puce de l'encadre ou le bloc annexe, pour les deux pastilles deja
    # diffusees au gabarit. On les accepte a ce titre, sans les confondre.
    ailleurs = [normalise(t) for t in
                fiche.get("essentiel", []) + [fiche.get("legende_schema", ""),
                                              fiche.get("alt_schema", ""),
                                              fiche.get("annexe", {}).get("texte", "")]]

    problemes = []
    for entree in derogations:
        problemes.append(f"! derogation au gel: {entree['raison']}")

    champs = {"legende_schema": fiche.get("legende_schema", ""),
              "alt_schema": fiche.get("alt_schema", ""),
              "annexe": fiche.get("annexe", {}).get("texte", ""),
              "axe": fiche.get("axe", ""),
              "apercu_visuels": fiche.get("apercu_visuels", "")}
    for rang, puce in enumerate(fiche.get("essentiel", []), start=1):
        champs[f"essentiel[{rang}]"] = puce
    for nom, texte in champs.items():
        manquants = accents_manquants(texte)
        if manquants:
            problemes.append(f"accents perdus dans {nom}: {', '.join(manquants[:5])}")
    for rang, paragraphe in enumerate(obtenus, start=1):
        if paragraphe in attendus:
            continue
        proche = difflib.get_close_matches(paragraphe, attendus, n=1, cutoff=0.6)
        detail = ""
        if proche:
            diff = [m for m in difflib.ndiff(proche[0].split(), paragraphe.split())
                    if m[0] in "-+"]
            detail = "\n      " + "\n      ".join(diff[:12])
        problemes.append(f"paragraphe {rang} de la fiche absent du courriel d'origine{detail}")
    for bloc in attendus:
        if bloc in obtenus or any(bloc in autre or autre in bloc for autre in ailleurs if autre):
            continue
        problemes.append(f"bloc du courriel absent de la reprise: {bloc[:90]}...")
    return problemes


def apparie() -> list[tuple[str, str]]:
    """Associe chaque fiche a son courriel d'origine, par numero d'envoi."""
    courriels = {}
    for chemin in glob.glob("emails/*.eml"):
        trouve = re.search(r"#(\d+)", os.path.basename(chemin))
        if trouve:
            courriels[int(trouve.group(1))] = chemin
    paires = []
    for fiche_chemin in sorted(glob.glob("archives/*/fiche.json")):
        with open(fiche_chemin, encoding="utf-8") as handle:
            numero = json.load(handle)["numero"]
        if numero in courriels:
            paires.append((fiche_chemin, courriels[numero]))
        else:
            print(f"[??] {fiche_chemin}: aucun courriel #{numero} dans emails/")
    return paires


def main() -> None:
    paires = apparie() if sys.argv[1:2] == ["--tous"] else [(sys.argv[1], sys.argv[2])]
    echec = False
    for fiche_chemin, eml_chemin in paires:
        problemes = verifie(fiche_chemin, eml_chemin)
        bloquants = [p for p in problemes if not p.startswith("!")]
        etiquette = os.path.basename(os.path.dirname(fiche_chemin))
        print(f"[{'KO' if bloquants else 'OK'}] {etiquette}")
        for probleme in problemes:
            if probleme.startswith("!"):
                print(f"  {probleme}")
            else:
                echec = True
                print(f"  - {probleme}")
    sys.exit(1 if echec else 0)


if __name__ == "__main__":
    main()
