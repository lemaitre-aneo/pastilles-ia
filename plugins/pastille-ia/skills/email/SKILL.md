---
description: Fabrique le courriel de diffusion d'une pastille LLM déjà rédigée et déjà illustrée: un fichier .msg Outlook, prêt à compléter et à envoyer, contenant le corps HTML au gabarit de la série et les deux visuels en pièces jointes affichées dans le corps. Utilise ce skill dès qu'on te demande de générer, produire, fabriquer ou mettre en forme le mail, l'email, le courriel, le .msg ou la version diffusable d'une pastille, typiquement juste après avoir collé dans la conversation l'illustration-titre et le schéma générés par Gemini. Produit aussi un HTML conservable aux couleurs de la série, visuels incorporés, importable dans Notion tel quel, portant en commentaire le dossier complet de la pastille pour permettre de la reprendre. Utilise-le aussi pour régénérer un courriel après une retouche du texte. Pour écrire la pastille elle-même, utilise generate; pour retoucher son texte, applique la retouche directement quand son contexte est dans la conversation, et n'appelle refine que si elle a été recollée sans son contexte de production.
---

# Fabrique du courriel d'une pastille (.msg Outlook)

## Ce que fait ce skill
Prend une pastille dont le texte est validé et dont les deux visuels ont été générés, puis produit un `.msg`: brouillon non envoyé, sujet au format de la série, corps HTML au gabarit, illustration-titre et schéma attachés et affichés dans le corps par référence `cid:`. Le fichier s'ouvre dans Outlook, il ne reste qu'à renseigner les destinataires et à envoyer.

La même passe écrit un second fichier, destiné à rester: un HTML sémantique habillé aux teintes de la série, nommé d'après le titre, visuels incorporés. Il s'importe dans Notion tel quel, se lit dans un navigateur et tient lieu d'archive. Voir « Les deux artefacts ».

Frontière avec les autres skills: `generate` écrit la pastille et produit le prompt d'images, `refine` reprend une pastille dont le contexte est perdu, en relisant son artefact HTML quand il existe, `review` la juge sans y toucher, et ce skill ne s'occupe que de la mise en courriel. Il ne réécrit jamais le texte: si une correction rédactionnelle apparaît en route, signale-la et propose de la traiter, ne la décide pas ici. Si l'utilisateur accepte, applique-la directement quand le dossier de la pastille est dans la conversation (voir la spec partagée, section « Faire évoluer une pastille »); `refine` ne sert que si le texte a été recollé sans son contexte. Si la correction est structurelle (changement d'axe, restructuration), c'est `generate` qui régénère, et les deux visuels sont alors à refaire dans Gemini avant de revenir ici. Dans tous les cas, le texte corrigé oblige à refabriquer le `.msg`, et à vérifier que les visuels n'ont pas été périmés par la correction.

## Spec partagée (à lire en premier)
Les normes de la série vivent dans un fichier partagé, source unique commune aux quatre skills. La section qui te concerne au premier chef est « Gabarit de diffusion », mais lis aussi les Règles du texte: c'est ce qui te dit combien de puces et de paragraphes sont admissibles, et ce que le courriel doit refuser.

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

Le webp, la transparence et les bandes de fond sont traités plus loin par le script de construction: ne fais ni la conversion ni le rognage à la main.

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
  "image_schema": "collee-2.png",
  "sources": [{"titre": "Une source", "url": "https://..."}, "Une source sans lien"]
}
```

Points de vigilance: `numero` est le numéro de diffusion donné par l'utilisateur et `position_liste` la place du sujet dans la liste des 45, d'où la rubrique est déduite; les deux sont indépendants, ici 13 et 5. `rubrique` et `temps_lecture` peuvent être écrits en dur pour forcer une valeur, sinon ils sont calculés. `schema_apres` est le rang du paragraphe après lequel le schéma s'insère, donc l'avant-dernier, puisque le dernier paragraphe porte l'enjeu et se lit après le visuel. `annexe` est facultative et plafonnée à un bloc, `style` valant `essayer` ou `piege`. Le texte alternatif de l'illustration-titre n'est pas dans la fiche: c'est le titre exact, la norme l'impose. `mention_ia` et `signature` ont des valeurs par défaut, ne les redéclare que pour les changer. `sources` est facultatif mais recommandé: reprends les références du brief de recherche, chacune sous forme de chaîne ou d'objet `titre` plus `url`. Elles n'apparaissent que dans le HTML conservé, jamais dans le courriel.

### 4. Construire et contrôler
```
python3 ${CLAUDE_SKILL_DIR}/scripts/build.py fiche.json \
    --msg "pastille NN accroche.msg" --html "pastille NN accroche.html"
python3 ${CLAUDE_SKILL_DIR}/scripts/verify.py "pastille NN accroche.msg" \
    pastille-NN-illustration-titre.png pastille-NN-schema.png \
    --html "pastille NN accroche.html"
```

Deux artefacts, tous deux issus de la même fiche et du même code de rendu: le `.msg` pour diffuser, le HTML pour importer, lire et conserver. Voir « Les deux artefacts ».

`build.py` écrit à côté de la fiche les deux PNG qu'il attache réellement, `pastille-NN-illustration-titre.png` et `pastille-NN-schema.png`. Ce sont eux qu'il faut passer à `verify.py`, et non les images d'origine: celles-ci ont pu être converties depuis le webp, aplaties ou rognées, auquel cas elles ne correspondent plus. Ce sont eux, aussi, qui sont incorporés dans le HTML.

Un mot sur le rognage, actif par défaut. Un schéma sorti de Gemini arrive souvent avec de larges bandes de fond en haut et en bas, et la tentation est de le rogner dans Outlook: ne le fais pas et ne le propose pas, car le rognage y réécrit les dimensions de l'image en dur, emporte le `max-width` et donne au bloc une largeur minimale qu'il ne sait plus réduire. Le script mesure donc les bandes de fond quasi blanc, garde 16 pixels de respiration et rogne avant de construire, en annonçant ce qu'il a retiré. Il s'abstient dans deux cas, en le disant: une image entièrement blanche, et un rognage qui emporterait plus de 60% de la surface, signe d'une détection douteuse plutôt que d'une vraie marge. Le drapeau `--sans-rognage` conserve les bandes et se contente de signaler celles qu'il a vues. Une illustration-titre pleine page n'est jamais concernée, faute de marge à retirer.

`verify.py` rouvre le fichier avec un parseur indépendant et sort en erreur si une contrainte est violée: conteneur invalide, propriété manquante, pièce jointe qui ne correspond pas à sa source, `cid` non référencé, police entre apostrophes, couleur portée par une cellule, apostrophe droite restante, sujet ambigu au codage. Avec `--html`, il contrôle en plus l'artefact conservé: ses deux images doivent être incorporées et plus aucune référence `cid:` ne doit rester, sans quoi le fichier ne se suffit pas à lui-même et n'affichera plus ses visuels une fois déplacé; et il ne doit porter qu'une table, celle du bandeau, sans imbrication, faute de quoi il redevient de la mise en page en tables, ce qu'un importeur aplatit mal. Ne livre rien dont la vérification échoue.

Le sujet ambigu mérite un mot, car c'est le seul contrôle dont le correctif est éditorial. Le sujet est le seul texte accentué du courriel, et Outlook (new) le rabat en octets cp1252 avant de le relire dans un codage sur deux octets: un sujet qui s'y décode entièrement s'affiche `[Pastille IA de l掗t閉 #7 : ...`, un sujet qui fait échouer ce décodage est intégralement sauvé par le repli. Il suffit d'un accent suivi d'un espace ou d'une ponctuation, et c'est le préfixe de série qui devrait le porter, puisqu'il est sur tous les courriels (voir « Gabarit de diffusion »). Quand l'alerte tombe, dis-le à l'utilisateur avec le rendu erroné sous les yeux et laisse-le trancher entre corriger le préfixe une fois pour toutes et reformuler ce titre-ci; ne réécris pas son titre de ton propre chef, et ne lui retire jamais ses accents en silence.

Contrôle ensuite le rendu visuel du HTML, à deux largeurs, en dessous et au dessus du plafond:

```
/opt/pw-browsers/chromium-1194/chrome-linux/chrome --headless --disable-gpu --no-sandbox \
  --hide-scrollbars --window-size=520,2400 --virtual-time-budget=3000 \
  --screenshot=apercu-520.png --default-background-color=FFFFFFFF \
  "file://$PWD/pastille NN accroche.html"
```

Regarde les captures avant de livrer. Le chemin de Chromium peut différer, adapte-le; s'il n'y a pas de navigateur, dis-le à l'utilisateur plutôt que d'annoncer un contrôle que tu n'as pas fait.

### 5. Livrer
Livre les deux fichiers. Dis en une ligne ce que contient le courriel (brouillon non envoyé, sans destinataire, sujet exact), et pour le HTML, qu'il s'importe dans Notion tel quel et qu'il tient d'archive. Rappelle la seule limite réelle: il n'y a pas d'Outlook dans l'environnement, donc la validation finale du rendu appartient à l'utilisateur. Ne prétends jamais avoir vérifié dans Outlook.

## Les deux artefacts
Un seul rendu, deux sorties, et rien de plus: tout ce qui n'était ni diffusable ni conservable a été retiré.

- **`pastille NN accroche.msg`**, pour diffuser. Brouillon Outlook, images en pièces jointes référencées par `cid:`, corps optimisé pour le moteur de rendu de Word. C'est le seul artefact destiné à être envoyé.
- **`pastille NN accroche.html`**, pour importer, lire et conserver. HTML sémantique aux teintes de la série, visuels incorporés en base64, donc un seul fichier qui se suffit à lui-même. Il s'importe dans Notion tel quel, s'ouvre dans n'importe quel navigateur des années plus tard, et sert de source aux captures de contrôle.

Ce second fichier fait donc les trois métiers à la fois, ce qui a permis d'abandonner les variantes qui les séparaient: le Markdown, la copie fidèle du courriel, et la version aux images voisines. L'archive de la pastille, ce sont ce fichier et le dossier qui le contient, avec la fiche et les PNG d'origine.

### Nommer le fichier: c'est lui qui nomme la page
**Les deux fichiers portent le même nom, `pastille NN accroche`, à l'extension près, et avec des espaces.** L'accroche les rend reconnaissables dans un dossier, et côté HTML elle décide du titre de la page importée. Deux raisons pour les espaces, l'une et l'autre constatées à l'usage:

- Notion nomme la page importée d'après le **nom du fichier**, et non d'après le `h1` du document. Un artefact appelé `pastille.html` donne une page appelée « pastille ».
- Les **tirets ne survivent pas** à toutes les chaînes de téléchargement, qui les suppriment et recollent les mots en un bloc illisible. L'espace, lui, passe, et il donne un titre de page correct.

`build.py` calcule le nom attendu depuis le titre, en gardant l'accroche jusqu'au deux-points, et le rappelle pour chacun des deux fichiers si celui que tu as donné diffère: reprends-le tel quel. Pense aux guillemets dans les commandes, le nom contenant des espaces.

### Ce que l'artefact garantit, et pourquoi
- **Visuels incorporés.** Un HTML qui pointe vers des PNG voisins cesse d'afficher ses images dès qu'on le déplace: c'est un aperçu, pas un artefact. Ici tout est dans le fichier. Revers à connaître: le base64 gonfle les visuels d'un tiers et l'import Notion est plafonné à 5 Mo sur le plan gratuit, 50 Mo sinon. `build.py` alerte au-delà de 4,5 Mo; dans ce cas, régénère des visuels plus légers avant de refabriquer.
- **Titre en tête, masqué au rendu.** Un `h1` réduit à un pixel et détouré, placé avant le bandeau. En tête, il ouvre la page importée; masqué, il ne fait pas doublon avec l'illustration qui le porte déjà; masqué visuellement plutôt que par `display:none`, il reste annoncé par un lecteur d'écran.
- **Le bandeau est une table** d'une ligne et trois cellules, seule table du fichier et seule exception à son balisage sans tables. Une table simple s'importe comme une table, donc le compte, la rubrique et le temps de lecture restent séparés au lieu d'arriver en une ligne de texte. Les cellules extérieures se réduisent à leur contenu et celle du milieu prend le reste, sans quoi le numéro s'éloigne de la rubrique. La cellule de droite commence par une espace insécable, invisible dans une cellule alignée à droite, qui sert de repli si un importeur aplatit quand même la table.
- **Les sources dans un `<details>` replié**, en pied de document. Ce choix règle leur visibilité sans recourir au CSS, qu'un importeur ignore: un navigateur replie nativement l'élément, et Notion exporte ses blocs dépliants sous cette forme, donc il devrait les relire comme tels. Le courriel, lui, ne les porte jamais, la norme de la série les réservant à la vérification; mais une archive sans ses références ne peut plus être rejugée dans un an.
- **Styles en ligne, pas de feuille `<style>`.** Un importeur qui ne lit pas le CSS ignore une feuille sans dommage, mais un importeur naïf peut aussi en recracher le contenu au milieu de la page. En ligne, ce risque n'existe pas.

### Ce que Notion garde, et ce qu'il ne garde pas
La structure des blocs, oui, et c'est le but. Les couleurs, non: seule la légende y ressort en gris, et c'est Notion qui colore nativement ses légendes, pas un style qui survivrait. L'habillage aux teintes de la série vaut donc pour la lecture du fichier dans un navigateur. À noter que la couleur de texte de Notion est une palette de noms, pas des valeurs hexadécimales: les teintes exactes de la charte n'y sont de toute façon pas reproductibles, même en construisant la page par l'API.

Ne promets donc pas un rendu Notion identique au courriel. L'encadré « L'essentiel » et le bloc annexe arrivent en citations, à convertir en callout côté Notion si l'utilisateur le souhaite.

### Où écrire ces fichiers
Un dossier par pastille, pour que le dossier soit l'archive: `sorties/pastille-NN-accroche/`, contenant la fiche JSON, les visuels d'origine, les deux PNG produits, le `.msg` et le HTML. Le HTML seul suffirait d'ailleurs à tout reconstruire; le dossier existe pour repartir d'une fiche lisible. Le dossier `sorties/` n'est pas suivi par git (voir `.gitignore`): ce dépôt porte l'outillage, pas les pastilles diffusées. En session cloud, pense donc à récupérer les fichiers avant la fin de la session, ou dis à l'utilisateur qu'ils disparaitront avec le conteneur.

## Ce que le courriel garantit, et pourquoi
Ces choix sont des corrections de défauts constatés dans Outlook, pas des préférences. Ne les défais pas sans raison, et si tu les modifies, reporte-les dans le gabarit partagé.

- **Largeur fluide, plafonnée.** Aucune largeur de colonne imposée: la colonne suit la fenêtre et cesse de s'étirer au delà du plafond (1000 pixels). Comme Word ignore `max-width`, le plafond lui est donné en plus par un commentaire conditionnel `[if mso]`.
- **Images à taille fixe**, 600 pixels pour l'illustration-titre et 560 pour le schéma, avec hauteur automatique: elles ne sont jamais étirées au delà de leur taille nominale et se réduisent seulement si la fenêtre passe en dessous. **La légende du schéma partage ce plafond et ce centrage**, donc son bord gauche est celui de l'image: une légende qui dépasse le visuel qu'elle décrit se lit comme un paragraphe de plus. Word ignorant `max-width`, le plafond de la légende lui est donné en plus par commentaire conditionnel, comme celui de la colonne.
- **Bandes de fond rognées à la construction.** Un visuel arrive fréquemment avec de larges marges blanches, et les rogner dans le client de messagerie est un piège: Outlook y réécrit les dimensions en dur, ce qui emporte le `max-width` et fige la largeur minimale du bloc. Le rognage a donc lieu en amont, sur le fichier, pour qu'il n'y ait plus de raison d'y toucher ensuite.
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
