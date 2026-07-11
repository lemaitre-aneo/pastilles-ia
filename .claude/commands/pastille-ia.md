---
name: pastilles-llm-multi-agent
description: Variante Claude Code du générateur de pastilles LLM, qui lance réellement plusieurs sous-agents en parallèle. Génère une pastille de communication interne sur les LLM (un texte court en français plus un prompt unique de génération d'images à coller dans le chat Gemini), via cinq sous-agents indépendants, une fusion, puis une revue critique par trois sous-agents et une correction. Utilise ce skill dès qu'on te demande de rédiger, produire ou générer une pastille, une fiche ou un contenu court d'acculturation sur les LLM, l'IA générative, le prompting, les agents, le RAG, la confidentialité IA ou tout sujet de la liste des 45 pastilles ci-dessous, que le mot "pastille" soit employé ou non. Utilise-le aussi dès qu'on te fournit un titre issu de cette liste.
---

# Générateur de pastilles LLM, version multi-agents (Claude Code)

## Ce que fait ce skill
Produit une pastille pédagogique complète à partir d'un titre. À la différence de la version chat, il lance de vrais sous-agents parallèles: une passe de recherche, puis cinq sous-agents indépendants qui rédigent chacun un brouillon sous un angle différent, puis une fusion par l'orchestrateur qui retient les meilleures formulations, et enfin une revue critique par trois sous-agents suivie d'une correction. Livrable: le texte de la pastille et un prompt unique de génération d'images à coller dans le chat Gemini.

## Environnement requis
Ce skill suppose Claude Code, avec les sous-agents (outil Task) et la recherche web disponibles. Si les sous-agents ne sont pas disponibles dans ton environnement, n'improvise pas: utilise la variante chat, qui fait le même travail en self-ensemble séquentiel.

## Entrée
Un titre de pastille, idéalement issu de la liste ci-dessous. Si le titre est ambigu ou hors liste, demande une clarification avant de générer.

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

## Processus multi-agents

### Étape 1, recherche (orchestrateur, une seule fois)
Toi, l'orchestrateur, fais d'abord une passe de recherche web ciblée sur le sujet de la pastille. Une seule passe, en amont. Les sous-agents ne peuvent pas lancer de sous-agents et n'héritent pas de ton contexte, donc c'est à toi de faire la recherche puis de leur transmettre les résultats.
- Objectif: exactitude, chiffres, exemples concrets et faits à jour.
- Ancre tes recherches dans le présent: repère la date du jour fournie dans ton contexte (champ currentDate) et privilégie les informations et chiffres les plus récents, car ce domaine évolue vite. Précise cette date au besoin dans tes requêtes.
- Priorise les sources originales ou officielles (blogs d'éditeurs, articles de recherche, sites gouvernementaux, documentation) plutôt que les agrégateurs.
- Adapte la profondeur: quelques recherches pour un concept stable (par exemple ce qu'est un token), davantage pour un sujet à chiffres ou mouvant (empreinte carbone et coûts, modèles spécifiques, SLM, MCP et connecteurs, RGPD).
- Produis un brief de recherche compact: faits clés, chiffres utiles, et 2 à 4 sources. Tu l'injecteras tel quel dans chaque sous-agent, et tu listeras les sources dans le livrable final.

### Étape 2, affinement de la thématique (orchestrateur, une seule fois)
Si plusieurs axes apparaissent pertinents après avoir enlever les axes adressés par d'autres pastilles prévues, dialogue avec l'utilisateur pour choisir l'axe de la pastille.
Si l'axe choisi nécessite de nouvelles sources, refait en une recherche web selon les consignes précédentes.

### Étape 3, fan-out (cinq sous-agents en parallèle)
Lance cinq sous-agents via l'outil Task, dans le même tour, pour qu'ils s'exécutent en parallèle. Sois explicite sur le parallélisme: par défaut Claude Code reste séquentiel, il ne parallélise que si tu le demandes clairement. Un sous-agent par angle:
1. Analogie: expliquer le concept via une métaphore concrète du quotidien.
2. Cas d'usage: partir d'une situation de travail réelle et vécue.
3. Idée reçue: démarrer d'un malentendu courant, puis rectifier.
4. Mécanique: aller au coeur du fonctionnement, précis mais accessible.
5. Enjeu: pourquoi ça compte, ce que ça change concrètement pour l'utilisateur.

Comme le contexte n'est pas hérité, chaque prompt de sous-agent doit être autonome et contenir tout le nécessaire. Utilise ce gabarit, en remplaçant les crochets:
```
Tu rédiges un brouillon d'une pastille pédagogique interne sur les LLM. Tu travailles seul, sans accès au reste de la conversation.

Titre de la pastille: [TITRE]
Angle imposé: [ANGLE, par exemple "Analogie: expliquer via une métaphore concrète du quotidien"]

À NE PAS ré-expliquer (déjà couvert par d'autres pastilles), à mentionner en une phrase au maximum:
[LISTE des points déjà traités ailleurs, à ne pas retraiter]

Brief de recherche (appuie-toi dessus, ne relance pas de recherche):
[BRIEF: faits clés, chiffres, sources]

Règles:
- Longueur selon la profondeur du sujet: 3 paragraphes courts si le sujet est léger, jusqu'à 4 paragraphes étoffés s'il est dense. Prose uniquement, pas de listes.
- Mets en gras et/ou en italique les termes importants, de l'ordre de 3 à 4 emphases par paragraphe (repère indicatif, ne force pas ce compte).
- Ton décontracté, précis et léger, accessible mais techniquement juste. Évite le name-dropping: pas d'accumulation de noms de modèles, outils, entreprises ou chercheurs, privilégie l'explication du mécanisme.
- Rythme: privilégie des phrases plutôt courtes et directes, mais varie leur longueur et ajoute du liant (connecteurs, deux-points, points-virgules) pour éviter le style haché ou télégraphique. La lecture à voix haute doit rester fluide.
- Français. Ne mentionne aucune entreprise. Pas de tiret cadratin.
- Contenu autonome, compréhensible seul.

Réponds exactement dans ce format:
TEXTE:
[les 3 à 4 paragraphes]
ILLUSTRATION_TITRE:
[une phrase décrivant le concept central à illustrer]
SCHEMA:
[oui ou non. Si oui, décris en 2 à 3 lignes le diagramme et ses libellés en français]
```

### Étape 4, fan-in et fusion (orchestrateur)
Attends les cinq retours, puis fusionne en une seule pastille finale:
- Retiens la structure la plus claire, la meilleure analogie, l'exemple le plus parlant, la correction la plus nette, la formulation la plus précise et le "pourquoi ça compte" le plus fort.
- Réécris en une seule voix cohérente. Pas d'effet patchwork.
- Respecte la longueur adaptée à la profondeur (voir Règles du texte) et le ton décontracté, précis et léger, sans name-dropping.
- Décide s'il faut un schéma: inclus-en un si au moins deux sous-agents ont répondu "oui", ou si le concept est intrinsèquement un processus, un flux ou une comparaison (par exemple RAG, agents, étapes de prompting, comparaison de modèles). Le cas échéant, fusionne les meilleures idées de schéma.
- Construis ensuite le prompt image unique (section ci-dessous).

### Règles d'écriture pour la pastille finale
- Longueur selon la profondeur du sujet: 3 paragraphes courts si le sujet est léger, jusqu'à 4 paragraphes étoffés s'il est dense. Prose uniquement, pas de listes.
- Mets en gras et/ou en italique les termes importants, de l'ordre de 3 à 4 emphases par paragraphe (repère indicatif, ne force pas ce compte).
- Ton décontracté, précis et léger, accessible mais techniquement juste. Évite le name-dropping: pas d'accumulation de noms de modèles, outils, entreprises ou chercheurs, privilégie l'explication du mécanisme.
- Rythme: privilégie des phrases plutôt courtes et directes, mais varie leur longueur et ajoute du liant (connecteurs, deux-points, points-virgules) pour éviter le style haché ou télégraphique. La lecture à voix haute doit rester fluide.
- Français. Ne mentionne aucune entreprise. Pas de tiret cadratin.
- Contenu autonome, compréhensible seul.

### Étape 5, revue critique et correction (trois sous-agents en parallèle, puis orchestrateur)
Quand la lancer: systématiquement à la première génération, une fois le texte fusionné et le prompt image construits. Ensuite, si l'utilisateur demande des ajustements, ne relance pas la revue d'office: propose-la, et ne la lance qu'avec son accord (elle coûte trois sous-agents de plus).

Principe: les relecteurs produisent des CONSTATS, jamais une réécriture. Chacun renvoie une liste de problèmes localisés, assortis d'une gravité et d'un correctif précis. C'est toi, l'orchestrateur, qui appliques et réécris, pour garder une voix unique et éviter l'effet patchwork.

Ce que la revue peut juger: les relecteurs ne voient pas les images, générées plus tard dans Gemini. La revue du visuel porte donc uniquement sur le PROMPT image (clarté, cohérence avec le texte, respect des consignes), jamais sur un rendu. Le contrôle visuel réel reste à l'utilisateur.

Lance trois sous-agents en parallèle (parallélisme explicite, sinon l'exécution sera séquentielle), un par grille. Le contexte n'étant pas hérité, chaque prompt doit être autonome et contenir tout le nécessaire: le titre, le texte fusionné, le bloc prompt image, le brief de recherche, la liste "déjà traité ailleurs" (et les textes des pastilles voisines s'ils sont disponibles), et la liste des 45 titres pour repérer les chevauchements.

Les trois grilles:
1. Fond, exactitude et périmètre: exactitude vs le brief (aucun chiffre, date ou fait inventé ni sur-affirmé, rien qui le contredise), cohérence entre le titre et ce que le texte délivre, chevauchements avec les pastilles voisines (le texte ré-explique-t-il ce qui est traité ailleurs ? redites à signaler), autonomie du contenu, clarté du message à retenir, repérage de ce qui vieillira mal (à nuancer).
2. Forme, ton et pédagogie: ton décontracté-précis-léger et techniquement juste, absence de name-dropping, rythme et fluidité à la lecture à voix haute, longueur adaptée à la profondeur (3 à 4 paragraphes, prose, pas de listes) et chasse au verbiage, accessibilité pour un profil non technique (jargon expliqué, analogies claires), présence d'emphases utiles (gras/italique), de l'ordre de 3 à 4 par paragraphe à titre indicatif (signale un texte trop peu emphasé autant qu'un excès, mais ne fais jamais retirer une emphase pertinente), force de l'accroche.
3. Conformité et visuel: contraintes dures (aucun tiret cadratin ni caractère non standard, aucun nom d'entreprise ni ANEO, français correct, prose sans listes ni puces); puis le prompt image: titre exact au caractère près, charte présente une seule fois, texte de la pastille bien marqué "à ne pas afficher", illustration-titre iconique et non schéma de processus, schéma en 2e image séparée si retenu, libellés de schéma courts (groupes nominaux) et en français, cohérence entre le visuel décrit et le coeur du texte.

Gabarit de relecteur (remplace les crochets):
```
Tu relis un brouillon quasi final de pastille pédagogique interne sur les LLM. Tu travailles seul, sans accès au reste de la conversation. Tu ne réécris pas: tu rends des constats et des correctifs précis.

Titre de la pastille: [TITRE]

Texte fusionné à relire:
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

Fan-in et correction (orchestrateur): rassemble les constats, dédoublonne, arbitre les conseils contradictoires. Garde-fou anti-gonflement: entre "ajouter" et "raccourcir", la concision l'emporte, sauf erreur de fond avérée. Applique les constats bloquants et recommandés, écarte ou mentionne les mineurs. Une seule passe, pas de boucle. Réécris la version corrigée en une seule voix, puis prépare le court résumé "Ce que la revue a corrigé" (voir Format de sortie).

### Points de vigilance Claude Code
- Parallélisme explicite: demande clairement cinq sous-agents en parallèle, sinon l'exécution sera séquentielle.
- Contexte non hérité: mets tout dans le prompt du sous-agent, en particulier le brief de recherche.
- Pas d'imbrication: un sous-agent ne peut pas en lancer un autre, garde recherche et fusion chez l'orchestrateur.
- Coût et limites: cinq sous-agents en parallèle multiplient l'usage de jetons et peuvent déclencher des limites de débit. En cas de limite, replie-toi sur une exécution séquentielle.
- Revue: la phase de revue ajoute trois sous-agents. Elle tourne d'office à la première génération; sur les demandes d'ajustement ultérieures, propose-la et ne la lance qu'avec l'accord de l'utilisateur. En cas de limite de débit, exécute les relecteurs en séquentiel ou replie-toi sur un relecteur global unique.
- Réemploi optionnel: tu peux définir les cinq angles comme sous-agents personnalisés dans .claude/agents/ pour les réutiliser, mais ce n'est pas obligatoire, les sous-agents polyvalents suffisent.

## Prompt de génération d'images (un seul bloc, à coller dans le chat Gemini)
Produis un seul bloc de prompt, rédigé en français, à coller tel quel dans le chat de Gemini. Gemini se charge d'appeler Nano Banana une ou deux fois, ce qui réduit les manipulations pour l'utilisateur.

Le bloc demande:
- Toujours une illustration-titre.
- Un schéma seulement s'il a été retenu à l'étape de fusion, généré comme une seconde image séparée (fichier distinct), jamais dans la même image que le titre.

Contenu du bloc:
- Décris la charte graphique une seule fois (bloc ci-dessous) et précise que toutes les images la partagent, pour une cohérence visuelle.
- Précise: tout texte affiché dans les images est en français. Cette consigne est importante, elle évite qu'un libellé se retrouve en anglais.
- Inclus le texte complet de la pastille dans le bloc, en contexte de génération, clairement marqué comme à ne pas afficher. Il aide le modèle à comprendre le sujet et à choisir une illustration juste. Les seuls textes rendus visibles sont le titre exact et, pour un schéma, ses libellés. Le texte de la pastille ne doit jamais apparaître dans les images.
- Illustration-titre: composition épurée et moderne, focus graphique central iconique représentant le concept. Ce n'est pas un schéma de processus. Le seul texte affiché est le titre exact, en en-tête: n'ajoute aucun sous-titre, accroche ou texte secondaire, le titre seul. Technique en deux temps pour le titre: dans le prompt généré, écris le titre exact entre guillemets droits (forme attendue: Le titre exact: "...") et demande un rendu fidèle, sans faute, en police sans serif corporate. Les guillemets ne sont qu'un délimiteur côté prompt: ne les commente pas et n'ajoute aucune consigne à leur sujet dans le prompt généré (pas de mention du type "les guillemets ne doivent pas apparaître").
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

## Format de sortie
Le travail des sous-agents reste dans leur propre contexte, seuls leurs retours te reviennent. N'affiche donc que le livrable final (déjà corrigé par l'étape de revue), la conversation principale reste propre. Si l'utilisateur demande à voir l'atelier, restitue les cinq brouillons reçus et les constats de revue.

Livrable final, dans cet ordre:
- Quand une revue a eu lieu (systématiquement à la première génération), un court résumé "Ce que la revue a corrigé" (2 à 4 lignes) présentant les principaux ajustements, avant le reste. Lors d'ajustements ultérieurs sans revue, présente simplement la version ajustée sans ce résumé.
- Le texte de la pastille (3 à 4 paragraphes), dans sa version corrigée.
- Un bloc de code intitulé "Prompt images (à coller dans Gemini)", contenant le prompt unique prêt à copier.
- Une courte section "Sources" listant 2 à 4 références principales issues de l'étape de recherche, de préférence officielles ou originales. Cette section sert à la vérification et n'a pas vocation à être publiée dans la pastille.

Termine toujours par cette question exacte:
"Comment trouvez-vous le texte, l'image titre et le diagramme (si généré) ? Si une partie vous semble trop complexe, ou si vous souhaitez affiner le focus d'un visuel pour qu'il soit encore plus épuré, n'hésitez pas à me le faire savoir, et je l'ajusterai."
