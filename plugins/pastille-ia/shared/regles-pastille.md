# Spec partagée des pastilles LLM

Ce fichier est la source unique des normes de la série. Les skills `generate` (création) et `refine` (raffinement) le lisent tous deux via `${CLAUDE_SKILL_DIR}/references/regles-pastille.md`. Ne duplique pas ces règles dans un SKILL.md: modifie-les ici.

Il contient: la liste des 45 pastilles et les consignes de périmètre, les Règles du texte, les Règles du titre, les Règles d'écriture pour la pastille finale, la spec du prompt de génération d'images (avec gabarits), la charte graphique, et la boite à outils de revue (grilles + gabarit de relecteur).

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

Sers-toi de cette liste pour situer la pastille et délimiter son périmètre. Avant de rédiger:
- Repère les 1 à 3 pastilles voisines qui recouvrent le sujet, et dresse une courte liste "déjà traité ailleurs, à ne pas ré-expliquer".
- Si une pastille voisine a déjà été produite, demande son texte à l'utilisateur (ou appuie-toi dessus s'il est fourni) pour caler précisément la limite.
- Les concepts fondateurs déjà couverts ne sont rappelés qu'en une phrase de mise en contexte, jamais ré-expliqués. Le coeur de la pastille est consacré à ce que son titre ajoute de neuf.
- Ne renvoie pas vers les autres pastilles dans le texte final, sauf si le titre l'impose.

Le libellé du titre peut évoluer (voir Règles du titre), mais le périmètre reste ancré sur le titre canonique: c'est lui, et non le libellé retenu, qui définit ce qui relève du sujet et ce qui est laissé aux voisines.

## Règles du texte
- Longueur adaptée à la profondeur du sujet. Un sujet léger tient en 3 paragraphes courts; un sujet plus riche peut aller jusqu'à 4 paragraphes plus étoffés. Ne gonfle pas artificiellement un sujet simple et ne compresse pas à l'excès un sujet dense: juge la profondeur par la richesse réelle du concept. Prose uniquement, pas de listes ni de puces.
- Ton décontracté, précis et léger: accessible, vivant et sans lourdeur, mais techniquement juste. Public visé: une main-d'oeuvre diverse en société de conseil, du profil non technique au développeur.
- Rythme: privilégie des phrases plutôt courtes et directes, mais varie leur longueur et ajoute du liant (connecteurs, deux-points, points-virgules) pour éviter le style haché ou télégraphique. La lecture à voix haute doit rester fluide.
- Reste léger, évite le name-dropping. N'accumule pas les noms de modèles, d'outils, d'entreprises, de chercheurs ou de techniques pour faire savant: privilégie l'explication claire du mécanisme. Ne cite un nom précis que s'il éclaire vraiment le propos, une ou deux fois au maximum. La recherche sert l'exactitude et alimente la section Sources, elle n'a pas à truffer le texte de références.
- Contenu autonome: la pastille se comprend seule, sans avoir lu les autres, sauf mention contraire dans le titre.
- Rédige en français.
- Ne mentionne jamais ANEO ni aucun nom d'entreprise.
- Le texte explicatif ne figure jamais dans l'image.
- N'utilise pas de tiret cadratin. Privilégie des caractères standard (virgules, deux-points, parenthèses).

## Règles du titre
Le titre est généré comme le reste, mais sous contrainte forte, car il porte trois rôles: identité de la série, ancre de périmètre et texte exact rendu dans l'image.
- Le titre canonique (celui fourni en entrée) est l'ancre de périmètre (non négociable) et un point de départ pour le libellé. La préférence pour ce libellé est faible: à qualité vraiment égale, on le garde, mais on choisit librement une variante dès qu'elle sert mieux le texte final, tant qu'elle respecte le périmètre et le style de série. Ne pas s'obliger à le conserver.
- Fidélité au périmètre: une variante ne doit ni élargir, ni déplacer le sujet défini par le titre canonique, ni empiéter sur une pastille voisine.
- Style de la série: une accroche courte et imagée, le plus souvent suivie de deux-points puis d'une glose en langage clair, ou une question. Registre décontracté, précis et léger, comme le texte.
- Cohérence: le titre tient sa promesse. Le texte délivre ce que le titre annonce, sans sur-promesse ni effet clickbait.
- Rendu image: assez court pour un rendu fiable par le générateur d'images. Un titre long est un compromis à signaler (suggérer Nano Banana Pro).
- Contraintes dures: français, aucun tiret cadratin ni caractère non standard, aucun nom d'entreprise.

## Règles d'écriture pour la pastille finale
- Longueur selon la profondeur du sujet: 3 paragraphes courts si le sujet est léger, jusqu'à 4 paragraphes étoffés s'il est dense. Prose uniquement, pas de listes.
- Mets en gras et/ou en italique les termes importants, de l'ordre de 3 à 4 emphases par paragraphe (repère indicatif, ne force pas ce compte).
- Ton décontracté, précis et léger, accessible mais techniquement juste. Évite le name-dropping: pas d'accumulation de noms de modèles, outils, entreprises ou chercheurs, privilégie l'explication du mécanisme.
- Rythme: privilégie des phrases plutôt courtes et directes, mais varie leur longueur et ajoute du liant (connecteurs, deux-points, points-virgules) pour éviter le style haché ou télégraphique. La lecture à voix haute doit rester fluide.
- Français. Ne mentionne aucune entreprise. Pas de tiret cadratin.
- Contenu autonome, compréhensible seul.
- Titre: voir Règles du titre. Le titre retenu doit tenir sa promesse (le texte délivre ce qu'il annonce, sans sur-promesse) et rester dans le périmètre canonique.

## Prompt de génération d'images (un seul bloc, à coller dans le chat Gemini)
Produis un seul bloc de prompt, rédigé en français, à coller tel quel dans le chat de Gemini. Gemini se charge d'appeler Nano Banana une ou deux fois, ce qui réduit les manipulations pour l'utilisateur.

Le bloc demande:
- Toujours une illustration-titre.
- Un schéma seulement s'il a été retenu à l'étape de fusion, généré comme une seconde image séparée (fichier distinct), jamais dans la même image que le titre.

Contenu du bloc:
- Décris la charte graphique une seule fois (bloc ci-dessous) et précise que toutes les images la partagent, pour une cohérence visuelle.
- Précise: tout texte affiché dans les images est en français. Cette consigne est importante, elle évite qu'un libellé se retrouve en anglais.
- Inclus le texte complet de la pastille dans le bloc, en contexte de génération, clairement marqué comme à ne pas afficher. Il aide le modèle à comprendre le sujet et à choisir une illustration juste. Les seuls textes rendus visibles sont le titre exact et, pour un schéma, ses libellés. Le texte de la pastille ne doit jamais apparaître dans les images.
- Illustration-titre: composition épurée et moderne, focus graphique central iconique représentant le concept. Ce n'est pas un schéma de processus. Le seul texte affiché est le titre exact retenu (celui choisi à l'étape de fusion, pas nécessairement le titre canonique de la série), en en-tête: n'ajoute aucun sous-titre, accroche ou texte secondaire, le titre seul. Technique en deux temps pour le titre: dans le prompt généré, écris le titre exact entre guillemets droits (forme attendue: Le titre exact: "...") et demande un rendu fidèle, sans faute, en police sans serif corporate. Les guillemets ne sont qu'un délimiteur côté prompt: ne les commente pas et n'ajoute aucune consigne à leur sujet dans le prompt généré (pas de mention du type "les guillemets ne doivent pas apparaître").
- Schéma s'il est retenu: une seconde image générée séparément, dans son propre fichier, jamais fusionnée avec l'illustration-titre ni juxtaposée dans la même image. Diagramme d'entreprise propre et net (processus, flowchart ou comparaison), cohérent avec l'illustration-titre, mêmes charte et style, libellés fournis explicitement en français, très peu de fioritures.
- Libellés de schéma: des groupes nominaux courts et lisibles seuls (par exemple "Exemples de bonnes réponses"), pas des phrases verbales qui sonnent comme des ordres ("Montrer de bonnes réponses"). Quelques mots par libellé.

Attention aux titres longs: Nano Banana rend fiablement les libellés courts mais peut faire une faute sur un titre long; la technique en deux temps limite le risque. Si le rendu d'un titre long reste incertain, indique à l'utilisateur qu'il peut demander à Gemini d'utiliser Nano Banana Pro, plus fiable pour le texte long.

Gabarit, illustration-titre seule (exemple avec le titre 1):
```
Génère une image en respectant cette charte graphique: [bloc Charte graphique].
Contexte pour comprendre le sujet, à NE PAS afficher dans l'image: [ici le texte complet de la pastille].
Illustration-titre pour une pastille pédagogique sur les LLM. Composition épurée et moderne, focus graphique central iconique: un nuage de lettres et de mots qui se condense en une bulle de dialogue, évoquant un modèle de langage qui transforme du texte en réponse. Ce n'est pas un schéma de processus.
Seul texte à afficher dans l'image: le titre, en en-tête, sans faute d'orthographe, en police sans serif corporate, sans sous-titre ni texte secondaire. Le titre exact: "TITRE EXACT". Tout le texte affiché est en français. Format 16:9.
```

Gabarit, illustration-titre plus schéma (deux images):
```
Prépares-toi à générer deux images séparées, dans deux fichiers distincts. Les deux partagent cette charte graphique: [bloc Charte graphique]. Tout texte affiché dans les images est en français.
Contexte pour comprendre le sujet, à NE PAS afficher dans les images: [ici le texte complet de la pastille].
Image 1, illustration-titre: composition épurée et moderne, focus graphique central iconique qui illustre le sujet. Ce n'est pas un schéma de processus. Seul texte à afficher: le titre, en en-tête, sans faute d'orthographe, police sans serif corporate, sans sous-titre ni texte secondaire. Le titre exact: "TITRE EXACT". Format 16:9.
Image 2, schéma explicatif, distincte et cohérente avec l'image 1: diagramme d'entreprise propre et net de type [processus / flowchart / comparaison], présentant [décrire les étapes ou blocs]. Libellés exacts à afficher en français: [liste des libellés]. Très peu de fioritures, focus sur la clarté, n'inclus pas le titre.
Génère dans un premier temps seulement la première image (l'illustration-titre), et attends les instructions de l'utilisateur pour générer la 2e image.
```

## Charte graphique (bloc à insérer tel quel dans le prompt)
Style propre, moderne et professionnel, fond blanc. Palette: orange vif et bleu corporate foncé en dominantes, blanc et gris pour les respirations, accents multiculturels discrets (rouge, vert, jaune, bleu) reprenant subtilement un motif de couleurs de logo. Superpositions graphiques épurées: motifs géométriques abstraits, quartiers de cercle, lignes claires. Composition aérée, jamais surchargée. Typographie sans serif, propre et corporate.

## Boite à outils de revue (grilles + gabarit de relecteur)
Ces grilles et ce gabarit servent la revue critique, en génération comme en raffinement. Principe: les relecteurs produisent des CONSTATS, jamais une réécriture. Chacun renvoie une liste de problèmes localisés, assortis d'une gravité et d'un correctif précis. C'est l'orchestrateur qui applique et réécrit, pour garder une voix unique et éviter l'effet patchwork.

Ce que la revue peut juger: les relecteurs ne voient pas les images, générées plus tard dans Gemini. La revue du visuel porte donc uniquement sur le PROMPT image (clarté, cohérence avec le texte, respect des consignes), jamais sur un rendu. Le contrôle visuel réel reste à l'utilisateur.

Les trois grilles (une par relecteur):
1. Fond, exactitude et périmètre: exactitude vs le brief (aucun chiffre, date ou fait inventé ni sur-affirmé, rien qui le contredise), cohérence entre le titre retenu et ce que le texte délivre (le titre tient-il sa promesse, sans sur-promesse ni clickbait ?), maintien du titre retenu dans le périmètre canonique (il ne doit ni élargir ni déplacer le sujet défini par le titre canonique, ni empiéter sur une voisine), chevauchements avec les pastilles voisines (le texte ré-explique-t-il ce qui est traité ailleurs ? redites à signaler), autonomie du contenu, clarté du message à retenir, repérage de ce qui vieillira mal (à nuancer).
2. Forme, ton et pédagogie: ton décontracté-précis-léger et techniquement juste, absence de name-dropping, rythme et fluidité à la lecture à voix haute, longueur adaptée à la profondeur (3 à 4 paragraphes, prose, pas de listes) et chasse au verbiage, accessibilité pour un profil non technique (jargon expliqué, analogies claires), présence d'emphases utiles (gras/italique), de l'ordre de 3 à 4 par paragraphe à titre indicatif (signale un texte trop peu emphasé autant qu'un excès, mais ne fais jamais retirer une emphase pertinente), force de l'accroche et qualité du titre retenu (accroche et punch, respect du style de la série, longueur raisonnable, pas de name-dropping dans le titre; un titre qui s'écarte du canonique n'est pas un défaut en soi, ne réclame le retour au canonique que si le titre retenu est plus faible).
3. Conformité et visuel: contraintes dures (aucun tiret cadratin ni caractère non standard, aucun nom d'entreprise ni ANEO, français correct, prose sans listes ni puces), y compris dans le titre retenu; puis le prompt image: titre retenu reproduit au caractère près (et non le titre canonique s'ils diffèrent), longueur du titre compatible avec un rendu image fiable (sinon suggérer Nano Banana Pro), charte présente une seule fois, texte de la pastille bien marqué "à ne pas afficher", illustration-titre iconique et non schéma de processus, schéma en 2e image séparée si retenu, libellés de schéma courts (groupes nominaux) et en français, cohérence entre le visuel décrit et le coeur du texte.

Gabarit de relecteur (remplace les crochets):
```
Tu relis un brouillon quasi final de pastille pédagogique interne sur les LLM. Tu travailles seul, sans accès au reste de la conversation. Tu ne réécris pas: tu rends des constats et des correctifs précis.

Titre canonique de la pastille (issu de la série, ancre de périmètre): [TITRE_CANONIQUE]
Titre retenu (à juger, peut différer du canonique): [TITRE_RETENU]

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
