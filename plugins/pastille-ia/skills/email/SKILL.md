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

1. Le contenu de la pastille: titre retenu, les puces de « L'essentiel », les 3 ou 4 paragraphes, la légende du schéma, le texte alternatif du schéma, et le bloc annexe s'il y en a un. S'il vient d'être produit dans la conversation, reprends-le tel quel sans le réécrire. Sinon demande-le, ou demande à l'utilisateur de le recoller. Si la légende du schéma manque, demande-la: ne l'invente pas, elle dit ce qu'il faut retenir d'un visuel que tu ne peux pas regarder. Le texte alternatif se traite autrement quand l'aperçu des visuels est là: dérive-le de l'aperçu (ce qui est dessiné, la forme et les libellés dans l'ordre de lecture, une à deux phrases) et soumets-le, ce n'est pas de l'invention mais une extraction. Sans aperçu, demande-le comme la légende. Et ne recopie jamais l'une dans l'autre: la légende s'imprime sous l'image et dit quoi en retenir, l'alt est ce que reçoit un lecteur d'écran et dit ce qui est dessiné; `build.py` signale les deux textes identiques.
2. Le numéro de diffusion. Il vient de l'utilisateur et prévaut toujours, même s'il contredit la liste des 45: cette liste est un inventaire de sujets, pas un ordre de diffusion. Si aucun numéro n'a été donné, propose la position du sujet dans la liste et demande confirmation avant de construire; ne la retiens pas en silence. C'est **la seule valeur du sujet à demander**: le préfixe de saison, lui, n'est pas configurable et ne se demande jamais (voir « Le préfixe du sujet ne se demande pas »).
3. La rubrique, quand elle a été décidée. Elle n'est pas un calcul: elle suit l'axe et le contenu de la pastille, et se lit dans le livrable de `generate` ou dans le dossier de l'artefact (voir la spec partagée, section « Numéro et rubrique »). Si tu l'as, écris-la en dur dans la fiche (champ `rubrique`). Si tu ne l'as pas, le script la déduit de la position du sujet dans la liste des 45 (champ `position_liste`), ce qui donne le classement d'inventaire: c'est un défaut raisonnable, pas une vérité, et il faut le confronter à ce que la pastille dit vraiment. Le cas à surveiller est celui d'une pastille dont l'axe a été déplacé en cours de route: le classement d'inventaire la range alors d'après un sujet qu'elle ne traite plus. Un doute se lève en une question à l'utilisateur, pas en laissant le défaut passer.
4. Les deux images, illustration-titre puis schéma, collées dans la conversation ou déposées sur le disque.

Le temps de lecture, lui, se déduit vraiment, à partir du nombre de mots. Les valeurs déduites, rubrique comprise, sont affichées à la construction: vérifie-les.

Si une seule image est disponible, ou aucune, ne fabrique pas le courriel: le schéma est systématique dans la série et l'illustration porte le titre, donc un courriel amputé n'est pas conforme, et `build.py` le refuse. Demande le visuel manquant. Deux nuances utiles avant de bloquer l'utilisateur:
- **L'archive, elle, n'attend pas.** Si le texte est validé et que les visuels ne sont pas encore générés, propose de produire l'artefact seul (voir « Construire et contrôler »): il portera à la place de chaque image manquante un encadré qui la nomme et dit ce qu'elle doit montrer. C'est le bon geste pour une reprise ancienne dont les visuels sont perdus, ou pour conserver une pastille avant de l'illustrer.
- **Ce n'est alors pas la fin du travail**: dis clairement que l'archive est provisoire, qu'elle se refabrique une fois les visuels générés, et que la diffusion reste impossible d'ici là.

## Processus

### 1. Récupérer les images
Une image collée dans le chat n'est pas un fichier: elle vit dans le transcript de session. Cherche d'abord des fichiers sur le disque (l'utilisateur a pu les déposer), sinon extrais-les du transcript:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/extract_images.py --dossier <dossier de travail> --nombre 2
```

Le script écrit les dernières images de la conversation, dans l'ordre de collage, et affiche leurs dimensions. Sers-toi de ces dimensions pour identifier laquelle est laquelle sans te tromper: **l'illustration-titre est toujours en 16:9, le schéma toujours plus compact**, du 4:3 au portrait 4:5 selon la forme qu'il a prise (voir la spec partagée, « Le schéma: forme libre, invariants fermes »). C'est donc la plus large des deux qui est l'illustration-titre, et c'est pour préserver cette distinction que le schéma n'est jamais en 16:9. Si le dossier ou l'aperçu des visuels annonce un format pour le schéma, vérifie qu'il correspond. Si l'ordre et les proportions se contredisent, demande confirmation plutôt que de deviner.

Le webp, la transparence et les bandes de fond sont traités plus loin par le script de construction: ne fais ni la conversion ni le rognage à la main.

### 2. Vérifier que les visuels correspondent au texte
Les images sont des artefacts déjà rendus, elles ne suivent pas les retouches du texte. L'illustration-titre affiche un titre, et tu ne peux pas le lire: rien ne garantit que ce soit le titre retenu.

Si les deux visuels viennent d'être générés dans cette conversation à partir du texte courant, il n'y a rien à faire. Sinon, et c'est le cas courant quand le texte a été recollé ou raffiné, demande confirmation à l'utilisateur sur deux points avant de construire: que l'illustration porte bien le titre retenu au caractère près, et que le schéma corresponde encore au mécanisme exposé dans les premiers paragraphes, sa forme comme ses libellés. L'aperçu des visuels, quand la pastille en a un (dans le livrable ou dans le dossier, champ `apercu_visuels`), dit exactement ce que chaque image devait montrer: cite-le dans ta question plutôt que de demander en l'air, une question précise se vérifie d'un coup d'œil. Si l'un des deux ne colle plus, le visuel est périmé: il faut le régénérer dans Gemini avant de fabriquer le courriel, sans quoi le bandeau, le corps et l'image ne raconteront pas la même histoire.

### 3. Écrire la fiche JSON
Une fiche décrit la pastille, le script fait le reste. Les emphases s'écrivent en markdown (`**gras**`, `*italique*`), la typographie française est appliquée automatiquement: n'ajoute pas d'espaces insécables ni d'apostrophes typographiques à la main, et ne mets pas de HTML dans la fiche.

Écris le texte avec les caractères du français, accents, cédille et e-dans-l'o compris (`cœur`, `œil`): ils traversent toute la chaîne, jusqu'au nom de fichier, qui les délie. `build.py` signale en revanche les caractères que la spec refuse, tiret cadratin, espace fine, accent décomposé (voir la spec partagée, section « Caractères »); ce sont des avertissements, à toi de décider s'il faut retoucher le texte avant de diffuser.

```json
{
  "numero": 13,
  "total": 45,
  "position_liste": 5,
  "titre": "Titre exact retenu, celui rendu dans l'illustration",
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

Points de vigilance: `numero` est le numéro de diffusion donné par l'utilisateur et `position_liste` la place du sujet dans la liste des 45, d'où la rubrique est déduite à défaut de mieux; les deux sont indépendants, ici 13 et 5. Écris `rubrique` en dur dès que la rubrique a été arbitrée sur l'axe et le contenu, ce qui est le cas normal quand la pastille sort de `generate` ou d'un artefact: la déduction par `position_liste` est un repli, et elle ramène le classement d'inventaire. `build.py` refuse une rubrique qui ne fait pas partie des six de la série, pour attraper la faute de frappe dans un champ qui n'est plus calculé. `temps_lecture` peut aussi être écrit en dur pour forcer une valeur, sinon il est calculé. `schema_apres` est le rang du paragraphe après lequel le schéma s'insère, donc l'avant-dernier, puisque le dernier paragraphe porte l'enjeu et se lit après le visuel. `annexe` est facultative et plafonnée à un bloc, `style` valant `essayer` ou `piege`. Le texte alternatif de l'illustration-titre n'est pas dans la fiche: c'est le titre exact, la norme l'impose. `mention_ia` et `signature` ont des valeurs par défaut, ne les redéclare que pour les changer. `sources` est facultatif mais recommandé: reprends les références du brief de recherche, chacune sous forme de chaîne ou d'objet `titre` plus `url`. Elles n'apparaissent que dans le HTML conservé, jamais dans le courriel. Les champs de reprise suivent le même chemin, sans être rendus du tout: `titre_canonique`, `axe`, `prompt_image`, `apercu_visuels` (l'aperçu en clair de ce que montrent les deux images) et `notes` partent dans le dossier incorporé au HTML, et ce sont eux qui permettront de reprendre la pastille des mois plus tard. Reprends-les du livrable de `generate` ou du dossier d'origine; `build.py` signale ceux qui manquent, sans échouer.

### 4. Construire et contrôler
```
python3 ${CLAUDE_SKILL_DIR}/scripts/build.py fiche.json \
    --msg "pastille NN accroche.msg" --html "pastille NN accroche.html"
python3 ${CLAUDE_SKILL_DIR}/scripts/verify.py "pastille NN accroche.msg" \
    pastille-NN-illustration-titre.png pastille-NN-schema.png \
    --html "pastille NN accroche.html"
```

Deux artefacts, tous deux issus de la même fiche et du même code de rendu: le `.msg` pour diffuser, le HTML pour importer, lire et conserver. Voir « Les deux artefacts ».

Quand il n'y a rien à diffuser, l'archive se produit seule, sans fabriquer un `.msg` que personne n'enverra (une reprise qui ne repart pas, une pastille qu'on veut seulement conserver):

```
python3 ${CLAUDE_SKILL_DIR}/scripts/build.py fiche.json --html "pastille NN accroche.html"
python3 ${CLAUDE_SKILL_DIR}/scripts/verify.py --html "pastille NN accroche.html"
```

Le contrôle porte alors sur les règles propres de l'artefact, qui ne dépendent pas du courriel: visuels incorporés, aucune référence `cid:` restante, une seule table, dossier qui se relit. Si une diffusion suit, refabrique les deux ensemble: un `.msg` sans artefact laisse la pastille sans archive.

**Les visuels ne sont obligatoires que pour le courriel.** Cette même commande accepte une fiche sans `image_titre` ni `image_schema`: à l'emplacement exact de chaque visuel manquant, l'artefact porte un encadré qui le nomme et reprend son texte alternatif, donc l'archive dit ce que les images devaient montrer. `build.py` annonce l'archive comme provisoire et rappelle que le courriel ne peut pas encore être fabriqué, `verify.py` compte les visuels déclarés dans le dossier au lieu d'en exiger deux, et `dossier.py` ressort une fiche sans le champ absent. Une fois les visuels générés, complète la fiche et refabrique. Ne construis jamais le `.msg` dans cet état: `build.py` s'y refuse, et c'est voulu.

`build.py` écrit à côté de la fiche les deux PNG qu'il attache réellement, `pastille-NN-illustration-titre.png` et `pastille-NN-schema.png`. Ce sont eux qu'il faut passer à `verify.py`, et non les images d'origine: celles-ci ont pu être converties depuis le webp, aplaties ou rognées, auquel cas elles ne correspondent plus. Ce sont eux, aussi, qui sont incorporés dans le HTML.

Un mot sur le rognage, actif par défaut. Un schéma sorti de Gemini arrive souvent avec de larges bandes de fond en haut et en bas, et la tentation est de le rogner dans Outlook: ne le fais pas et ne le propose pas, car le rognage y réécrit les dimensions de l'image en dur, emporte le `max-width` et donne au bloc une largeur minimale qu'il ne sait plus réduire. Le script mesure donc les bandes de fond quasi blanc, garde 16 pixels de respiration et rogne avant de construire, en annonçant ce qu'il a retiré. Il s'abstient dans deux cas, en le disant: une image entièrement blanche, et un rognage qui emporterait plus de 60% de la surface, signe d'une détection douteuse plutôt que d'une vraie marge. Le drapeau `--sans-rognage` conserve les bandes et se contente de signaler celles qu'il a vues. Une illustration-titre pleine page n'est jamais concernée, faute de marge à retirer.

`verify.py` rouvre le fichier avec un parseur indépendant et sort en erreur si une contrainte est violée: conteneur invalide, propriété manquante, pièce jointe qui ne correspond pas à sa source, `cid` non référencé, police entre apostrophes, couleur portée par une cellule, apostrophe droite restante, sujet ambigu au codage. Avec `--html`, il contrôle en plus l'artefact conservé: ses deux images doivent être incorporées et plus aucune référence `cid:` ne doit rester, sans quoi le fichier ne se suffit pas à lui-même et n'affichera plus ses visuels une fois déplacé; et il ne doit porter qu'une table, celle du bandeau, sans imbrication, faute de quoi il redevient de la mise en page en tables, ce qu'un importeur aplatit mal. Ne livre rien dont la vérification échoue.

Le contrôle de l'objet mérite un mot, car il porte sur un caractère qu'on ne voit pas. Le sujet est le seul texte accentué du courriel, et Outlook (new) le rabat en octets cp1252 avant de le relire dans un codage sur deux octets, ce qui avale les caractères deux par deux: `[Pastille IA de l掗t閉 #7 : ...`. Une seule séquence invalide suffit à faire échouer ce décodage, et le repli sauve alors le sujet entier: `render.sujet` place donc une espace insécable entre le préfixe et le numéro, dont l'octet `0xA0` suivi du dièse fait office de rupture. C'est invisible et cela vaut pour n'importe quel préfixe et n'importe quel titre. Si l'alerte tombe, c'est que cette rupture a sauté: rétablis-la dans `render.sujet` plutôt que de toucher au titre de l'utilisateur, et ne lui retire jamais ses accents. Le détail du mécanisme, les fausses pistes et la limite (cp932 reste hors de portée de tout caractère invisible) sont dans « Gabarit de diffusion ».

Contrôle ensuite le rendu visuel du HTML, à deux largeurs, en dessous et au-dessus du plafond:

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

- **Largeur fluide, plafonnée.** Aucune largeur de colonne imposée: la colonne suit la fenêtre et cesse de s'étirer au-delà du plafond (1000 pixels). Comme Word ignore `max-width`, le plafond lui est donné en plus par un commentaire conditionnel `[if mso]`.
- **Images à taille fixe**, 600 pixels pour l'illustration-titre et 560 pour le schéma, avec hauteur automatique: elles ne sont jamais étirées au-delà de leur taille nominale et se réduisent seulement si la fenêtre passe en dessous. **La légende du schéma partage ce plafond et ce centrage**, donc son bord gauche est celui de l'image: une légende qui dépasse le visuel qu'elle décrit se lit comme un paragraphe de plus. Word ignorant `max-width`, le plafond de la légende lui est donné en plus par commentaire conditionnel, comme celui de la colonne.
- **Bandes de fond rognées à la construction.** Un visuel arrive fréquemment avec de larges marges blanches, et les rogner dans le client de messagerie est un piège: Outlook y réécrit les dimensions en dur, ce qui emporte le `max-width` et fige la largeur minimale du bloc. Le rognage a donc lieu en amont, sur le fichier, pour qu'il n'y ait plus de raison d'y toucher ensuite.
- **Couleurs déclarées là où Word les lit.** Word n'hérite pas la couleur d'un `<td>` vers son texte, il applique celle du thème de rédaction. Chaque bloc porte donc sa couleur sur l'élément qui porte le texte, `color` est déclaré avant `font-family` (un nom de police entre apostrophes casse l'analyse CSS de Word et emporte la fin de la déclaration), les noms de police ne sont jamais quotés, et tout est doublé en balises présentationnelles `<font color face>`, `<b>`, `<i>`.
- **Typographie française** appliquée par le code: espace insécable avant `:` `;` `!` `?`, apostrophes typographiques, dans le corps HTML comme dans la version texte.
- **Corps en entités ASCII**, pour ne dépendre d'aucune détection d'encodage côté client.
- **Images en ligne**, référencées par `cid:`, marquées `ATT_MHTML_REF` et masquées de la liste des pièces jointes. Si un client n'affiche pas les images dans le corps, c'est ce marquage qu'il faut basculer.
- **Sujet** au format `[Pastille IA de l'été] #NN : Titre`, en espaces ordinaires: les insécables et la recherche des messageries font mauvais ménage. Un titre qui contient déjà un deux-points en produit deux, c'est accepté.

### Le préfixe du sujet ne se demande pas
Le préfixe de saison est une norme de la série, pas un réglage de pastille: une seule valeur, `[Pastille IA de l'été]`, portée par `render.PREFIXE_SUJET` et posée sur tous les courriels. **Ne demande donc jamais à l'utilisateur quel préfixe il veut**, ne lui en propose pas de variante, et ne l'écris pas dans la fiche: le champ `prefixe_sujet` n'existe plus. Une question sur ce point donne à croire qu'il y a là un choix éditorial à faire courriel par courriel, alors que la constance du préfixe est justement ce qui fait reconnaître la série dans une boîte de réception.

Deux conséquences pratiques. Les fiches et les dossiers d'avant portent encore ce champ: `build.py` le retire, et ne dit quelque chose que s'il portait une autre valeur que celle de la série, auquel cas le sujet ne changera pas pour autant. Et si la série est un jour rebaptisée, cela se fait en changeant cette constante, une fois pour toutes les pastilles, pas en interrogeant l'utilisateur à chaque diffusion.

## Gabarit partagé
`plugins/pastille-ia/shared/template-pastille.html` est produit par le même code que le courriel réel, avec un contenu de remplacement:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/build.py --gabarit plugins/pastille-ia/shared/template-pastille.html
```

Régénère-le après toute modification du rendu, pour qu'il ne prenne pas de retard sur le générateur. C'est la version à coller à la main dans un client de messagerie si le `.msg` ne peut pas servir.

## Dépendances
`olefile` pour la vérification, `pillow` pour la conversion des images (webp, transparence). Installe-les si elles manquent (`pip install olefile pillow`). Le reste est de la bibliothèque standard: le conteneur `.msg` est écrit par `scripts/cfb.py`, sans dépendance.
