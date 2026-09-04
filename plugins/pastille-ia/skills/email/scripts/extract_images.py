#!/usr/bin/env python3
# pastille-ia: outils multi-agents pour les pastilles pédagogiques sur les LLM.
# Copyright (C) 2026 ANEO
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Récupère les images collées dans la conversation.

Une image collée dans le chat n'existe pas sur le disque: elle vit dans le
transcript de session. Ce script la retrouve et l'écrit en fichier.

    python3 extract_images.py --dossier . --nombre 2
    python3 extract_images.py --transcript chemin.jsonl --dossier .

Les images sont écrites dans l'ordre où elles apparaissent, en ne gardant que
les `--nombre` dernières: illustration-titre puis schéma, si vous les avez
collées dans cet ordre. Vérifiez toujours le résultat, l'ordre de collage est
la seule information disponible.
"""
import argparse
import base64
import glob
import hashlib
import json
import os

EXTENSIONS = {"image/png": "png", "image/jpeg": "jpg", "image/webp": "webp",
              "image/gif": "gif"}


def transcripts():
    motifs = [os.path.expanduser("~/.claude/projects/*/*.jsonl"),
              os.path.expanduser("~/.config/claude/projects/*/*.jsonl")]
    fichiers = [f for motif in motifs for f in glob.glob(motif)]
    return sorted(fichiers, key=os.path.getmtime, reverse=True)


def parcourir(objet, trouvees):
    if isinstance(objet, dict):
        if objet.get("type") == "image" and isinstance(objet.get("source"), dict):
            src = objet["source"]
            if src.get("type") == "base64" and src.get("data"):
                trouvees.append((src.get("media_type", "image/png"), src["data"]))
        for valeur in objet.values():
            parcourir(valeur, trouvees)
    elif isinstance(objet, list):
        for valeur in objet:
            parcourir(valeur, trouvees)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcript", help="transcript à lire (défaut: le plus récent)")
    ap.add_argument("--dossier", default=".", help="où écrire les images")
    ap.add_argument("--nombre", type=int, default=2, help="nombre d'images à garder")
    ap.add_argument("--prefixe", default="collee", help="préfixe des fichiers écrits")
    args = ap.parse_args()

    candidats = [args.transcript] if args.transcript else transcripts()
    if not candidats or not candidats[0]:
        raise SystemExit("aucun transcript trouvé: passez --transcript")

    trouvees = []
    with open(candidats[0], encoding="utf-8", errors="replace") as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                parcourir(json.loads(ligne), trouvees)
            except json.JSONDecodeError:
                continue

    uniques, vues = [], set()
    for type_mime, data in trouvees:
        brut = base64.b64decode(data)
        empreinte = hashlib.sha256(brut).hexdigest()
        if empreinte in vues:
            continue
        vues.add(empreinte)
        uniques.append((type_mime, brut))

    if not uniques:
        raise SystemExit(f"aucune image dans {candidats[0]}")

    os.makedirs(args.dossier, exist_ok=True)
    for i, (type_mime, brut) in enumerate(uniques[-args.nombre:]):
        ext = EXTENSIONS.get(type_mime, "bin")
        chemin = os.path.join(args.dossier, f"{args.prefixe}-{i + 1}.{ext}")
        with open(chemin, "wb") as f:
            f.write(brut)
        print(f"{chemin}  {type_mime}  {len(brut)} octets  {dimensions(brut)}")
    print(f"transcript lu: {candidats[0]}")


def dimensions(brut):
    """Taille en pixels, sans dépendance: PNG et webp lossy suffisent ici."""
    if brut[:8] == b"\x89PNG\r\n\x1a\n":
        import struct
        return "{}x{}".format(*struct.unpack(">II", brut[16:24]))
    if brut[:4] == b"RIFF" and brut[12:16] == b"VP8 ":
        import struct
        largeur, hauteur = struct.unpack("<HH", brut[26:30])
        return f"{largeur & 0x3FFF}x{hauteur & 0x3FFF}"
    return "dimensions inconnues"


if __name__ == "__main__":
    main()
