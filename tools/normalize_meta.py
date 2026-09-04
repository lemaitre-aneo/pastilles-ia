#!/usr/bin/env python3
"""Normalise les meta.json des pastilles reexportees sur un schema unique.

Les agents de reprise ont produit des schemas divergents (numero_envoi contre
numero_diffusion, temps_de_lecture contre temps_lecture, titre canonique
parfois absent). Seul `sujet` est utilise par build_eml.py, donc rien n'etait
casse, mais un schema commun rend le dossier exploitable par script.

Les valeurs sont derivees du HTML livre (source de verite du rendu) plutot que
recopiees des anciens meta.json, sauf le sujet du courriel, qui vient de
l'import. Genere aussi l'index et le recapitulatif des points de vigilance.

Usage: python3 tools/normalize_meta.py
"""

from __future__ import annotations

import html
import json
import os
import re

TOTAL_SERIE = 45

# Numero d'envoi -> position dans la liste canonique des 45, titre canonique,
# rubrique. Le bandeau porte le numero d'envoi (choix du commanditaire) mais la
# rubrique suit le sujet reel, donc la position canonique.
CANONIQUE = {
    1: (1, "Au fait, c'est quoi un LLM ?", "Comprendre"),
    2: (16, "Anatomie d'un bon prompt : la recette de base", "Prompting"),
    3: (23, "Zéro syndrome de la page blanche : rédiger et reformuler ses mails ou CR", "Au travail"),
    4: (3, "Dans les coulisses : comment une IA apprend (sans vraiment comprendre)", "Comprendre"),
    6: (14, "L'art du Fact-Checking : comment ne pas gober les hallucinations de l'IA", "Limites"),
    7: (39, "Responsabilité : vous êtes le seul signataire de ce que produit l'IA", "Risques et cadre"),
    8: (4, 'Le contexte : la "mémoire vive" de l\'IA (ce qu\'elle voit à un instant T)', "Comprendre"),
    9: (18, "L'art de la discussion : pourquoi il faut itérer plutôt que tout demander d'un coup", "Prompting"),
    10: (17, "Les pièges du prompt : flou artistique et overdose d'instructions", "Prompting"),
    11: (28, "Mise en situation : préparer une réunion ou un brief client avec l'IA", "Au travail"),
    12: (40, "Confidentialité : où vont vraiment les données que vous tapez ?", "Risques et cadre"),
    13: (5, "Pourquoi l'IA oublie : la vérité sur la mémoire d'une session à l'autre", "Comprendre"),
    14: (12, "Zéro pointé : pourquoi l'IA est structurellement nulle en calcul mental", "Limites"),
}

ANNEXES = {"À ESSAYER": "À essayer", "A ESSAYER": "À essayer", "LE PIÈGE": "Le piège", "LE PIEGE": "Le piège"}


def lire_html(slug: str) -> dict:
    with open(os.path.join("pastilles", slug, "pastille.html"), encoding="utf-8") as handle:
        contenu = handle.read()
    alts = re.findall(r'<img[^>]*alt="([^"]*)"', contenu)
    minutes = re.search(r"(\d+) min de lecture", contenu)
    rubrique = re.search(r"&middot;&nbsp;&nbsp;([^<]+)", contenu)
    annexe = next((valeur for label, valeur in ANNEXES.items() if label in contenu), None)
    # Les attributs alt portent des entites HTML legitimes (&quot; obligatoire dans
    # un attribut entre guillemets doubles): on les decode pour les donnees.
    return {
        "titre_retenu": html.unescape(alts[0]) if alts else "",
        "alt_schema": html.unescape(alts[1]) if len(alts) > 1 else "",
        "temps_de_lecture": f"{minutes.group(1)} min de lecture" if minutes else "",
        "rubrique_affichee": html.unescape(rubrique.group(1)).strip() if rubrique else "",
        "bloc_annexe": annexe,
    }


def normalise(slug: str) -> dict:
    numero = int(slug.split("-", 1)[0])
    position, titre_canonique, rubrique = CANONIQUE[numero]
    chemin = os.path.join("pastilles", slug, "meta.json")
    with open(chemin, encoding="utf-8") as handle:
        ancien = json.load(handle)
    rendu = lire_html(slug)

    meta = {
        "slug": slug,
        "sujet": ancien["sujet"],
        "numero_envoi": numero,
        "total_serie": TOTAL_SERIE,
        "position_canonique": position,
        "titre_canonique": titre_canonique,
        "titre_retenu": rendu["titre_retenu"],
        "rubrique": rubrique,
        "temps_de_lecture": rendu["temps_de_lecture"],
        "bloc_annexe": rendu["bloc_annexe"],
        "texte_alternatif_schema": rendu["alt_schema"],
        "gel_du_corps": "integral" if not os.path.exists(
            os.path.join("pastilles", slug, "gel-exceptions.json")
        ) else "derogation tracee dans gel-exceptions.json",
    }
    if rendu["rubrique_affichee"] != rubrique:
        raise SystemExit(f"{slug}: rubrique affichee '{rendu['rubrique_affichee']}' != '{rubrique}'")
    with open(chemin, "w", encoding="utf-8") as handle:
        json.dump(meta, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return meta


def section_vigilance(slug: str) -> str:
    chemin = os.path.join("pastilles", slug, "pastille.md")
    with open(chemin, encoding="utf-8") as handle:
        texte = handle.read()
    trouve = re.search(r"##\s*Points de vigilance\s*(.*?)(?=\n##|\Z)", texte, re.S)
    return trouve.group(1).strip() if trouve else "(aucun point signale)"


def main() -> None:
    slugs = sorted(os.listdir("pastilles"))
    slugs = [s for s in slugs if os.path.isdir(os.path.join("pastilles", s))]
    metas = [normalise(slug) for slug in slugs]

    lignes = [
        "# Pastilles reexportees",
        "",
        "Les pastilles deja diffusees, reprises au gabarit actuel de la serie. Le corps du",
        "texte est inchange: la reprise ajoute les cadres que le gabarit impose (bandeau,",
        "encadre L'essentiel, legende du schema, bloc annexe), les textes alternatifs",
        "rediges d'apres les visuels, les sources qui corroborent le message et un prompt",
        "image regenere.",
        "",
        "Chaque dossier contient `pastille.html` (a coller dans le client de messagerie),",
        "`pastille.eml` (ouvrable directement pour renvoi), les deux visuels, `meta.json` et",
        "`pastille.md` (le livrable lisible, avec sources et points de vigilance).",
        "",
        "Le bandeau porte le numero d'ENVOI, pas le rang dans la liste des 45; la rubrique,",
        "elle, suit le sujet reel, donc la position canonique.",
        "",
        "| Envoi | Rubrique | Position canonique | Titre retenu | Bloc annexe |",
        "| --- | --- | --- | --- | --- |",
    ]
    for meta in metas:
        annexe = meta["bloc_annexe"] or "aucun"
        lignes.append(
            f"| {meta['numero_envoi']} / {TOTAL_SERIE} | {meta['rubrique']} | "
            f"{meta['position_canonique']} | {meta['titre_retenu']} | {annexe} |"
        )
    lignes += ["", "## Points de vigilance releves a la reprise", ""]
    lignes.append(
        "Le corps du texte etant gele, ces constats n'ont pas ete corriges: ils sont "
        "remontes tels quels pour arbitrage. Seule exception, decidee explicitement: les "
        "tirets cadratins de la pastille 11, remplaces par des parentheses."
    )
    lignes.append("")
    for meta in metas:
        lignes.append(f"### {meta['numero_envoi']} / {TOTAL_SERIE} - {meta['titre_retenu']}")
        lignes.append("")
        lignes.append(section_vigilance(meta["slug"]))
        lignes.append("")

    with open(os.path.join("pastilles", "README.md"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(lignes).rstrip() + "\n")
    print(f"{len(metas)} meta.json normalises, pastilles/README.md genere")


if __name__ == "__main__":
    main()
