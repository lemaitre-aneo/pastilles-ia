# Pastilles IA

Outils multi-agents pour les **pastilles** pédagogiques internes sur les LLM: un texte court en français, un prompt unique de génération d'images à coller dans Gemini avec l'aperçu de ce que ces images montreront, puis le courriel de diffusion. Quatre skills:

- **`generate`**: crée une pastille à partir d'un titre. Lance de vrais sous-agents en parallèle (six rédacteurs sous des angles différents, fusion pondérée, puis revue critique par trois relecteurs et correction). C'est aussi lui qui régénère une pastille existante quand la demande réclame du matériau neuf, un changement d'axe par exemple; le nouvel axe est alors partagé par les six brouillons, qui gardent leur jeu d'angles. Pour un seul morceau à reprendre, il sait aussi lancer un fan-out ciblé, trois rédacteurs sur ce fragment.
- **`refine`**: reprend une pastille venue d'ailleurs, quand le contexte de sa production est perdu. Entrée de référence: son fichier HTML, dont le dossier incorporé dispense de toute reconstitution. À défaut, et cela reste un chemin entier pour les pastilles antérieures au dossier, on recolle le texte et le skill reconstitue ce qui manque avant d'appliquer un diff minimal. **Une retouche demandée alors que la pastille est déjà dans la conversation ne passe pas par ce skill**, et une demande qui réclame du matériau neuf non plus (voir « Faire évoluer une pastille »).
- **`review`**: fait relire une pastille par trois relecteurs indépendants et parallèles (fond et exactitude, forme et pédagogie, conformité et visuel), qui rendent des constats localisés, consolidés et arbitrés, sans rien réécrire. Invocable seul pour un diagnostic, et déclenché par `generate` (d'office), par `refine` (sur accord) ou depuis une retouche dans le fil (sur accord).
- **`email`**: fabrique le courriel de diffusion, un `.msg` Outlook prêt à compléter et à envoyer, à partir du texte validé et des deux visuels collés dans la conversation. Corps HTML au gabarit, images affichées dans le corps, typographie française appliquée. La même passe écrit un second fichier, un HTML aux teintes de la série avec ses visuels incorporés et le dossier de la pastille en commentaire: il s'importe dans Notion tel quel, tient lieu d'archive et sert de référence pour reprendre la pastille (voir « Les deux artefacts »).

Les quatre skills partagent **une seule source de vérité pour les normes de la série** (`plugins/pastille-ia/shared/regles-pastille.md`): liste des 45 pastilles et périmètre, vocabulaire de l'axe et de l'angle avec la bibliothèque d'angles, Règles du texte et du titre, spec du prompt image avec la bibliothèque de formes de schéma et l'aperçu des visuels, charte graphique, doctrine d'évolution (retoucher, réagencer ou régénérer), gabarit de diffusion, boîte à outils de revue. Le gabarit HTML de diffusion vit à côté, dans `plugins/pastille-ia/shared/template-pastille.html`. Chaque skill n'y ajoute que son propre processus.

## Le schéma: forme libre, invariants fermes

Les deux visuels d'une pastille sont générés dans Gemini à partir d'un bloc de prompt unique. Le schéma, lui, n'a pas de moule: **sa forme est un choix éditorial**, au même titre que l'angle du texte. Trois boîtes et deux flèches conviennent à une séquence; imposées à un mécanisme qui n'en est pas une, elles le déguisent en séquence, et le lecteur retient une idée fausse.

Les six rédacteurs proposent donc chacun une forme, et la fusion retient **celle qui rend le mécanisme le plus lisible, pas celle qui revient le plus souvent**: six brouillons sur un même axe proposent souvent le même flux d'étapes, et la forme proposée une seule fois est parfois la seule qui regarde le mécanisme en face. La bibliothèque de la spec en recense onze (flux, boucle, comparaison en colonnes, couches, anatomie, matrice, entonnoir, zones et périmètre, chronologie, balance, arborescence) et n'est pas fermée. Deux tests la gardent honnête: la **substitution** (si une autre forme ferait aussi bien, la forme n'apporte rien) et le **coût pour le lecteur** (une matrice demande de comprendre deux axes avant de lire une case, elle vaut ce prix quand le croisement est le propos).

Ce qui reste ferme, parce que ce sont des contraintes de diffusion et non des goûts: une seconde image dans son propre fichier, le mécanisme des deux premiers paragraphes et jamais la conclusion, un seul mécanisme par schéma, des libellés courts en français, et surtout la **lisibilité à 560 pixels de large sur téléphone**. C'est elle qui borne le reste: le format va du 4:3 au portrait 4:5, le 16:9 est exclu (les libellés s'y écrasent, et c'est aussi le format qui distingue le schéma de l'illustration-titre à l'extraction), et la densité se juge à ce que l'œil doit démêler plutôt qu'à un nombre de boîtes.

### L'aperçu des visuels

Un prompt est fait pour être collé, pas pour être lu, et c'est pourtant lui qu'il faudrait relire pour savoir ce que l'image va montrer. Le livrable porte donc, **à côté du bloc**, un aperçu en clair des deux images: le motif central et le titre exact rendu pour l'illustration; la forme retenue, le mécanisme qu'elle rend visible, la structure, les libellés et le format pour le schéma.

Il sert quatre lecteurs: l'**utilisateur**, qui peut contester une forme avant de payer une génération; les **relecteurs** de `review`, qui ne voient jamais les images et jugeaient un bloc de prompt à leur place; la **reprise**, des mois plus tard, via le champ `apercu_visuels` du dossier incorporé à l'artefact HTML; et le **lecteur d'écran**, puisque le texte alternatif du schéma s'en dérive.

Ses deux voisins ne font pas le même travail, et les confondre coûte au lecteur: la **légende** est publiée sous le visuel et dit ce qu'il faut en retenir; le **texte alternatif** est ce que reçoit un lecteur d'écran et dit ce qui est dessiné, la forme et les libellés dans l'ordre de lecture (`build.py` signale un alt qui recopie la légende); l'aperçu, lui, reste interne et porte en plus le pourquoi de la forme. L'alt du schéma est donc l'extrait lisible de l'aperçu, pas un texte écrit à côté de lui, et le schéma est le seul des deux visuels qui porte de l'information, celui de l'illustration-titre restant le titre exact. L'aperçu ne se sépare jamais du prompt: dès qu'une ligne du prompt bouge, l'aperçu est réécrit avec elle, et une divergence est un défaut, le prompt faisant foi.

## Le jeu d'angles du fan-out

Six rédacteurs, et leur jeu d'angles n'est pas figé. **Trois slots de noyau** sont toujours là:

- **mécanique**, sans quoi aucun brouillon ne porte la justesse technique;
- **enjeu**, qui fournit le dernier paragraphe, obligatoire dans la série;
- **ancrage concret**, dont la *fonction* est fixe mais l'*angle* libre dans sa famille (analogie, cas d'usage, scène, avant/après). Il faut toujours un brouillon qui rattache le sujet au monde du lecteur; mais la métaphore tire à vide sur certains sujets, alors que l'ancrage, lui, marche partout.

**Trois slots libres** se choisissent dans la bibliothèque d'angles (idée reçue, contre-exemple, avant/après, ordre de grandeur, frontière, filiation, scène, garde-fou, progression, question-réponse, et les angles d'ancrage non employés) selon l'axe et la rubrique pressentie, ou s'inventent quand un axe le mérite.

Un angle est une **porte d'entrée**, pas une qualité. « Pédagogique », « clair », « accessible » n'en sont donc pas: ce sont des normes que les six brouillons doivent tenir ensemble, et en faire des angles laisserait entendre que les autres peuvent être obscurs. Quand l'envie d'un angle « pédagogique » se présente, ce qui manque est presque toujours un ordre d'exposition (*progression*: partir de ce que le lecteur sait et avancer d'un cran à la fois) ou une entrée par sa question (*question-réponse*).

Le socle par défaut (mécanique, enjeu, analogie en ancrage, puis cas d'usage et idée reçue) reste le repli: il est éprouvé sur la série, s'en écarter demande une raison. Et la liberté est bornée par deux garde-fous, sans lesquels elle se retourne contre le fan-out:

- **Contrainte de diversité**: trois slots libres qui ouvrent sur la même porte ne valent qu'un brouillon payé trois fois.
- **Ne pas choisir les angles d'après ce qu'on écrirait soi-même**, sinon six points de vue deviennent six versions du même. L'angle qui paraît le moins naturel est souvent le plus rentable.

Les angles retenus sont annoncés dès qu'on s'écarte du défaut, et tracés dans le livrable: c'est ce qui permet, plus tard, de savoir si un traitement demandé a déjà son brouillon.

### La fusion pondère, elle n'additionne pas

Six angles à parts égales donnent un texte sans porte d'entrée. L'orchestrateur décide donc du **poids** des angles avant de rédiger la version fusionnée. Sans demande particulière, aucun ne domine a priori. Mais quand l'utilisateur demande un angle, ou qu'un angle sert manifestement mieux l'axe, il devient **dominant**: il donne la porte d'entrée, la charpente et le registre, dès le premier paragraphe.

Dominant n'est pas exclusif. Ce n'est pas un copier-coller du brouillon concerné: les autres angles continuent d'alimenter ce qui reste pertinent, un chiffre juste venu de la mécanique, une clôture mieux tournée venue de l'enjeu, un exemple frappant venu d'ailleurs, dès lors que cela se coule dans le registre dominant. Les deux dérives sont symétriques: diluer l'angle demandé jusqu'à ce que l'utilisateur ne le reconnaisse plus, ou réduire la fusion à un seul brouillon et jeter les cinq autres.

## La rubrique suit l'axe, pas l'inventaire

Le bandeau du courriel porte une rubrique, une des six de la série (Comprendre, Limites, Prompting, Au travail, Agents et outils, Risques et cadre). **Elle ne se calcule pas**: elle suit ce que la pastille dit, donc son axe et son contenu final, et se décide à la fusion, une fois le texte arrêté. La position du sujet dans la liste des 45 donne le **défaut**, celui du thème pris dans toute son étendue: il tient la plupart du temps, il l'emporte à égalité, et quand il tient il n'y a rien à annoncer.

Il cède quand l'axe déplace le centre de gravité de la pastille. Une pastille sur le contexte (position 4, « Comprendre ») traitée sous l'axe « ce qu'il ne faut jamais y coller » parle de risque et se range sous « Risques et cadre »: c'est là que le lecteur la chercherait. Le test se pose sur le texte, pas sur le titre canonique: **sous quelle rubrique un lecteur irait-il chercher ce texte-là ?** Un écart s'annonce en une ligne, avec la rubrique qu'il remplace, pour pouvoir être refusé.

Conséquence directe: **un changement d'axe rouvre la rubrique**, au même titre que le titre retenu et le prompt d'images. C'est l'oubli facile d'une régénération, la rubrique n'étant qu'une ligne du bandeau, et c'est pour cela que `generate` la repose à chaque relance et que la grille « fond et périmètre » de `review` la juge sur le texte. Côté fabrication, la rubrique arbitrée s'écrit dans la fiche (champ `rubrique`, contrôlé contre les six noms connus) et voyage dans le dossier de l'artefact; sans ce champ, `build.py` retombe sur le classement d'inventaire en le disant, plutôt que de faire passer un défaut pour un arbitrage.

## Les deux artefacts

Une seule fiche, un seul code de rendu, deux sorties et rien de plus:

| Fichier | Usage | Particularité |
| --- | --- | --- |
| `pastille NN accroche.msg` | diffuser | brouillon Outlook, visuels en pièces jointes `cid:`, corps optimisé pour le moteur de rendu de Word |
| `pastille NN accroche.html` | **importer dans Notion**, lire, conserver, **reprendre** | HTML sémantique aux teintes de la série, visuels **incorporés**, et le dossier complet de la pastille en commentaire |

Le second fait quatre métiers à la fois, lire, importer, conserver et reprendre, ce qui a permis d'abandonner les variantes qui les séparaient: le Markdown, la copie fidèle du courriel, la version aux images voisines. L'archive d'une pastille, ce sont ce fichier et le dossier qui le contient, avec la fiche et les PNG d'origine.

**Les deux sorties ne sont pas solidaires**: `build.py fiche.json --html "..."`, sans `--msg`, produit l'archive seule, et `verify.py --html "..."` la contrôle seule. Diffuser et conserver sont deux décisions distinctes, et une pastille reprise des mois plus tard, ou tirée d'un texte qui ne repartira pas, n'a pas à fabriquer un `.msg` que personne n'enverra. L'inverse ne vaut pas: un `.msg` sans artefact laisse la pastille sans archive.

**L'archive n'attend pas les visuels, le courriel les exige.** Une fiche sans `image_titre` ni `image_schema` produit un artefact provisoire: à l'emplacement exact de chaque visuel manquant, un encadré le nomme et reprend son texte alternatif, donc l'archive dit ce que l'image devait montrer et suffit à la régénérer. C'est le bon geste pour une pastille conservée avant d'être illustrée, ou pour une reprise ancienne dont les images sont perdues: elle rejoint le formalisme tout de suite. Le `.msg`, lui, est refusé tant qu'un visuel manque, et pas par prudence de code: le schéma est systématique dans la série et l'illustration porte le titre.

**Les deux fichiers portent le même nom**, à l'extension près, avec des espaces. Notion nomme la page importée d'après le nom du fichier, pas d'après le `h1` du document; et les tirets ne survivent pas à toutes les chaînes de téléchargement, qui les suppriment et recollent les mots. `build.py` calcule le nom depuis le titre, en gardant l'accroche jusqu'au deux-points, et le rappelle si celui reçu diffère: `pastille 7 les tokens.html`, `pastille 45 la chaine de pensee.html`.

Quatre détails de cet artefact, dont trois viennent de l'import, et aucun n'est cosmétique:

- **Le titre ouvre le fichier mais reste masqué au rendu** (`h1` détouré, pas `display:none`). En tête, il ouvre la page importée; masqué, il ne fait pas doublon avec l'illustration qui le porte déjà; masqué visuellement plutôt que supprimé, il reste annoncé par un lecteur d'écran.
- **Le bandeau est une table** d'une ligne et trois cellules, seule table du fichier. Une table simple s'importe comme une table, ce qui garde le compte, la rubrique et le temps de lecture séparés au lieu de les coller en une ligne de texte. `verify.py` tolère cette table et une seule, et refuse toute imbrication: c'est la mise en page en tables qui s'importe mal, pas la table en soi.
- **Le dossier de la pastille voyage dans un commentaire HTML**, `<!--pastille:dossier … pastille:fin-->`, en fin de corps: la fiche entière en JSON, texte, titres, axe, prompt d'images et aperçu des visuels, sources et notes d'échange. C'est ce qui fait de ce fichier la **référence pour reprendre une pastille** des mois plus tard, et pas seulement de quoi la relire. Un commentaire parce qu'un analyseur HTML les supprime par définition, là où un importeur naïf pourrait recracher le contenu d'un `<script>` dans la page. Les visuels étant déjà incorporés, `scripts/dossier.py` ressort du seul fichier une `fiche.json` et les deux PNG: de quoi tout refabriquer sans rien redemander.
- **Les sources vivent dans un `<details>` replié.** Un navigateur le replie nativement, et Notion exporte ses blocs dépliants sous cette forme, donc l'import devrait donner un bloc dépliant. Le courriel ne les porte pas, la norme les réservant à la vérification; mais une archive sans ses références ne peut plus être rejugée.

Ce que Notion garde: la structure des blocs. Ce qu'il ne garde pas: les couleurs, aucune. La légende du schéma y arrive en paragraphe ordinaire: elle est écrite en `<p>` et non en `figcaption`, que Notion importerait deux fois, une fois en paragraphe placé avant l'image et une fois en légende native. L'habillage aux teintes de la série vaut donc pour la lecture du fichier dans un navigateur; sa palette de texte étant une liste de noms et non des valeurs hexadécimales, les teintes exactes de la charte n'y seraient de toute façon pas reproductibles.

Attention à la taille: le base64 gonfle les visuels d'un tiers, pour un import plafonné à 5 Mo sur le plan gratuit de Notion et 50 Mo sinon. `build.py` alerte au-delà de 4,5 Mo; il faut alors régénérer des visuels plus légers.

Les deux fichiers vivent dans un dossier par pastille, `sorties/pastille-NN-accroche/`, avec la fiche et les visuels. Ce dossier n'est pas suivi par git: ce dépôt s'installe comme plugin chez des collègues qui n'ont pas accès à GitHub, il porte donc l'outillage et non les pastilles diffusées. En session cloud, récupérez les fichiers avant la fin de la session.

## Faire évoluer une pastille

Une pastille se retouche plus souvent qu'elle ne se crée, et **la retouche n'est pas un skill par défaut**. Deux tests tranchent, dans cet ordre: l'ampleur de la demande, puis le contexte disponible.

| Situation | Chemin |
| --- | --- |
| **Retouche** (l'axe et le fond restent) et la pastille a été produite ou déjà travaillée dans cette conversation | Retouche directe dans le fil, **aucun skill**. Le dossier est intact, il n'y a rien à réhydrater. |
| **Retouche** d'une pastille recollée, produite ailleurs (autre conversation, session antérieure, courriel déjà diffusé) | `/refine`, qui reconstitue d'abord le dossier manquant |
| **Réagencement**: l'architecture change (ordre des paragraphes, cœur déplacé, encadré redécoupé) mais le matériau est bon | Réorganisation sur place, **sans fan-out**. Relancer six rédacteurs pour réarranger ce qu'on a déjà, c'est payer six fois pour du matériau qu'on ne cherche pas. |
| **Reprise ciblée**: un morceau délimité est à re-produire (paragraphe qui n'explique rien, analogie qui tombe à plat, encadré à refaire) mais le reste tient | Petit fan-out sur ce seul morceau, avec le texte conservé transmis comme cadre. Trois rédacteurs, pas six: rien de validé n'est jeté. |
| **Changement d'angle**: le traitement change (partir d'un cas d'usage, d'une idée reçue, du mécanisme) mais l'axe reste | Fusion refaite en pondérant cet angle comme dominant, s'il faisait partie du jeu retenu. Zéro sous-agent. Fan-out sous angle imposé seulement si cet angle n'a pas été couvert. |
| **Changement d'axe**: le sujet précis traité change, il faut du matériau neuf sur toute la pastille | Régénération par `generate`, **après confirmation** de l'utilisateur (sauf s'il l'a déjà demandée explicitement). Un diff minimal sur un axe qui change ne produit qu'un patchwork. |

Deux questions ordonnent ces cas: **ai-je besoin de matière que je n'ai pas ?**, puis **s'il faut produire, combien faut-il jeter ?** On prend toujours la réponse la plus légère qui fait le travail.

Un mot de vocabulaire, parce que la confusion coûte cher: l'**axe** est le sujet précis traité à l'intérieur du thème, l'**angle** est la manière de l'aborder (analogie, cas d'usage, idée reçue, mécanique, enjeu, et une dizaine d'autres dans la bibliothèque de la spec). Les six rédacteurs partagent un axe et se répartissent les angles. Changer d'axe change ce que la pastille dit, donc réclame du matériau neuf; changer d'angle change seulement la façon de le dire, et le brouillon écrit sous cet angle existe le plus souvent déjà: on refait la fusion en le pondérant comme dominant, sans relancer personne. Les mots de la demande, eux, ne décident de rien: « corrige », « raccourcis », « change le titre » se disent pareil dans tous les cas. La doctrine complète (test de l'ampleur et signaux structurels, ce qu'on transmet de l'ancien texte, consignes de réagencement, régénération et ce qu'elle garde, test du contexte et ses cas limites, règles du diff minimal, re-synchronisation du prompt image, revue proposée et non imposée, sortie réduite à ce qui change) est dans la spec partagée, section « Faire évoluer une pastille »; `generate` la suit à son étape 6 et `refine` à ses étapes 3 à 5.

Une régénération n'est pas gratuite: six nouveaux brouillons, un titre possiblement différent, une rubrique reposée sur le nouvel axe, un prompt image reconstruit, donc des visuels à refaire dans Gemini et un courriel à refabriquer. C'est pour cela qu'elle se confirme avant d'être lancée. Relancée sur un nouvel axe, elle conserve son jeu d'angles: c'est le sujet qui change, pas la manière de l'aborder. Les angles ne se contraignent que dans le cas plus rare où l'utilisateur impose lui-même un traitement.

Les sous-agents n'héritent d'aucun contexte, donc l'orchestrateur leur transmet aussi **ce qui a orienté la demande**: le retour de l'utilisateur avec ses mots, ce qui est validé et doit survivre, ce qui est écarté. Sans cela ils rejoueraient la pastille qui vient d'être refusée, faute de savoir qu'elle a existé. L'ancien texte, lui, suit une règle de proportion: **il est utile en proportion de ce qu'on en garde.** En reprise ciblée, le texte conservé doit partir avec le fragment à produire, sans quoi celui-ci ne se raccorde ni à la voix ni à ce qui est déjà dit. En régénération complète, rien n'en part: là il n'oriente plus, il enferme, et les brouillons convergeraient vers ce qu'on voulait quitter. Ce n'est pas l'ancien texte qui est dangereux, c'est l'ancien texte sans mandat: cadre de ce qui reste, il aide; modèle de ce qu'il faut refaire, il fixe. Les mêmes consignes partent aux relecteurs de `review`, pour qu'ils ne prennent pas une contrainte assumée pour un défaut. Le dosage compte: trop de consignes uniformise les brouillons, et c'est leur diversité qui fait la valeur de la fusion.

| Entrée | Invocation | Installation |
| --- | --- | --- |
| Ouvrir le dépôt dans Claude Code (local **ou** cloud web) | `/generate`, `/refine`, `/review`, `/email` | aucune, chargé automatiquement |
| Installer le plugin (Cowork, autres postes) | `/pastille-ia:generate`, `/pastille-ia:refine`, `/pastille-ia:review`, `/pastille-ia:email` | via la marketplace GitHub |

Les dossiers `.claude/skills/generate`, `.claude/skills/refine`, `.claude/skills/review` et `.claude/skills/email` sont des liens symboliques vers les sources; ce sont des **skills de projet simples**, donc Claude Code les charge sans aucune action quand on ouvre le dépôt, en local comme en session cloud (le dossier `.claude/` fait partie du clone).

## Structure

```
.claude/skills/generate -> ../../plugins/pastille-ia/skills/generate   # skill projet (symlink) -> /generate
.claude/skills/refine   -> ../../plugins/pastille-ia/skills/refine     # skill projet (symlink) -> /refine
.claude/skills/review   -> ../../plugins/pastille-ia/skills/review     # skill projet (symlink) -> /review
.claude/skills/email    -> ../../plugins/pastille-ia/skills/email      # skill projet (symlink) -> /email
.claude-plugin/marketplace.json                                        # catalogue "alliance-ia" (pour Cowork / CLI)
plugins/pastille-ia/
  .claude-plugin/plugin.json                                           # manifeste du plugin
  shared/regles-pastille.md                                            # LA source unique des normes (les 4 skills la lisent)
  shared/template-pastille.html                                        # gabarit HTML de diffusion, PRODUIT par build.py --gabarit
  skills/generate/
    SKILL.md                                                           # processus de création
    references -> ../../shared                                         # symlink -> ${CLAUDE_SKILL_DIR}/references/regles-pastille.md
  skills/refine/
    SKILL.md                                                           # processus de réhydratation puis retouche
    references -> ../../shared                                         # symlink -> ${CLAUDE_SKILL_DIR}/references/regles-pastille.md
  skills/review/
    SKILL.md                                                           # processus de revue critique (trois relecteurs)
    references -> ../../shared                                         # symlink -> ${CLAUDE_SKILL_DIR}/references/regles-pastille.md
  skills/email/
    SKILL.md                                                           # processus de mise en courriel
    references -> ../../shared                                         # symlink -> ${CLAUDE_SKILL_DIR}/references/regles-pastille.md
    exemple/fiche-modele.json                                          # modele de fiche a copier (aucun contenu reel)
    scripts/build.py                                                   # fiche JSON -> .msg + HTML conservable (+ gabarit)
    scripts/render.py                                                  # corps du courriel et de l'artefact, typographie FR
    scripts/msg.py                                                     # proprietes MAPI et pieces jointes en ligne
    scripts/cfb.py                                                     # ecriture du conteneur OLE2 du .msg, sans dependance
    scripts/extract_images.py                                          # recupere les images collees dans la conversation
    scripts/dossier.py                                                  # ressort la fiche et les visuels d'un artefact HTML
    scripts/verify.py                                                  # relit le .msg et le HTML, echoue si violation
```

Le symlink interne `references -> ../../shared` reste dans le dossier du plugin: c'est le contournement officiel documenté pour partager un fichier entre skills, préservé à l'installation du plugin comme à l'ouverture du dépôt. Chaque SKILL.md lit la spec via `${CLAUDE_SKILL_DIR}/references/regles-pastille.md`.

## Utilisation

### 1. Ce dépôt, dans Claude Code (local ou cloud web)

Rien à installer. Ouvrez le dépôt, accordez la confiance du dossier, puis:

```
/generate      # créer une pastille à partir d'un titre
/refine        # reprendre une pastille venue d'ailleurs (son fichier HTML, ou son texte recollé)
/review        # faire relire une pastille, sans la modifier
/email         # fabriquer le courriel .msg (collez les deux visuels générés)
```

Le parcours complet d'une pastille: `/generate` produit le texte et le prompt d'images, vous générez les deux visuels dans Gemini et vous les collez dans la conversation, `/email` fabrique le `.msg` et le HTML conservable. Les retouches se demandent en langage naturel, sans commande: tant que la pastille est dans la conversation, elles s'appliquent dans le fil, puis `/email` se rejoue sans rien régénérer d'autre. `/refine` ne sert qu'à reprendre une pastille dont la conversation d'origine est perdue: donnez-lui son fichier HTML, il y lit tout le dossier; à défaut, recollez le texte, ce qui reste le chemin des pastilles antérieures au dossier. `/review` juge sans modifier: `generate` le déclenche d'office, et vous pouvez l'appeler seul sur n'importe quelle pastille.

Fonctionne à l'identique en local et en session Claude Code sur le web (les skills sont lus depuis `.claude/skills/` du clone). Aucune marketplace, aucun `/plugin install`, aucun rafraîchissement de cache.

### 2. Cowork / claude.ai

Customize > Plugins > **Add from a repository**, puis l'URL du dépôt (`https://github.com/lemaitre-aneo/pastilles-ia`). Les skills apparaissent via `/` ou le bouton `+`, sous `/pastille-ia:generate` et `/pastille-ia:refine`.

### 3. Autres postes / autres dépôts (Claude Code CLI)

```
/plugin marketplace add lemaitre-aneo/pastilles-ia
/plugin install pastille-ia@alliance-ia
/reload-plugins
```

Puis `/pastille-ia:generate`, `/pastille-ia:refine`, `/pastille-ia:review` ou `/pastille-ia:email`.

## Développement

Les normes de la série sont centralisées dans `plugins/pastille-ia/shared/regles-pastille.md`: modifiez-les là, et les quatre skills en héritent (pas de duplication à synchroniser). Les processus propres à chaque skill vivent dans leur `SKILL.md`. En ouvrant le dépôt, `/generate` et `/refine` pointent (via les symlinks) directement sur ces fichiers: vos modifications sont prises en compte tout de suite, `/reload-plugins` recharge après édition. Pour publier vers Cowork et les autres postes, poussez sur GitHub (ils rafraîchissent ensuite la marketplace).

## Notes

- **Sous-agents parallèles:** `generate` en lance six pour ses brouillons; `review` en lance trois, un par grille de relecture; `refine` n'en lance aucun lui-même et se contente de proposer `review`; `email` n'en lance aucun. Une retouche menée dans le fil n'en lance aucun non plus, sauf si l'utilisateur accepte la revue proposée. Une régénération, en revanche, en relance six puis trois: c'est le coût qui justifie de la confirmer d'abord. Le processus tourne dans Claude Code et dans Cowork. Dans le chat simple de claude.ai (hors Cowork), les sous-agents ne s'exécutent pas; `generate` bascule sur son repli séquentiel documenté et `review` se replie sur un relecteur global unique.
- **Symlinks:** valables sous Linux/WSL et dans le cloud Linux d'Anthropic, aussi bien pour les skills projet (`.claude/skills/*`) que pour les `references -> ../../shared` internes. Un clone Windows sans support des symlinks git verrait des liens cassés; remplacer alors le lien concerné par une copie réelle du fichier cible. Même solution de repli si une session cloud ne suivait pas un symlink.
- **Courriel et Outlook:** le rendu du `.msg` est contraint par le moteur de rendu de Word, qui affiche les messages ouverts dans Outlook pour Windows. Les contournements (couleur jamais portée par un `<td>`, `color` avant `font-family`, aucun nom de police entre apostrophes, mise en forme doublée en balises `<font>`, plafond de largeur en commentaire conditionnel) sont documentés dans la spec partagée et appliqués par `render.py`. `verify.py` échoue si l'un d'eux est défait. Aucun Outlook n'existe dans l'environnement de génération: la validation finale du rendu appartient toujours à l'humain.
- **Le sujet est `[Pastille IA de l'été] #NN : Titre`, et son préfixe n'est pas configurable.** C'est la marque de la série, la même sur tous les courriels: une constante `render.PREFIXE_SUJET`, absente de la fiche, qui ne se demande jamais à l'utilisateur. La seule valeur du sujet qui lui appartient est le numéro de diffusion. Un rebaptême de la série se ferait en changeant cette constante, pas courriel par courriel; les fiches d'avant portant encore un champ `prefixe_sujet`, `build.py` le retire et ne le signale que s'il divergeait.
- **Le sujet du courriel est le seul texte accentué du fichier**, le corps partant en entités ASCII. Outlook (new) le rabat en octets cp1252 puis le relit dans un codage sur deux octets, ce qui avale les caractères deux par deux: sans précaution, 29 des 45 titres s'affichent `[Pastille IA de l掗t閉 #7 : ...`. Une seule séquence invalide fait échouer ce décodage et sauve le sujet entier par repli, d'où l'espace insécable que `render.sujet` place entre le préfixe et le numéro: octet `0xA0` suivi du dièse, invisible, indépendante du libellé du préfixe et du titre. `build.py` alerte et `verify.py` refuse le fichier si elle a sauté.
- **Dépendances du skill `email`:** `olefile` (vérification) et `pillow` (conversion webp et aplatissement de la transparence). Le conteneur `.msg` lui-même est écrit sans aucune dépendance.
- **Nom de marketplace vs dépôt:** la marketplace s'appelle `alliance-ia`, le dépôt GitHub `pastilles-ia`; les installations lisent `pastille-ia@alliance-ia`.
```
