---
description: Fabrique le courriel de diffusion d'une pastille LLM déjà rédigée et déjà illustrée: un fichier .msg Outlook, prêt à compléter et à envoyer, contenant le corps HTML au gabarit de la série et les deux visuels en pièces jointes affichées dans le corps. Utilise ce skill dès qu'on te demande de générer, produire, fabriquer ou mettre en forme le mail, l'email, le courriel, le .msg ou la version diffusable d'une pastille, typiquement juste après avoir collé dans la conversation l'illustration-titre et le schéma générés par Gemini. Utilise-le aussi pour régénérer un courriel après une retouche du texte. Pour écrire la pastille elle-même, utilise generate; pour retoucher son texte, refine.
---

# Fabrique du courriel d'une pastille (.msg Outlook)

## Ce que fait ce skill
Prend une pastille dont le texte est validé et dont les deux visuels ont été générés, puis produit un `.msg` unique: brouillon non envoyé, sujet au format de la série, corps HTML au gabarit, illustration-titre et schéma attachés et affichés dans le corps par référence `cid:`. Le fichier s'ouvre dans Outlook, il ne reste qu'à renseigner les destinataires et à envoyer.

Frontière avec les autres skills: `generate` écrit la pastille et produit le prompt d'images, `refine` retouche un texte existant, et ce skill ne s'occupe que de la mise en courriel. Il ne réécrit jamais le texte: si une correction rédactionnelle apparaît en route, signale-la et propose `refine`, ne la décide pas ici.

## Spec partagée (à lire en premier)
Les normes de la série vivent dans un fichier partagé, source unique commune aux trois skills. La section qui te concerne au premier chef est « Gabarit de diffusion », mais lis aussi les Règles du texte: c'est ce qui te dit combien de puces et de paragraphes sont admissibles, et ce que le courriel doit refuser.

`${CLAUDE_SKILL_DIR}/references/regles-pastille.md`

## Entrées attendues
Ce skill est autonome: il ne suppose pas qu'un autre skill vient de tourner. Le texte peut sortir d'une génération faite juste avant, d'un raffinement, ou d'un simple copier-coller de l'utilisateur quand la conversation d'origine est perdue. Ce qui compte est ce qui est présent maintenant.

1. Le contenu de la pastille: titre retenu, les puces de « L'essentiel », les 3 ou 4 paragraphes, la légende du schéma, le texte alternatif du schéma, et le bloc annexe s'il y en a un. S'il vient d'être produit dans la conversation, reprends-le tel quel sans le réécrire. Sinon demande-le, ou demande à l'utilisateur de le recoller. Si la légende du schéma ou son texte alternatif manquent, demande-les: ne les invente pas, la légende dit ce qu'il faut voir dans un visuel que tu ne peux pas regarder.
2. Le numéro de diffusion. Il vient de l'utilisateur et prévaut toujours, même s'il contredit la liste des 45: cette liste est un inventaire de sujets, pas un ordre de diffusion. Si aucun numéro n'a été donné, propose la position du sujet dans la liste et demande confirmation avant de construire; ne la retiens pas en silence.
3. Les deux images, illustration-titre puis schéma, collées dans la conversation ou déposées sur le disque.

Deux champs ne sont pas à réclamer, le script les déduit: la rubrique, à partir de la position du sujet dans la liste des 45 (champ `position_liste`), et le temps de lecture, à partir du nombre de mots. Les valeurs déduites sont affichées à la construction, vérifie-les.

Si une seule image est disponible, arrête-toi et demande la seconde: le schéma est systématique dans la série, un courriel sans schéma n'est pas conforme.

## Processus

### 1. Récupérer les images
Une image collée dans le chat n'est pas un fichier: elle vit dans le transcript de session. Cherche d'abord des fichiers sur le disque (l'utilisateur a pu les déposer), sinon extrais-les du transcript:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/extract_images.py --dossier <dossier de travail> --nombre 2
```

Le script écrit les dernières images de la conversation, dans l'ordre de collage, et affiche leurs dimensions. Sers-toi de ces dimensions pour identifier laquelle est laquelle sans te tromper: l'illustration-titre est en 16:9, le schéma en 4:3. Si l'ordre et les proportions se contredisent, demande confirmation plutôt que de deviner.

Le webp et la transparence sont convertis plus loin par le script de construction: ne fais pas la conversion à la main.

### 2. Vérifier que les visuels correspondent au texte
Les images sont des artefacts déjà rendus, elles ne suivent pas les retouches du texte. L'illustration-titre affiche un titre, et tu ne peux pas le lire: rien ne garantit que ce soit le titre retenu.

Si les deux visuels viennent d'être générés dans cette conversation à partir du texte courant, il n'y a rien à faire. Sinon, et c'est le cas courant quand le texte a été recollé ou raffiné, demande confirmation à l'utilisateur sur deux points avant de construire: que l'illustration porte bien le titre retenu au caractère près, et que les libellés du schéma correspondent encore au mécanisme exposé dans les premiers paragraphes. Si l'un des deux ne colle plus, le visuel est périmé: il faut le régénérer dans Gemini avant de fabriquer le courriel, sans quoi le bandeau, le corps et l'image ne raconteront pas la même histoire.

### 3. Écrire la fiche JSON
Une fiche décrit la pastille, le script fait le reste. Les emphases s'écrivent en markdown (`**gras**`, `*italique*`), la typographie française est appliquée automatiquement: n'ajoute pas d'espaces insécables ni d'apostrophes typographiques à la main, et ne mets pas de HTML dans la fiche.

```json
{
  "numero": 13,
  "total": 45,
  "position_liste": 5,
  "titre": "Titre exact retenu, celui rendu dans l'illustration",
  "prefixe_sujet": "[Pastille IA de l'été]",
  "essentiel": ["Puce 1.", "Puce 2.", "Puce 3."],
  "paragraphes": ["Paragraphe 1", "Paragraphe 2", "Paragraphe 3", "Paragraphe 4"],
  "schema_apres": 3,
  "legende_schema": "Une phrase.",
  "alt_schema": "Ce que montre le schéma, une phrase.",
  "annexe": {"etiquette": "À essayer", "style": "essayer", "texte": "..."},
  "image_titre": "collee-1.png",
  "image_schema": "collee-2.png"
}
```

Points de vigilance: `numero` est le numéro de diffusion donné par l'utilisateur et `position_liste` la place du sujet dans la liste des 45, d'où la rubrique est déduite; les deux sont indépendants, ici 13 et 5. `rubrique` et `temps_lecture` peuvent être écrits en dur pour forcer une valeur, sinon ils sont calculés. `schema_apres` est le rang du paragraphe après lequel le schéma s'insère, donc l'avant-dernier, puisque le dernier paragraphe porte l'enjeu et se lit après le visuel. `annexe` est facultative et plafonnée à un bloc, `style` valant `essayer` ou `piege`. Le texte alternatif de l'illustration-titre n'est pas dans la fiche: c'est le titre exact, la norme l'impose. `mention_ia` et `signature` ont des valeurs par défaut, ne les redéclare que pour les changer.

### 4. Construire et contrôler
```
python3 ${CLAUDE_SKILL_DIR}/scripts/build.py fiche.json --msg pastille-NN.msg --apercu apercu.html
python3 ${CLAUDE_SKILL_DIR}/scripts/verify.py pastille-NN.msg <image titre> <image schema>
```

`verify.py` rouvre le fichier avec un parseur indépendant et sort en erreur si une contrainte est violée: conteneur invalide, propriété manquante, pièce jointe qui ne correspond pas à sa source, `cid` non référencé, police entre apostrophes, couleur portée par une cellule, apostrophe droite restante. Ne livre pas un fichier dont la vérification échoue.

Contrôle ensuite le rendu visuel de l'aperçu, à deux largeurs, en dessous et au dessus du plafond:

```
/opt/pw-browsers/chromium-1194/chrome-linux/chrome --headless --disable-gpu --no-sandbox \
  --hide-scrollbars --window-size=520,2400 --virtual-time-budget=3000 \
  --screenshot=apercu-520.png --default-background-color=FFFFFFFF file://$PWD/apercu.html
```

Regarde les captures avant de livrer. Le chemin de Chromium peut différer, adapte-le; s'il n'y a pas de navigateur, dis-le à l'utilisateur plutôt que d'annoncer un contrôle que tu n'as pas fait.

### 5. Livrer
Livre le `.msg` en fichier joint. Dis en une ligne ce que contient le courriel (brouillon non envoyé, sans destinataire, sujet exact) et rappelle la seule limite réelle: il n'y a pas d'Outlook dans l'environnement, donc la validation finale du rendu appartient à l'utilisateur. Ne prétends jamais avoir vérifié dans Outlook.

## Ce que le courriel garantit, et pourquoi
Ces choix sont des corrections de défauts constatés dans Outlook, pas des préférences. Ne les défais pas sans raison, et si tu les modifies, reporte-les dans le gabarit partagé.

- **Largeur fluide, plafonnée.** Aucune largeur de colonne imposée: la colonne suit la fenêtre et cesse de s'étirer au delà du plafond (1000 pixels). Comme Word ignore `max-width`, le plafond lui est donné en plus par un commentaire conditionnel `[if mso]`.
- **Images à taille fixe**, 600 pixels pour l'illustration-titre et 560 pour le schéma, avec hauteur automatique: elles ne sont jamais étirées au delà de leur taille nominale et se réduisent seulement si la fenêtre passe en dessous.
- **Couleurs déclarées là où Word les lit.** Word n'hérite pas la couleur d'un `<td>` vers son texte, il applique celle du thème de rédaction. Chaque bloc porte donc sa couleur sur l'élément qui porte le texte, `color` est déclaré avant `font-family` (un nom de police entre apostrophes casse l'analyse CSS de Word et emporte la fin de la déclaration), les noms de police ne sont jamais quotés, et tout est doublé en balises présentationnelles `<font color face>`, `<b>`, `<i>`.
- **Typographie française** appliquée par le code: espace insécable avant `:` `;` `!` `?`, apostrophes typographiques, dans le corps HTML comme dans la version texte.
- **Corps en entités ASCII**, pour ne dépendre d'aucune détection d'encodage côté client.
- **Images en ligne**, référencées par `cid:`, marquées `ATT_MHTML_REF` et masquées de la liste des pièces jointes. Si un client n'affiche pas les images dans le corps, c'est ce marquage qu'il faut basculer.
- **Sujet** au format `[Prefixe] #NN : Titre`, en espaces ordinaires: les insécables et la recherche des messageries font mauvais ménage. Un titre qui contient déjà un deux-points en produit deux, c'est accepté.

## Gabarit partagé
`plugins/pastille-ia/shared/template-pastille.html` est produit par le même code que le courriel réel, avec un contenu de remplacement:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/build.py --gabarit plugins/pastille-ia/shared/template-pastille.html
```

Régénère-le après toute modification du rendu, pour qu'il ne prenne pas de retard sur le générateur. C'est la version à coller à la main dans un client de messagerie si le `.msg` ne peut pas servir.

## Dépendances
`olefile` pour la vérification, `pillow` pour la conversion des images (webp, transparence). Installe-les si elles manquent (`pip install olefile pillow`). Le reste est de la bibliothèque standard: le conteneur `.msg` est écrit par `scripts/cfb.py`, sans dépendance.
