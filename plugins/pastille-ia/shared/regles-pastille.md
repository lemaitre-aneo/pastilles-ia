# Spec partagée des pastilles LLM

Ce fichier est la source unique des normes de la série. Les skills `generate` (création), `refine` (reprise d'une pastille venue d'ailleurs), `review` (revue critique) et `email` (mise en courriel) le lisent tous les quatre via `${CLAUDE_SKILL_DIR}/references/regles-pastille.md`. Ne duplique pas ces règles dans un SKILL.md: modifie-les ici.

Il contient: la liste des 45 pastilles et les consignes de périmètre, le vocabulaire de l'axe et de l'angle avec la bibliothèque d'angles et la règle de composition, les Règles du texte, les Règles du titre, les Règles d'écriture pour la pastille finale, la spec du prompt de génération d'images (avec gabarits), la charte graphique, la doctrine d'évolution d'une pastille (retoucher, réagencer ou régénérer, et avec quel contexte), le gabarit de diffusion, et la boite à outils de revue (grilles + gabarit de relecteur).

## Liste des 45 pastilles (pour la continuité)
1. Au fait, c'est quoi un LLM ?
2. Modèles de fondation : ces géants pré-entraînés dont tout découle
3. Dans les coulisses : comment une IA apprend (sans vraiment comprendre)
4. Le contexte : la "mémoire vive" de l'IA (ce qu'elle voit à un instant T)
5. Pourquoi l'IA oublie : la vérité sur la mémoire d'une session à l'autre
6. Température et créativité : régler le curseur de la "folie" de l'IA
7. Les tokens : la monnaie d'échange (et la manière de penser) des LLM
8. Le non-déterminisme : pourquoi l'IA fait des stats et ne donne jamais deux fois la même réponse
9. Multimodalité : quand l'IA commence à voir, entendre et coder
10. Knowledge cutoff : pourquoi votre IA vit (parfois) dans le passé
11. Les biais de l'IA : le miroir pas toujours glorieux de nos propres données
12. Zéro pointé : pourquoi l'IA est structurellement nulle en calcul mental
13. Les hallucinations : quand l'IA invente la vie avec un aplomb incroyable
14. L'art du Fact-Checking : comment ne pas gober les hallucinations de l'IA
15. L'empreinte carbone de l'IA : combien d'eau et de CO2 pour un prompt ?
16. Anatomie d'un bon prompt : la recette de base
17. Les pièges du prompt : flou artistique et overdose d'instructions
18. L'art de la discussion : pourquoi il faut itérer plutôt que tout demander d'un coup
19. Donner des ordres : comment imposer un format de sortie strict (JSON, tableaux, etc.)
20. Diviser pour régner : découper une tâche complexe en étapes claires
21. Le Few-Shot Prompting : un bon exemple vaut mille consignes
22. Inception : donner un rôle et un contexte à votre IA
23. Zéro syndrome de la page blanche : rédiger et reformuler ses mails ou CR
24. La diagonale du fou : résumer et synthétiser un pavé de 50 pages en 2 minutes
25. Le sparring-partner : brainstormer et structurer ses idées sans filtre
26. Caméléon : traduire et adapter son ton selon le destinataire
27. Data-analyst de poche : faire parler un tableur ou des données brutes
28. Mise en situation : préparer une réunion ou un brief client avec l'IA
29. Avis aux dévs : l'IA comme copilote de code et de review
30. SLM : Pourquoi sortir un tank pour écraser une mouche ?
31. Le "harnais" : donner des bras, des yeux et un cadre au LLM
32. C'est quoi un "Agent" IA, concrètement ?
33. Human-in-the-loop : pourquoi il faut toujours garder un humain aux manettes
34. Quand l'agent s'emballe : autonomie et erreurs en cascade
35. Automatisation : confier un workflow complet à un agent
36. Tool Use : quand l'IA apprend à utiliser une calculatrice ou une API
37. Le RAG : faire réviser vos propres documents à l'IA avant qu'elle ne réponde
38. MCP et connecteurs : brancher l'IA directement sur vos outils de dev et d'orga
39. Responsabilité : vous êtes le seul signataire de ce que produit l'IA
40. Confidentialité : où vont vraiment les données que vous tapez ?
41. Alerte Rouge : les données clients à ne JAMAIS copier-coller dans une IA public
42. Shadow AI : pourquoi le ChatGPT gratuit perso au bureau est une fausse bonne idée
43. RGPD et IA : ce qu'il faut savoir pour rester dans les clous
44. Prompt Injection : quand on pirate une IA avec de simples phrases
45. La Chaîne de Pensée : pourquoi l'IA a besoin de "réfléchir à voix haute"

Cette liste est un inventaire de sujets, pas un ordre de diffusion. Ses positions servent au périmètre et à la continuité; elles ne sont pas le numéro affiché dans le bandeau du courriel, qui suit l'ordre de publication décidé par l'utilisateur (voir « Numéro et rubrique »).

Sers-toi de cette liste pour situer la pastille et délimiter son périmètre. Avant de rédiger:
- Repère les 1 à 3 pastilles voisines qui recouvrent le sujet, et dresse une courte liste "déjà traité ailleurs, à ne pas ré-expliquer".
- Si une pastille voisine a déjà été produite, demande son texte à l'utilisateur (ou appuie-toi dessus s'il est fourni) pour caler précisément la limite.
- Les concepts fondateurs déjà couverts ne sont rappelés qu'en une phrase de mise en contexte, jamais ré-expliqués. Le coeur de la pastille est consacré à ce que son titre ajoute de neuf.
- Ne renvoie pas vers les autres pastilles dans le texte final, sauf si le titre l'impose.

Le libellé du titre peut évoluer (voir Règles du titre), mais le périmètre reste ancré sur le titre canonique: c'est lui, et non le libellé retenu, qui définit ce qui relève du sujet et ce qui est laissé aux voisines.

## Axe et angle (vocabulaire, à ne pas confondre)
Ces deux mots reviennent partout et désignent deux choses de nature différente. Les confondre conduit à relancer une génération là où un autre traitement suffisait, ou à disperser les rédacteurs sur des variantes que personne n'a demandées.

- **Thème**: le sujet de la pastille, fixé par son titre canonique et son périmètre. Il ne bouge pas sans changer de pastille.
- **Axe**: le sujet précis retenu à l'intérieur du thème, ce dont la pastille parle vraiment quand plusieurs facettes sont possibles. Il se choisit en amont, avec l'utilisateur, avant de rédiger. Changer d'axe change **ce que la pastille dit**, et demande donc du matériau neuf, parfois de nouvelles sources.
- **Angle**: la manière d'aborder cet axe. Analogie, cas d'usage, idée reçue, mécanique, enjeu. C'est un traitement, une porte d'entrée, un ton, pas un sujet. Changer d'angle change **la façon de le dire**, sur le même axe.

### Bibliothèque d'angles
Les angles ne sont pas un jeu figé. Ce sont des portes d'entrée, et certaines conviennent mieux que d'autres selon l'axe. Voici celles qui ont fait la preuve de leur utilité; la liste n'est pas fermée, un angle inventé pour un axe particulier est légitime s'il tient en une phrase claire.

Noyau, trois slots qui ne se suppriment pas:
- **Mécanique**: le fonctionnement, précis mais accessible. Sans lui, aucun brouillon ne porte la justesse technique et la fusion devient une jolie coquille.
- **Enjeu**: ce que le sujet change concrètement pour le lecteur. Le dernier paragraphe de la pastille est toujours l'enjeu, donc ce matériau est requis à tous les coups.
- **Ancrage concret**: un slot dont la fonction est fixe et l'angle choisi. Il faut toujours un brouillon qui rattache le sujet au monde du lecteur, sans quoi la pastille reste abstraite pour le public non technique visé par la série. L'angle qui remplit ce slot se prend dans la famille de l'ancrage, selon ce qui prend sur l'axe: **analogie** quand le sujet supporte la métaphore, **cas d'usage** quand une situation de travail parle mieux, **scène** ou **avant/après** quand l'écart se montre plus qu'il ne s'explique. C'est le slot obligatoire dont l'angle reste libre, exprès: la métaphore tire à vide sur certains sujets, l'ancrage jamais.

Bibliothèque, pour les slots libres (et pour remplir l'ancrage):
- **Analogie**: une métaphore concrète du quotidien.
- **Cas d'usage**: une situation de travail réelle et vécue.
- **Idée reçue**: un malentendu courant, puis la rectification.
- **Contre-exemple**: ce qui se passe quand on s'y prend mal, et ce que l'échec enseigne.
- **Avant/après**: la même tâche sans puis avec, pour rendre l'écart tangible.
- **Ordre de grandeur**: partir d'un chiffre frappant et le rendre parlant. Exige un brief solide, sinon c'est l'angle qui invente.
- **Frontière**: ce que le sujet ne fait pas, ne couvre pas, ne remplace pas. Précieux quand le voisinage dans les 45 est chargé.
- **Filiation**: d'où ça vient, ce que ça remplace, pourquoi cela apparait maintenant.
- **Scène**: un court échange, un dialogue, un moment de bureau.
- **Garde-fou**: le risque, puis la parade, dans cet ordre.
- **Progression**: partir de ce que le lecteur sait déjà et avancer d'un cran à la fois jusqu'au concept. L'angle de l'ordre d'exposition, là où l'analogie substitue une image et où la mécanique entre directement dans le fonctionnement.
- **Question-réponse**: partir de la question que le lecteur se pose vraiment, y répondre, et laisser cette réponse ouvrir la suivante. Proche de l'idée reçue, mais sans malentendu à corriger: il n'y a qu'une curiosité à satisfaire.

Affinités indicatives par rubrique (voir « Numéro et rubrique »), à ne pas suivre mécaniquement:
- Comprendre: analogie, mécanique, filiation, progression.
- Limites: idée reçue, contre-exemple, ordre de grandeur, question-réponse.
- Prompting: cas d'usage, avant/après, scène, contre-exemple.
- Au travail: cas d'usage, avant/après, scène.
- Agents et outils: mécanique, frontière, contre-exemple, progression.
- Risques et cadre: garde-fou, idée reçue, ordre de grandeur, frontière, question-réponse.

Ce qui n'est pas un angle: une qualité exigée de tous. « Pédagogique », « clair », « accessible », « juste », « vivant » ne sont pas des portes d'entrée, ce sont des normes que les six brouillons doivent tenir ensemble (voir Règles du texte, et la grille 2 de la revue). En faire des angles laisserait entendre que les autres peuvent être obscurs ou faux, et produirait un brouillon indistinct de son voisin. Quand l'envie d'un angle « pédagogique » se présente, ce qui manque est presque toujours un ordre d'exposition (progression) ou une entrée par la question du lecteur (question-réponse): ces deux-là sont des angles, et ils sont dans la liste.

### Composer le jeu d'angles
Six rédacteurs: trois slots de noyau et trois slots libres.
- **Trois slots de noyau**, dans tous les cas: mécanique, enjeu, et l'ancrage concret dont l'angle se choisit dans sa famille.
- **Trois slots libres**, choisis dans la bibliothèque ou inventés, selon l'axe et la rubrique.
- **Jeu par défaut**, à garder en l'absence de raison de faire autrement: mécanique, enjeu, analogie (ancrage), puis cas d'usage, idée reçue et un troisième angle ajusté à la rubrique. Le socle est éprouvé sur la série; s'en écarter demande une raison, pas une envie.
- **Contrainte de diversité**, qui est la raison d'être du fan-out: les trois slots libres doivent ouvrir sur des portes réellement différentes. Deux angles qui démarrent sur la même scène ou la même métaphore n'en font qu'un, et on a payé deux fois.
- **Ne choisis pas les angles d'après ce que tu écrirais toi-même.** C'est le piège du choix libre: six déclinaisons de ton intuition ne valent pas mieux qu'un seul brouillon, et tu perds ce que le fan-out est censé t'apporter. En cas d'hésitation, retiens l'angle qui te parait le moins naturel: c'est précisément celui que tu n'aurais pas écrit seul.
- **Annonce les angles retenus en une ligne** dès que tu t'écartes du jeu par défaut, avec la raison en quelques mots. L'utilisateur doit pouvoir dire « non, garde l'analogie » avant que six sous-agents ne partent.
- **Pondère les angles à la fusion, ne les additionne pas.** Le fan-out produit six brouillons, pas six sixièmes de pastille. Voir « Pondérer les angles à la fusion » ci-dessous.
- **Garde la trace des angles employés.** Si l'utilisateur demande plus tard un traitement particulier, il faut savoir si cet angle a été couvert: c'est ce qui décide entre reprendre le brouillon correspondant et relancer un fan-out (voir « Faire évoluer une pastille »).

### Pondérer les angles à la fusion
La fusion n'est pas une moyenne. Tous les angles ne pèsent pas pareil dans une pastille donnée, et celui qui tient le dossier doit décider de ce poids au lieu de le subir.

- **Par défaut**, aucun angle ne domine a priori: on retient de chaque brouillon ce que son angle était seul à pouvoir produire, et le texte final trouve sa propre porte d'entrée.
- **Quand un angle est demandé** par l'utilisateur, ou quand un angle sert manifestement mieux l'axe que les autres, il devient **dominant**: c'est lui qui donne la porte d'entrée, la charpente et le registre du texte. Le premier paragraphe s'ouvre sur son terrain, pas au troisième détour.
- **Dominant ne veut pas dire exclusif.** Ce n'est pas un copier-coller du brouillon concerné: les autres angles continuent d'alimenter ce qui reste pertinent, un chiffre juste venu de la mécanique, une conclusion mieux tournée venue de l'enjeu, un exemple frappant venu d'ailleurs. On garde ce qui sert le texte et se coule dans le registre dominant; on écarte ce qui tire dans une autre direction.
- **Les deux dérives, symétriques.** Diluer l'angle demandé jusqu'à ce qu'il ne soit plus qu'une couleur parmi six: l'utilisateur ne reconnait pas ce qu'il a demandé. Ou réduire la fusion au seul brouillon dominant: on jette cinq brouillons payés et la pastille perd en justesse et en relief. Le bon dosage se voit à la lecture: la porte d'entrée est celle demandée, et le corps reste nourri.
- Le noyau garde son rôle même sous un angle dominant: la mécanique fournit l'exactitude, l'enjeu fournit la clôture obligatoire. Un angle dominant ne dispense ni de l'un ni de l'autre.

Conséquence directe pour le fan-out de `generate`: les six rédacteurs partagent le même axe et se répartissent les angles. Donc:
- Un changement d'axe ne touche pas à la répartition des angles. On relance les mêmes angles sur le nouvel axe, avec un brief mis à jour si besoin.
- Un changement d'angle ne touche pas au sujet. Il ne réclame pas forcément de nouvelle production: le brouillon écrit sous cet angle existe peut-être déjà, et il vaut mieux refaire la fusion en le pondérant comme dominant que de relancer six rédacteurs.

## Règles du texte
- Longueur adaptée à la profondeur du sujet. Un sujet léger tient en 3 paragraphes; un sujet plus riche peut aller jusqu'à 4. Ne gonfle pas artificiellement un sujet simple et ne compresse pas à l'excès un sujet dense: juge la profondeur par la richesse réelle du concept.
- Taille des paragraphes: 45 à 60 mots chacun, 2 à 3 phrases. C'est une contrainte ferme, pas un repère. Au-delà, le paragraphe dépasse quinze lignes sur téléphone et redevient un pavé. Si un paragraphe déborde, coupe-le en deux plutôt que de le comprimer. Le corps explicatif est en prose continue, sans listes ni puces.
- Ordre des paragraphes: le dernier paragraphe porte l'enjeu, c'est-à-dire ce que le sujet change concrètement pour le lecteur. Il se lit après le schéma et clôt la pastille.
- Blocs structurés, en complément du corps et jamais à sa place. La pastille porte systématiquement un encadré de synthèse, "L'essentiel", placé en tête: deux à trois puces d'une ligne chacune, ou une phrase unique si le sujet n'a qu'un seul angle. Une puce tient en douze mots ou soixante-dix signes au maximum, ce qui garantit la ligne unique jusqu'à 600 pixels de large; au delà elle passe sur deux lignes et l'encadré redevient de la prose courte au lieu d'un balayage. Une puce qui déborde porte en général deux idées: coupe-la ou choisis. Elle peut porter en outre un seul bloc annexe au maximum, au choix un encadré actionnable (prompt à copier, méthode courte) ou un encadré de mise en garde. La synthèse porte le quoi, la prose porte le pourquoi et le comment. Test de relecture: si l'encadré peut remplacer l'article, c'est l'article qui est trop mince, pas l'encadré qui est trop bavard.
- Ton décontracté, précis et léger: accessible, vivant et sans lourdeur, mais techniquement juste. Public visé: une main-d'oeuvre diverse en société de conseil, du profil non technique au développeur.
- Rythme: privilégie des phrases plutôt courtes et directes, mais varie leur longueur et ajoute du liant (connecteurs, deux-points, points-virgules) pour éviter le style haché ou télégraphique. La lecture à voix haute doit rester fluide.
- Reste léger, évite le name-dropping. N'accumule pas les noms de modèles, d'outils, d'entreprises, de chercheurs ou de techniques pour faire savant: privilégie l'explication claire du mécanisme. Ne cite un nom précis que s'il éclaire vraiment le propos, une ou deux fois au maximum. La recherche sert l'exactitude et alimente la section Sources, elle n'a pas à truffer le texte de références.
- Contenu autonome: la pastille se comprend seule, sans avoir lu les autres, sauf mention contraire dans le titre.
- Rédige en français.
- Ne mentionne jamais ANEO ni aucun nom d'entreprise.
- Le texte explicatif ne figure jamais dans l'image.
- N'utilise pas de tiret cadratin. Privilégie des caractères standard (virgules, deux-points, parenthèses).
- Typographie française: espace insécable avant `:` `;` `!` `?`, et apostrophe typographique (’) plutôt que droite. Le skill `email` l'applique automatiquement au courriel, corps HTML et version texte; pour un rendu en conversation, applique-la à la main.

## Règles du titre
Le titre est généré comme le reste, mais sous contrainte forte, car il porte trois rôles: identité de la série, ancre de périmètre et texte exact rendu dans l'image.
- Le titre canonique (celui fourni en entrée) est l'ancre de périmètre (non négociable) et un point de départ pour le libellé. La préférence pour ce libellé est faible: à qualité vraiment égale, on le garde, mais on choisit librement une variante dès qu'elle sert mieux le texte final, tant qu'elle respecte le périmètre et le style de série. Ne pas s'obliger à le conserver.
- Fidélité au périmètre: une variante ne doit ni élargir, ni déplacer le sujet défini par le titre canonique, ni empiéter sur une pastille voisine.
- Style de la série: une accroche courte et imagée, le plus souvent suivie de deux-points puis d'une glose en langage clair, ou une question. Registre décontracté, précis et léger, comme le texte.
- Cohérence: le titre tient sa promesse. Le texte délivre ce que le titre annonce, sans sur-promesse ni effet clickbait.
- Rendu image: assez court pour un rendu fiable par le générateur d'images. Un titre long est un compromis à signaler (suggérer Nano Banana Pro).
- Contraintes dures: français, aucun tiret cadratin ni caractère non standard, aucun nom d'entreprise.

## Règles d'écriture pour la pastille finale
- Longueur selon la profondeur du sujet: 3 paragraphes si le sujet est léger, jusqu'à 4 s'il est dense. Chaque paragraphe fait 45 à 60 mots, 2 à 3 phrases. La pastille fait donc 135 à 240 mots au total: c'est volontairement court, et cela oblige à choisir. Ce qui relève d'une pastille voisine est laissé à cette voisine. Corps explicatif en prose continue, sans listes ni puces; voir Règles du texte pour les blocs structurés autorisés en complément. Le dernier paragraphe porte l'enjeu.
- Mets en gras et/ou en italique les termes qui portent vraiment le sens, une à deux emphases par paragraphe au maximum. Le message clé est porté par l'encadré de synthèse, pas par le gras: au-delà de deux emphases par paragraphe, le lecteur n'a plus de chemin de lecture privilégié et le texte redevient un pavé uniforme.
- Rédige l'encadré de synthèse une fois le texte arrêté, jamais avant: il doit dénouer ce que le titre annonce, sans le reformuler. Douze mots ou soixante-dix signes par puce au maximum.
- Ton décontracté, précis et léger, accessible mais techniquement juste. Évite le name-dropping: pas d'accumulation de noms de modèles, outils, entreprises ou chercheurs, privilégie l'explication du mécanisme.
- Rythme: privilégie des phrases plutôt courtes et directes, mais varie leur longueur et ajoute du liant (connecteurs, deux-points, points-virgules) pour éviter le style haché ou télégraphique. La lecture à voix haute doit rester fluide.
- Français. Ne mentionne aucune entreprise. Pas de tiret cadratin.
- Contenu autonome, compréhensible seul.
- Titre: voir Règles du titre. Le titre retenu doit tenir sa promesse (le texte délivre ce qu'il annonce, sans sur-promesse) et rester dans le périmètre canonique.

## Prompt de génération d'images (un seul bloc, à coller dans le chat Gemini)
Produis un seul bloc de prompt, rédigé en français, à coller tel quel dans le chat de Gemini. Gemini se charge d'appeler Nano Banana une ou deux fois, ce qui réduit les manipulations pour l'utilisateur.

Le bloc demande:
- Toujours une illustration-titre.
- Toujours un schéma, généré comme une seconde image séparée (fichier distinct), jamais dans la même image que le titre.

Contenu du bloc:
- Décris la charte graphique une seule fois (bloc ci-dessous) et précise que toutes les images la partagent, pour une cohérence visuelle.
- Précise: tout texte affiché dans les images est en français. Cette consigne est importante, elle évite qu'un libellé se retrouve en anglais.
- Inclus le texte complet de la pastille dans le bloc, en contexte de génération, clairement marqué comme à ne pas afficher. Il aide le modèle à comprendre le sujet et à choisir une illustration juste. Les seuls textes rendus visibles sont le titre exact et, pour un schéma, ses libellés. Le texte de la pastille ne doit jamais apparaître dans les images.
- Illustration-titre: composition épurée et moderne, focus graphique central iconique représentant le concept. Ce n'est pas un schéma de processus. Le seul texte affiché est le titre exact retenu (celui choisi à l'étape de fusion, pas nécessairement le titre canonique de la série), en en-tête: n'ajoute aucun sous-titre, accroche ou texte secondaire, le titre seul. Technique en deux temps pour le titre: dans le prompt généré, écris le titre exact entre guillemets droits (forme attendue: Le titre exact: "...") et demande un rendu fidèle, sans faute, en police sans serif corporate. Les guillemets ne sont qu'un délimiteur côté prompt: ne les commente pas et n'ajoute aucune consigne à leur sujet dans le prompt généré (pas de mention du type "les guillemets ne doivent pas apparaître").
- Schéma, systématique: une seconde image générée séparément, dans son propre fichier, jamais fusionnée avec l'illustration-titre ni juxtaposée dans la même image. Diagramme d'entreprise propre et net (processus, flowchart ou comparaison), cohérent avec l'illustration-titre, mêmes charte et style, libellés fournis explicitement en français, très peu de fioritures.
- Le schéma illustre le mécanisme exposé dans le corps de l'explication, jamais la conclusion. Il s'insère avant le dernier paragraphe, donc il doit se comprendre à la lecture des deux premiers.
- Format du schéma: 4:3 plutôt que 16:9, cinq blocs au maximum. Il est diffusé à 560 pixels de large et ses libellés doivent rester lisibles sur téléphone.
- Chaque image est accompagnée, dans le livrable, du texte alternatif à renseigner à la diffusion: le titre exact pour l'illustration-titre, une phrase décrivant ce que montre le schéma pour le second visuel.
- Libellés de schéma: des groupes nominaux courts et lisibles seuls (par exemple "Exemples de bonnes réponses"), pas des phrases verbales qui sonnent comme des ordres ("Montrer de bonnes réponses"). Quelques mots par libellé.

Cohérence entre le texte et les visuels: le titre rendu dans l'illustration est toujours le titre retenu, et le schéma illustre toujours le mécanisme du texte courant. Les visuels sont des artefacts déjà rendus, ils ne suivent pas les retouches: dès que le titre change, ou que le mécanisme exposé dans les premiers paragraphes bouge, les images existantes sont périmées et doivent être régénérées avant la diffusion. Un skill qui ne peut pas lire les images ne peut pas le constater seul: il demande confirmation.

Attention aux titres longs: Nano Banana rend fiablement les libellés courts mais peut faire une faute sur un titre long; la technique en deux temps limite le risque. Si le rendu d'un titre long reste incertain, indique à l'utilisateur qu'il peut demander à Gemini d'utiliser Nano Banana Pro, plus fiable pour le texte long.

Gabarit unique, illustration-titre plus schéma (deux images):
```
Prépares-toi à générer deux images séparées, dans deux fichiers distincts. Les deux partagent cette charte graphique: [bloc Charte graphique]. Tout texte affiché dans les images est en français.
Contexte pour comprendre le sujet, à NE PAS afficher dans les images: [ici le texte complet de la pastille].
Image 1, illustration-titre: composition épurée et moderne, focus graphique central iconique qui illustre le sujet. Ce n'est pas un schéma de processus. Seul texte à afficher: le titre, en en-tête, sans faute d'orthographe, police sans serif corporate, sans sous-titre ni texte secondaire. Le titre exact: "TITRE EXACT". Format 16:9.
Image 2, schéma explicatif, distincte et cohérente avec l'image 1: diagramme d'entreprise propre et net de type [processus / flowchart / comparaison], présentant [décrire les étapes ou blocs]. Libellés exacts à afficher en français: [liste des libellés]. Très peu de fioritures, focus sur la clarté, n'inclus pas le titre. Format 4:3, cinq blocs au maximum, libellés assez grands pour rester lisibles une fois l'image réduite à 560 pixels de large.
Génère dans un premier temps seulement la première image (l'illustration-titre), et attends les instructions de l'utilisateur pour générer la 2e image.
```

## Charte graphique (bloc à insérer tel quel dans le prompt)
Les trois couleurs officielles sont `#FE5100` (orange), `#000F9F` (bleu) et `#FFB600` (orange clair). Elles sont la source commune des illustrations et du courriel: le bloc ci-dessous les donne au générateur d'images, et le gabarit de diffusion en dérive ses teintes. Toute autre valeur employée quelque part est un dérivé de ces trois, jamais une couleur inventée.
Style propre, moderne et professionnel, fond blanc. Palette: orange #FE5100 et bleu #000F9F en dominantes, orange clair #FFB600 en appui, blanc et gris pour les respirations, accents multiculturels discrets (rouge, vert, jaune, bleu) reprenant subtilement un motif de couleurs de logo. Superpositions graphiques épurées: motifs géométriques abstraits, quartiers de cercle, lignes claires. Composition aérée, jamais surchargée. Typographie sans serif, propre et corporate.

## Faire évoluer une pastille (doctrine commune: retoucher, réagencer, reprendre ou régénérer)
Une pastille se retouche bien plus souvent qu'elle ne se crée: un mot qui gêne, un paragraphe trop dense, un titre à resserrer, une puce qui déborde. C'est une opération ordinaire. Deux questions la cadrent, dans cet ordre: l'ampleur de ce qui est demandé (retouche, réagencement, reprise d'un morceau ou régénération complète), puis, dès lors que le texte existant est conservé, le contexte dont on dispose.

### Test de l'ampleur (en premier)
La demande porte-t-elle sur la façon de dire, ou sur ce que la pastille raconte ?

Cinq réponses possibles, de la plus légère à la plus coûteuse:

- **Retouche**: l'axe et le fond restent, la surface bouge. Ton, longueur, un paragraphe, une puce, le titre, un chiffre, un exemple à remplacer, l'enjeu à remettre en clôture, un libellé de schéma. C'est le cas ordinaire: passe au test du contexte.
- **Réagencement**: l'axe tient et le matériau est bon, mais l'architecture ne va pas. L'ordre des paragraphes est à revoir, un point secondaire doit devenir le coeur, le mécanisme et l'exemple doivent échanger leurs places, l'encadré est à refaire sur un autre découpage, le schéma doit illustrer autre chose du même texte. C'est plus qu'un diff minimal, et pourtant il n'y a aucun matériau neuf à produire: celui qui tient le dossier réorganise lui-même, dans le fil, en s'appuyant sur le texte courant et, s'ils sont là, sur les brouillons déjà reçus. Pas de fan-out: relancer six rédacteurs pour réarranger ce qu'on a déjà, c'est payer six fois pour du matériau qu'on ne cherche pas.
- **Reprise ciblée**: une partie délimitée doit être re-produite, le reste tient. Un paragraphe qui n'explique rien, une analogie qui tombe à plat, un encadré à refaire, un titre à retrouver. Il faut du matériau neuf, mais pour ce morceau seulement: le diff minimal ne suffit pas (on ne retouche pas, on remplace), et la régénération complète jetterait ce qui marche. Le bon geste est un fan-out ciblé, quelques rédacteurs sur ce seul morceau, avec le texte conservé transmis comme cadre à respecter.
- **Changement d'angle**: l'axe reste, le traitement change. L'utilisateur veut partir d'un cas d'usage, d'une idée reçue, du mécanisme, plutôt que de la porte d'entrée retenue. Ce n'est pas un changement de sujet, donc pas une régénération: si cet angle faisait partie du jeu retenu, son brouillon existe déjà. Refais la fusion en pondérant cet angle comme dominant (voir « Pondérer les angles à la fusion »), et non en recopiant son brouillon: les autres brouillons gardent ce qu'ils avaient de juste et de fort. Zéro sous-agent. Regarde la trace des angles employés (voir « Composer le jeu d'angles ») avant de conclure qu'il manque.
- **Structurel (changement d'axe)**: il faut du matériau neuf partout. L'axe change, le thème se déplace, ou le brouillon retenu est à jeter. Le diff minimal n'y arrive pas: appliqué à un axe qui change, il garde la charpente de l'ancien sujet sous le vocabulaire du nouveau, exactement le patchwork que la règle de la voix unique veut éviter. Il faut régénérer, voir « Régénération » ci-dessous.

Deux questions ordonnent ces cinq réponses:
- **Ai-je besoin de matière que je n'ai pas ?** Non: retouche, réagencement, ou reprise d'un brouillon existant si c'est l'angle qui change. Oui: reprise ciblée ou régénération.
- **Et s'il faut produire, combien faut-il jeter ?** Un morceau délimité: reprise ciblée, on garde le reste. La pastille entière: régénération, et seul un changement d'axe la justifie.

Prends toujours la réponse la plus légère qui fait le travail. Une régénération lancée là où une reprise ciblée suffisait jette du travail validé, et coûte six sous-agents plus une revue pour remplacer un paragraphe.

Signaux structurels (matériau neuf nécessaire):
- **Changement d'axe**, demandé explicitement ou en substance: « parle plutôt de ce qui arrive quand la fenêtre se remplit », « recentre sur les données qu'on saisit, pas sur celles qui sortent », « ce n'est pas cette facette du sujet qui m'intéresse ». La pastille doit dire autre chose du même thème: le matériau manque, et le brief aussi parfois.
- Déplacement du thème ou du périmètre: la pastille doit traiter un autre sujet, empiéter volontairement sur une voisine, ou son titre canonique change.

Un **changement d'angle** n'est pas dans cette liste, et c'est volontaire: « pars d'une situation de travail », « plutôt sous l'angle de l'idée reçue », « explique le mécanisme au lieu de filer la métaphore » demandent un autre traitement du même axe, pas un autre sujet. Ne relance un fan-out (sous angle imposé) que si le brouillon correspondant n'est plus disponible, contexte perdu, ou si l'angle demandé ne figurait pas dans le jeu retenu.
- Insatisfaction qui se répète: après deux ou trois retouches sur le même point, si rien ne convainc, ce n'est plus la formulation qui est en cause mais le brouillon retenu. Dis-le et propose la régénération plutôt que d'enchainer une quatrième retouche.
- Revue qui rend des constats de fond massifs (le texte n'explique pas son sujet, le titre ne tient pas sa promesse, le mécanisme illustré est mal choisi): le défaut est dans le brouillon, pas dans les phrases. Nuance utile: si ce qui échoue est le traitement et non le sujet, un autre angle suffit peut-être, et le brouillon correspondant est peut-être déjà écrit.

#### Ce qu'on transmet de l'ancien texte
Règle générale: **l'ancien texte est utile en proportion de ce qu'on en garde.**
- **On garde presque tout et on remplace un morceau** (reprise ciblée): le texte conservé se transmet aux rédacteurs, et il le doit. C'est la contrainte de continuité: sans lui, le rédacteur ignore la voix de la pastille, ce qui est déjà dit, ce qu'il ne doit pas répéter, et son fragment ne se raccorde pas. Le passage écarté peut l'accompagner, borné et marqué comme écarté, avec le grief de l'utilisateur: à cette échelle il ne fixe pas l'écriture, il balise ce qu'il faut éviter.
- **On jette tout et on repart sur un autre axe** (régénération complète): rien de l'ancien texte ne se transmet. Là il n'oriente plus, il enferme: le rédacteur en écrit une variante et les brouillons convergent vers ce qu'on voulait justement quitter. Seul un fragment expressément validé par l'utilisateur fait le voyage.

Autrement dit, ce n'est pas l'ancien texte qui est dangereux, c'est l'ancien texte sans mandat: transmis comme cadre de ce qui reste, il aide; transmis comme modèle de ce qu'il faut refaire, il fixe.

Ne surinterprète pas: « change le titre », « raccourcis », « ajoute un exemple » restent des retouches. « Refais-moi ce paragraphe, il n'explique rien » est une reprise ciblée, pas une régénération. Un doute se tranche en posant la question, pas en choisissant l'option la plus chère.

Reprendre un morceau, en pratique: délimite exactement ce qui est remplacé et ce qui est conservé, avant de produire quoi que ce soit. Le texte conservé est intangible: il part avec la commande du fragment comme cadre à respecter, et il ne se réécrit pas au passage. Une fois le fragment retenu, vérifie le raccord (transitions, redites avec ce qui reste, comptages, enjeu toujours en clôture), re-synchronise le prompt image seulement si le morceau touchait au mécanisme illustré ou au titre, et affiche le texte complet recomposé en signalant ce qui a changé. Revue proposée, non imposée: la pastille n'est pas neuve. Le détail du fan-out ciblé (combien de rédacteurs, quoi mettre dans leur prompt) est porté par le skill `generate`.

Réagencer, en pratique: garde l'axe, le titre retenu et le brief; réorganise en une seule voix, sans laisser les coutures de l'ancien plan; revérifie les contraintes de comptage que le déplacement met à mal (taille des paragraphes, enjeu en clôture, puces de l'encadré); re-synchronise le prompt image selon les règles ci-dessous, car un mécanisme qui change de place change souvent le schéma. Affiche le texte réagencé en entier, puisque presque tout bouge, et propose la revue sans l'imposer, comme pour une retouche.

### Régénération (cas structurel)
Régénérer, c'est relancer le processus de `generate`, six brouillons compris. Cela coûte, et cela jette du travail validé: le texte change en entier, le titre retenu peut changer, le prompt image est reconstruit, les visuels déjà rendus deviennent périmés et le courriel doit être refabriqué.

**Demande donc avant de régénérer.** Une seule question, qui dit ce que cela implique et laisse l'alternative ouverte, du genre: « Cet axe-là demande de reprendre la génération: six nouveaux brouillons, titre possiblement différent, visuels à refaire. Je relance, ou je reste sur une retouche plus locale ? »

Exception, et elle compte: si l'utilisateur a déjà été explicite (« régénère », « relance la génération », « refais les brouillons », « reprends de zéro », « réécris-la complètement sous cet angle »), relance sans redemander. Faire reconfirmer une décision qui vient d'être prise n'est pas de la prudence.

Ce qui se garde, ce qui se refait:
- Le brief de recherche se garde s'il couvre encore le sujet. Nouvelle recherche seulement si l'axe déplace le sujet ou appelle des faits qu'il ne porte pas.
- Le titre canonique et le périmètre se gardent: ils ne dépendent pas de l'axe. Si c'est le sujet lui-même qui se déplace, le titre canonique change, et cela se tranche avec l'utilisateur avant de relancer.
- L'axe demandé s'applique aux six rédacteurs, puisque c'est le sujet: ils le partagent et gardent leur jeu d'angles, qui restent la source de diversité du fan-out. Un axe nouveau ne rend pas les angles caducs, il change ce qu'ils traitent. Le cas où les angles eux-mêmes sont contraints est différent, et plus rare: il n'arrive que si l'utilisateur impose un angle précis (voir « Axe et angle »).
- La revue est d'office sur un texte régénéré, comme à toute première génération.
- Le texte refusé ne part pas aux rédacteurs, jamais en entier (ceci vaut pour la régénération complète; en reprise ciblée, voir « Ce qu'on transmet de l'ancien texte »). Un sous-agent qui le lit en écrit une variante: c'est un ancrage, pas une information, et les défauts de l'ancien texte voyagent avec lui. Seule exception, un fragment que l'utilisateur a validé (une phrase, un exemple, un titre), transmis comme élément à conserver: un fragment choisi oriente, le texte entier ancre. Si les rédacteurs semblent avoir besoin de l'ancien texte pour comprendre la demande, c'est le signe qu'il s'agissait d'un réagencement, pas d'une régénération.
- Le retour de l'utilisateur se transmet aux sous-agents: ce n'est pas une information réservée à l'orchestrateur. Ils n'héritent d'aucun contexte, donc sans son grief (avec ses mots, pas paraphrasé), sans ce qu'il veut conserver et sans ce qu'il écarte, ils reproduisent la version qu'il vient de refuser, faute de savoir qu'elle a existé. Il en va de même de tout ce qui a orienté la demande: public visé précisé, exemple imposé, analogie interdite, contrainte de longueur. Le skill de génération dit comment le formuler, et rappelle qu'un excès de consignes uniformise les brouillons: on ne transmet que ce qui change l'écriture.
- Le prompt image se reconstruit entièrement, et les visuels existants sont périmés: dis-le sans attendre la question.

Si le contexte de production est perdu et que la demande est structurelle, le bon chemin est `generate` (à partir du titre canonique, avec une passe de recherche), pas `refine`: il n'y a pas de diff minimal à appliquer à un texte qu'on va réécrire.

### Test du contexte (dès que le texte existant est conservé)
Deuxième question, une fois l'ampleur tranchée: le dossier de la pastille est-il dans la conversation courante ?

Le dossier, c'est le texte et son titre retenu, le titre canonique, l'axe, le brief et ses sources, le périmètre (voisines et liste "déjà traité ailleurs"), et le prompt image s'il existe. Il vit dans la conversation, ou dans le fichier HTML de la pastille, qui l'incorpore précisément pour qu'il survive à la conversation.

- **Contexte présent**, cas le plus fréquent: la pastille a été produite, retouchée ou déjà travaillée dans cette conversation, ou l'utilisateur en a fourni les pièces au fil de l'échange. **Aucun skill à invoquer.** Applique la retouche directement, dans le fil, en suivant les règles ci-dessous. N'appelle pas `refine`: il ne ferait que redemander ou reconstituer un dossier que tu as déjà sous les yeux, avec le risque de repartir sur un brief reconstitué moins fiable que le vrai. N'appelle pas `generate` non plus: il repartirait de zéro.
- **Contexte perdu**: la pastille vient d'ailleurs (autre conversation, session antérieure, courriel déjà diffusé). C'est le cas d'usage du skill `refine`, et le seul. Demande d'abord **le fichier HTML de la pastille**: il porte son dossier complet en commentaire, texte, titres, axe, prompt d'images, sources et notes, plus les visuels incorporés, donc il n'y a rien à reconstituer. À défaut, il faut repartir du texte recollé et reconstituer, ce qui donne un dossier moins fiable; dans ce cas, produire l'artefact à la fin évite la même reconstitution la fois suivante.

Le vocabulaire de la demande ne décide de rien. « retouche », « corrige », « raccourcis », « reformule », « change le titre », « relis et corrige » se disent exactement pareil dans les deux cas: seule la présence ou l'absence du dossier tranche. Un texte qui apparaît dans la conversation n'est pas pour autant un texte sans contexte: ce qui compte est de savoir si son dossier de production est là, pas si son texte est visible.

Cas limites:
- Pastille produite plus haut dans cette conversation, dossier présent: contexte présent, retouche directe. C'est le cas le plus courant, et celui où l'appel à un skill de retouche est une erreur.
- Texte recollé alors qu'il a été produit plus haut dans la même conversation: contexte présent. Le collage ne perd rien, le dossier est toujours là.
- Dossier partiel (le texte est là, le brief manque): traite le manque comme tel, ne bascule pas sur `refine` pour autant. Reconstitue ce qui manque si la retouche en dépend, comme le ferait `refine` à son étape de brief.
- Doute réel: la question à poser à l'utilisateur est « ce texte vient-il d'une autre conversation ? », pas « voulez-vous un raffinement ? ».

### Règles du diff minimal (dans les deux cas)
- Applique uniquement ce qui est demandé et ce qui en découle nécessairement. Préserve tout le reste: n'en profite pas pour réécrire des passages non concernés, ni pour "améliorer" au passage.
- Réécris en une seule voix cohérente, sans effet patchwork à la jointure de la retouche.
- Respecte toutes les normes de cette spec (Règles du texte, Règles du titre, Règles d'écriture pour la pastille finale), y compris les contraintes dures: français, pas de tiret cadratin ni caractère non standard, aucun nom d'entreprise ni ANEO, corps explicatif en prose sans listes ni puces. Les blocs structurés définis par cette spec (encadré de synthèse, bloc annexe) restent autorisés et ne comptent pas comme des listes.
- Vérifie ce que la retouche déplace: la taille des paragraphes touchés (45 à 60 mots), la place de l'enjeu (dernier paragraphe), la longueur des puces de « L'essentiel » (douze mots ou soixante-dix signes), le nombre d'emphases. Une retouche locale casse souvent une contrainte de comptage voisine.
- Titre: si la retouche implique le titre, applique les Règles du titre et garde le périmètre ancré sur le canonique. Sinon, laisse le titre retenu tel quel.
- Recherche: ne relance une recherche web que si la retouche touche un fait, un chiffre ou une donnée mouvante que le brief disponible ne couvre pas. Une retouche de style ne demande aucune recherche quand le brief est là. N'invente jamais un chiffre: si tu ne peux le vérifier ni par le brief ni par une recherche, demande la donnée à l'utilisateur plutôt que d'affirmer.

### Re-synchronisation du prompt image (diff minimal)
Principe directeur: ne régénère jamais le prompt image gratuitement. Si la retouche ne change pas ce que les images doivent montrer, le prompt image reste inchangé.

- Titre retenu modifié: remplace le titre exact (la ligne du type `Le titre exact: "..."`) au caractère près, et rien d'autre.
- Concept central déplacé par la retouche (l'illustration-titre ou le schéma ne colle plus au texte): ajuste la description de l'illustration et/ou du schéma en conservant la charte, le style et la structure du prompt existant. Diff minimal, pas de réécriture complète.
- Le schéma est systématique: ne le retire jamais. Si la retouche déplace le mécanisme illustré, ajuste sa description selon les gabarits de la section « Prompt de génération d'images ». S'il manque au prompt existant, ajoute-le.
- Ni le titre rendu ni le concept illustré ne changent: laisse le prompt image entièrement inchangé. Le contexte caché "à ne pas afficher" n'affecte pas le rendu; ne le rafraîchis que si l'utilisateur le demande.
- Pas de prompt image disponible: n'en fabrique pas, sauf demande explicite. Si la retouche touche au titre ou au concept illustré, signale que le prompt existant ailleurs devra être mis à jour, et propose de le régénérer.
- Dès que le prompt image change, les visuels déjà rendus sont périmés: dis-le, ils doivent être régénérés avant toute nouvelle diffusion.

### Revue après retouche
Ne déclenche pas de revue d'office sur une retouche: elle coûte trois sous-agents. Propose-la, et ne la déclenche qu'avec l'accord de l'utilisateur, en passant par le skill `review`. La revue d'office ne vaut que pour la première génération d'une pastille.

### Sortie d'une retouche
- Contexte présent: n'affiche que ce qui change. Le passage retouché (ou le texte complet si la retouche le traverse), une ligne sur le prompt image seulement s'il bouge, et rien d'autre. Ne rejoue pas le livrable entier, ne réaffiche pas les sources inchangées, n'annonce pas de processus: l'utilisateur voit déjà tout le reste plus haut dans la conversation.
- Contexte perdu: le livrable complet, tel que le définit le skill `refine`, puisque l'utilisateur n'a rien d'autre sous les yeux.

## Gabarit de diffusion (mise en forme du courriel)
La pastille est diffusée par courriel, dans une mise en forme qui fait partie des normes de la série au même titre que le texte et les images. Le skill `email` fabrique ce courriel: un `.msg` Outlook contenant le corps HTML et les deux visuels affichés dans le corps. Le même code écrit aussi, dans le dossier de la pastille, un second fichier HTML aux mêmes teintes mais sans mise en page en tables, visuels incorporés: c'est l'artefact conservé, importable tel quel dans un outil de notes et lisible dans un navigateur. Deux sorties, un seul rendu, donc pas de version divergente. Les sources du brief figurent dans cet artefact, jamais dans le courriel: la série ne les publie pas, mais une archive sans ses références ne peut plus être rejugée. Le fichier de référence `plugins/pastille-ia/shared/template-pastille.html` est produit par le même code, avec un contenu de remplacement: c'est la version à coller à la main si le `.msg` ne peut pas servir, et elle ne peut pas prendre de retard sur le générateur.

Ordre des blocs, de haut en bas:
1. Bandeau de série: numéro de la pastille sur 45, rubrique, temps de lecture. En texte, jamais en image.
2. Illustration-titre, texte alternatif reprenant le titre exact.
3. Encadré "L'essentiel", systématique, trois puces au maximum.
4. Les paragraphes, sauf le dernier.
5. Schéma, suivi d'une légende d'une phrase.
6. Dernier paragraphe, consacré à l'enjeu.
7. Bloc annexe facultatif, un seul: "À essayer" ou "Le piège".
8. Mention de relecture IA, puis signature.

Sujet du courriel: `[Prefixe] #NN : Titre retenu`, par exemple `[Pastille IA de l'été] #4 : Les tokens : la monnaie d'échange (et la manière de penser) des LLM`. Le préfixe suit la saison de diffusion. Un titre qui contient déjà un deux-points en produit deux dans le sujet, c'est accepté. Le sujet reste en espaces ordinaires, sans insécables: la recherche des messageries les gère mal.

Contraintes de mise en page:
- Tables et styles en ligne uniquement, colonne unique. Une feuille de style ne survit pas au collage dans un client de messagerie, et le moteur de rendu d'Outlook pour Windows ne gère ni les grilles ni les boîtes flexibles.
- Largeur fluide, jamais imposée: la colonne suit la fenêtre. Elle est seulement plafonnée, à 1000 pixels, pour que la mesure du texte reste lisible sur un écran large. Word ignorant `max-width`, le plafond lui est donné en plus par un commentaire conditionnel `[if mso]`.
- Images à taille fixe, 600 pixels pour l'illustration-titre et 560 pour le schéma, hauteur automatique: elles ne sont jamais étirées au delà de leur taille nominale et se réduisent seulement si la fenêtre passe en dessous. Chaque image porte un texte alternatif renseigné.
- La légende du schéma se cale sur la largeur du schéma, pas sur celle de la colonne: même plafond, même centrage, donc même bord gauche. Une phrase qui dépasse l'image qu'elle décrit cesse de se rattacher visuellement à elle et se lit comme un paragraphe de plus. La contrainte vaut dans le courriel comme dans l'artefact conservé.
- Les bandes de fond d'un visuel sont rognées à la fabrication du courriel, jamais dans le client de messagerie. Rogner une image dans Outlook réécrit ses dimensions en dur, ce qui emporte le `max-width` et donne au bloc une largeur minimale qu'il ne sait plus réduire. Un schéma cadré au plus juste dès sa génération évite le sujet.
- Texte justifié, conformément au choix éditorial de la série. Le HTML de courriel ne gérant pas la césure, la justification étire les espaces entre les mots; c'est la contrainte de taille des paragraphes qui compense, puisque la dernière ligne d'un paragraphe n'est jamais étirée.
- Corps de texte à 16 pixels, interligne 26 pixels.
- Couleurs dérivées des trois couleurs officielles, jamais choisies à la main: les fonds sont ces couleurs très éclaircies, les textes de blocs des versions assombries. Un point de vigilance: l'orange officiel ne donne que 3,2:1 sur blanc, insuffisant pour un texte de 12 pixels, donc les petits libellés prennent une version assombrie qui remonte au delà de 5:1. L'orange officiel reste employé tel quel là où il est grand ou décoratif, le numéro du bandeau et les barres latérales.
- L'encadré de synthèse porte son texte en gras, sur une teinte claire, avec une bordure pleine sur les quatre côtés. Le gras est le seul poids fiable en courriel: Word ne rend pas les poids intermédiaires, un demi-gras retombe sur le régulier. La bordure pleine et la teinte le séparent des blocs annexes, qui n'ont qu'une barre latérale.

Contraintes imposées par le moteur de rendu de Word. Ce sont des corrections de défauts constatés, pas des préférences: chacune a produit un rendu faux dans Outlook avant d'être ajoutée.
- Aucune couleur de texte portée par un `<td>`: Word ne l'hérite pas vers le texte, il applique celle du thème de rédaction. La couleur est déclarée sur l'élément qui porte réellement le texte.
- Aucun fond de bloc porté par la seule `<table>`: Word ne peint pas un fond de table, seulement un fond de cellule. Un bloc coloré pose donc son fond sur son `<td>`, le fond de table ne servant qu'aux autres clients. C'est la symétrie du point précédent: la couleur du texte descend jusqu'à l'élément textuel, la couleur du fond descend jusqu'à la cellule.
- `color` déclaré avant `font-family` dans chaque style. Un nom de police entre apostrophes casse l'analyse CSS de Word, qui abandonne la fin de la déclaration; ce qui compte doit être passé avant ce point de rupture.
- Aucun nom de police entre apostrophes, pour la même raison.
- Mise en forme doublée en balises présentationnelles (`<font color face>`, `<b>`, `<i>`), que Word applique sans passer par le CSS.
- Corps HTML en entités ASCII, pour ne dépendre d'aucune détection d'encodage côté client.
- Images en ligne référencées par `cid:`, marquées `ATT_MHTML_REF`, masquées de la liste des pièces jointes.

### Numéro et rubrique
Le numéro affiché dans le bandeau est le numéro de diffusion, et **c'est l'utilisateur qui le donne**. La position du sujet dans la liste des 45 n'en est pas la source de vérité: l'ordre de publication n'a aucune raison de suivre l'ordre de l'inventaire. Si l'utilisateur fournit un numéro, il prévaut, sans discussion et même s'il contredit la liste. S'il n'en fournit pas, propose la position du sujet dans la liste et demande confirmation avant de fabriquer le courriel; ne la retiens jamais en silence.

La rubrique, elle, suit le sujet et non le numéro de diffusion: elle se lit sur la position du sujet dans la liste des 45. Une pastille diffusée en treizième position mais inventoriée en cinquième porte donc la rubrique du groupe « Comprendre », pas celle du groupe « Limites ».

- Comprendre: positions 1 à 9 de la liste
- Limites: positions 10 à 14
- Prompting: positions 16 à 22
- Au travail: positions 23 à 29
- Agents et outils: positions 30 à 38
- Risques et cadre: position 15, puis 39 à 45

## Boite à outils de revue (grilles + gabarit de relecteur)
Ces grilles et ce gabarit sont les normes de la revue critique. Le processus, lui, est porté par le skill `review`: c'est lui qui lance les relecteurs et consolide leurs constats, qu'il soit invoqué directement par un humain, par `generate` et `refine` au moment de leur revue, ou depuis une retouche menée dans le fil de la conversation (voir « Faire évoluer une pastille »). Celui qui déclenche la revue ne la conduit jamais lui-même: il la déclenche puis applique ce qu'elle rend.

Principe: les relecteurs produisent des CONSTATS, jamais une réécriture. Chacun renvoie une liste de problèmes localisés, assortis d'une gravité et d'un correctif précis. C'est le skill appelant qui applique et réécrit, pour garder une voix unique et éviter l'effet patchwork.

Ce que la revue peut juger: les relecteurs ne voient pas les images, générées plus tard dans Gemini. La revue du visuel porte donc uniquement sur le PROMPT image (clarté, cohérence avec le texte, respect des consignes), jamais sur un rendu. Le contrôle visuel réel reste à l'utilisateur.

Les trois grilles (une par relecteur):
1. Fond, exactitude et périmètre: exactitude vs le brief (aucun chiffre, date ou fait inventé ni sur-affirmé, rien qui le contredise), cohérence entre le titre retenu et ce que le texte délivre (le titre tient-il sa promesse, sans sur-promesse ni clickbait ?), maintien du titre retenu dans le périmètre canonique (il ne doit ni élargir ni déplacer le sujet défini par le titre canonique, ni empiéter sur une voisine), chevauchements avec les pastilles voisines (le texte ré-explique-t-il ce qui est traité ailleurs ? redites à signaler), autonomie du contenu, clarté du message à retenir, repérage de ce qui vieillira mal (à nuancer).
2. Forme, ton et pédagogie: ton décontracté-précis-léger et techniquement juste, absence de name-dropping, rythme et fluidité à la lecture à voix haute, longueur adaptée à la profondeur (3 à 4 paragraphes de 45 à 60 mots chacun, corps en prose sans listes, dernier paragraphe consacré à l'enjeu; signale tout paragraphe qui dépasse 60 mots et propose où le couper) et chasse au verbiage, accessibilité pour un profil non technique (jargon expliqué, analogies claires), sobriété des emphases (gras/italique), une à deux par paragraphe au maximum: signale tout excès, ne réclame jamais d'emphase supplémentaire, le message clé étant porté par l'encadré de synthèse; qualité de cet encadré (deux à trois puces, douze mots ou soixante-dix signes chacune au maximum: compte-les et signale celles qui débordent, en proposant la coupe; il dénoue le titre au lieu de le reformuler, et il ne peut pas se substituer à l'article), force de l'accroche et qualité du titre retenu (accroche et punch, respect du style de la série, longueur raisonnable, pas de name-dropping dans le titre; un titre qui s'écarte du canonique n'est pas un défaut en soi, ne réclame le retour au canonique que si le titre retenu est plus faible).
3. Conformité et visuel: contraintes dures (aucun tiret cadratin ni caractère non standard, aucun nom d'entreprise ni ANEO, français correct, corps explicatif en prose sans listes ni puces), y compris dans le titre retenu; blocs structurés conformes (encadré de synthèse présent, plafonné à trois puces, chacune tenant en douze mots ou soixante-dix signes, un seul bloc annexe au maximum); puis le prompt image: titre retenu reproduit au caractère près (et non le titre canonique s'ils diffèrent), longueur du titre compatible avec un rendu image fiable (sinon suggérer Nano Banana Pro), charte présente une seule fois, texte de la pastille bien marqué "à ne pas afficher", illustration-titre iconique et non schéma de processus, schéma présent (il est systématique) et généré en 2e image séparée, schéma qui illustre le mécanisme du corps et non la conclusion, format 4:3 et cinq blocs au maximum, libellés de schéma courts (groupes nominaux) et en français, textes alternatifs fournis pour les deux images, cohérence entre le visuel décrit et le coeur du texte.

### Arbitrage des constats
Une fois les trois relecteurs revenus, leurs constats sont consolidés avant d'être appliqués. Ces règles valent partout, quel que soit le skill qui a déclenché la revue:
- Dédoublonner: un même défaut vu par deux grilles ne compte qu'une fois, en retenant le correctif le plus précis.
- Arbitrer les contradictions plutôt que de les empiler. Quand deux relecteurs s'opposent, tranche et dis-le, au lieu d'appliquer les deux.
- Garde-fou anti-gonflement: entre "ajouter" et "raccourcir", la concision l'emporte, sauf erreur de fond avérée.
- Appliquer les constats bloquants et recommandés, écarter ou mentionner les mineurs.
- Un constat qui contredit une norme de cette spec est écarté, en le disant: la spec fait foi, pas le relecteur.
- Un constat qui reproche ce que l'utilisateur a expressément demandé (un titre imposé, un exemple qu'il tient à garder, un parti pris qu'il a choisi) ne s'applique pas contre lui. Mentionne-le une fois, en disant que cela vient d'une consigne, et laisse-le trancher. Ce cas se réduit d'ailleurs en amont: les consignes de l'utilisateur sont transmises aux relecteurs, pour qu'ils ne prennent pas une contrainte pour un défaut.
- Le titre retenu est corrigé au même titre que le texte.
- Une seule passe, jamais de boucle. On ne relance pas une revue sur le texte corrigé.
- La réécriture se fait en une seule voix, par le skill appelant, jamais par recollage des formulations des relecteurs.

Gabarit de relecteur (remplace les crochets):
```
Tu relis un brouillon quasi final de pastille pédagogique interne sur les LLM. Tu travailles seul, sans accès au reste de la conversation. Tu ne réécris pas: tu rends des constats et des correctifs précis.

Titre canonique de la pastille (issu de la série, ancre de périmètre): [TITRE_CANONIQUE]
Titre retenu (à juger, peut différer du canonique): [TITRE_RETENU]

Consignes posées par l'utilisateur (contraintes assumées, ne les compte pas comme des défauts; bloc à supprimer s'il n'y en a pas):
[CONSIGNES: ce qu'il a imposé ou écarté, avec ses mots. Si l'une de ces consignes te parait poser un problème réel, dis-le comme une alerte séparée, pas comme un constat à corriger]

Texte à relire:
[TEXTE COMPLET]

Prompt image associé (à relire aussi):
[BLOC PROMPT IMAGE]

Brief de recherche de référence (fait foi pour l'exactitude):
[BRIEF]

Déjà traité par d'autres pastilles, à ne pas ré-expliquer (et textes voisins si fournis):
[LISTE + TEXTES VOISINS]

Liste des 45 titres (pour repérer les chevauchements):
[LISTE DES 45 TITRES]

Ta grille de relecture (tiens-t'en strictement à elle):
[RUBRIQUE 1, 2 OU 3]

Rappel: tu ne peux pas voir d'image; juge seulement le PROMPT image, pas un rendu.

Réponds exactement dans ce format:
CONSTATS:
- [bloquant|recommandé|mineur] [problème localisé] -> [correctif précis]
- ... (n'invente pas de problème: si un point est bon, ne le liste pas)
VERDICT:
[une phrase: publiable tel quel / corrections mineures / corrections nécessaires]
```
