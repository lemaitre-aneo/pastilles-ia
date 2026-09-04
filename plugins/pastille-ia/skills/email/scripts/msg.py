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

"""Assemblage d'un .msg Outlook (format MS-OXMSG) avec pièces jointes en ligne.

Le message produit est un brouillon non envoyé: il s'ouvre dans Outlook prêt à
recevoir ses destinataires. Les images sont attachées et référencées par
`cid:` depuis le corps HTML, avec le marqueur ATT_MHTML_REF qui indique à
Outlook qu'elles appartiennent au corps et non à la barre de pièces jointes.
"""
import datetime
import struct

import cfb

PT_LONG, PT_BOOL, PT_STR, PT_BIN, PT_TIME = 0x0003, 0x000B, 0x001F, 0x0102, 0x0040
LISIBLE_MODIFIABLE = 0x00000006

CLSID_MESSAGE = bytes.fromhex("0b0d020000000000c000000000000046")


def _filetime(dt):
    origine = datetime.datetime(1601, 1, 1, tzinfo=datetime.timezone.utc)
    return int((dt - origine).total_seconds() * 10_000_000)


class Proprietes:
    """Propriétés d'un stockage: les valeurs fixes vont dans le flux de
    propriétés, les variables dans leur propre flux __substg1.0_."""

    def __init__(self):
        self.lignes = []
        self.flux = []

    def entier(self, pid, valeur):
        self.lignes.append(((pid << 16) | PT_LONG, struct.pack("<iI", valeur, 0)))

    def booleen(self, pid, valeur):
        self.lignes.append(((pid << 16) | PT_BOOL,
                            struct.pack("<HHI", 1 if valeur else 0, 0, 0)))

    def horodatage(self, pid, dt):
        self.lignes.append(((pid << 16) | PT_TIME, struct.pack("<Q", _filetime(dt))))

    def chaine(self, pid, valeur):
        data = valeur.encode("utf-16-le")
        tag = (pid << 16) | PT_STR
        self.lignes.append((tag, struct.pack("<II", len(data) + 2, 0)))
        self.flux.append((f"__substg1.0_{tag:08X}", data))

    def binaire(self, pid, data):
        tag = (pid << 16) | PT_BIN
        self.lignes.append((tag, struct.pack("<II", len(data), 0)))
        self.flux.append((f"__substg1.0_{tag:08X}", data))

    def poser(self, stockage, entete):
        for nom, data in self.flux:
            stockage.add(cfb.Entry(nom, cfb.STREAM, data))
        corps = b"".join(struct.pack("<II", tag, LISIBLE_MODIFIABLE) + val
                         for tag, val in sorted(self.lignes, key=lambda l: l[0]))
        stockage.add(cfb.Entry("__properties_version1.0", cfb.STREAM, entete + corps))


def ecrire(chemin, sujet, html, texte, images, horodatage=None):
    """images: liste de dicts {cid, nom, nom_court, donnees, type_mime}."""
    maintenant = horodatage or datetime.datetime.now(datetime.timezone.utc)
    for img in images:
        if f'cid:{img["cid"]}' not in html:
            raise ValueError(f'le cid {img["cid"]} est absent du corps HTML')

    racine = cfb.Entry("Root Entry", cfb.ROOT, clsid=CLSID_MESSAGE)
    nameid = racine.add(cfb.Entry("__nameid_version1.0", cfb.STORAGE))
    for tag in ("00020102", "00030102", "00040102"):
        nameid.add(cfb.Entry(f"__substg1.0_{tag}", cfb.STREAM, b""))

    haut = Proprietes()
    haut.chaine(0x001A, "IPM.Note")                 # PidTagMessageClass
    haut.chaine(0x0037, sujet)                      # PidTagSubject
    haut.chaine(0x0E1D, sujet)                      # PidTagNormalizedSubject
    haut.chaine(0x0070, sujet)                      # PidTagConversationTopic
    haut.chaine(0x1000, texte)                      # PidTagBody
    haut.binaire(0x1013, html.encode("utf-8"))      # PidTagHtml
    haut.entier(0x0E07, 0x00000009)                 # MessageFlags: non envoyé, lu
    haut.entier(0x340D, 0x00040000)                 # StoreSupportMask: unicode
    haut.entier(0x5909, 2)                          # MessageEditorFormat: HTML
    haut.entier(0x3FDE, 65001)                      # InternetCodepage: utf-8
    haut.entier(0x3FFD, 65001)                      # MessageCodepage
    haut.booleen(0x0E1B, bool(images))              # HasAttachments
    haut.horodatage(0x3007, maintenant)
    haut.horodatage(0x3008, maintenant)
    entete = (b"\x00" * 8 + struct.pack("<IIII", 0, len(images), 0, len(images))
              + b"\x00" * 8)
    haut.poser(racine, entete)

    for i, img in enumerate(images):
        st = racine.add(cfb.Entry(f"__attach_version1.0_#{i:08X}", cfb.STORAGE))
        p = Proprietes()
        p.entier(0x0FFE, 7)                         # ObjectType: MAPI_ATTACH
        p.entier(0x0E21, i)                         # AttachNumber
        p.entier(0x3705, 1)                         # AttachMethod: par valeur
        p.entier(0x370B, -1)                        # RenderingPosition: hors flux
        p.entier(0x0E20, len(img["donnees"]))       # AttachSize
        p.entier(0x3714, 0x00000004)                # AttachFlags: ATT_MHTML_REF
        p.booleen(0x7FFE, True)                     # AttachmentHidden: en ligne
        p.binaire(0x3701, img["donnees"])           # AttachDataBinary
        p.chaine(0x3704, img["nom_court"])          # AttachFilename
        p.chaine(0x3707, img["nom"])                # AttachLongFilename
        p.chaine(0x3703, "." + img["nom"].rsplit(".", 1)[-1])
        p.chaine(0x370E, img["type_mime"])          # AttachMimeTag
        p.chaine(0x3712, img["cid"])                # AttachContentId
        p.chaine(0x3001, img["nom"])                # DisplayName
        p.horodatage(0x3007, maintenant)
        p.horodatage(0x3008, maintenant)
        p.poser(st, b"\x00" * 8)

    cfb.write(racine, chemin)
    return chemin
