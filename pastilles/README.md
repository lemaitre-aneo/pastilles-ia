# Pastilles reexportees

Les pastilles deja diffusees, reprises au gabarit actuel de la serie. Le corps du
texte est inchange: la reprise ajoute les cadres que le gabarit impose (bandeau,
encadre L'essentiel, legende du schema, bloc annexe), les textes alternatifs
rediges d'apres les visuels, les sources qui corroborent le message et un prompt
image regenere.

Chaque dossier contient `pastille.html` (a coller dans le client de messagerie),
`pastille.eml` (ouvrable directement pour renvoi), les deux visuels, `meta.json` et
`pastille.md` (le livrable lisible, avec sources et points de vigilance).

Le bandeau porte le numero d'ENVOI, pas le rang dans la liste des 45; la rubrique,
elle, suit le sujet reel, donc la position canonique.

| Envoi | Rubrique | Position canonique | Titre retenu | Bloc annexe |
| --- | --- | --- | --- | --- |
| 1 / 45 | Comprendre | 1 | Au fait, c'est quoi un LLM ? | Le piège |
| 2 / 45 | Prompting | 16 | Anatomie d'un bon prompt : la recette de base | À essayer |
| 3 / 45 | Au travail | 23 | Dites adieu au syndrome de la page blanche : rédiger et reformuler ses mails ou CR | À essayer |
| 4 / 45 | Comprendre | 3 | Dans les coulisses : comment une IA apprend (sans vraiment comprendre) | Le piège |
| 6 / 45 | Limites | 14 | L’art du Fact-Checking : comment ne pas gober les hallucinations de l’IA | À essayer |
| 7 / 45 | Risques et cadre | 39 | Responsabilité : vous êtes le seul signataire de ce que produit l'IA | Le piège |
| 8 / 45 | Comprendre | 4 | Le contexte : la "mémoire vive" de l'IA (ce qu'elle voit à un instant T) | Le piège |
| 9 / 45 | Prompting | 18 | L'art de la discussion : pourquoi il faut itérer plutôt que tout demander d'un coup | À essayer |
| 10 / 45 | Prompting | 17 | Les pièges du prompt : flou artistique et overdose d'instructions | À essayer |
| 11 / 45 | Au travail | 28 | Mise en situation : préparer une réunion ou un brief client avec l'IA | À essayer |
| 12 / 45 | Risques et cadre | 40 | Confidentialité : où vont vraiment les données que vous tapez ? | Le piège |
| 13 / 45 | Comprendre | 5 | L'IA repart de zéro à chaque session : on lui rappelle tout | À essayer |
| 14 / 45 | Limites | 12 | Zéro pointé : pourquoi l’IA est structurellement nulle en calcul mental | Le piège |

## Points de vigilance releves a la reprise

Le corps du texte etant gele, ces constats n'ont pas ete corriges: ils sont remontes tels quels pour arbitrage. Seule exception, decidee explicitement: les tirets cadratins de la pastille 11, remplaces par des parentheses.

### 1 / 45 - Au fait, c'est quoi un LLM ?

- Le texte gelé présente le fonctionnement du modèle comme une prédiction strictement "mot après mot" ("il tire un mot... puis recommence"). C'est la description standard et pédagogiquement correcte du mécanisme d'entraînement et de génération (prédiction du token suivant), mais les travaux d'interprétabilité d'Anthropic montrent que certains modèles peuvent, en interne, anticiper plusieurs mots à venir (par exemple planifier une rime avant d'écrire le vers). Correctif possible si on retouchait un jour ce texte : nuancer "un fragment à la fois" par une remarque du type "même si, en coulisses, le calcul anticipe parfois plus loin que le mot immédiat". Non corrigé ici, conformément à la consigne de gel du corps.
- Les chiffres de probabilité du schéma (canapé 62 %, tapis 21 %, toit 9 %, vélo 1 %) sont un exemple pédagogique illustratif et non une mesure sourcée : aucune vérification externe n'est nécessaire ni possible, mais il convient de garder à l'esprit qu'ils ne représentent pas une sortie réelle d'un modèle précis.
- Aucun autre chiffre daté ou nom d'entreprise ne figure dans le texte gelé : rien d'autre à signaler.

### 2 / 45 - Anatomie d'un bon prompt : la recette de base

- Aucun chiffre ni date à vérifier dans le texte gelé : la pastille décrit une structure conceptuelle (rôle, contexte, tâche, contraintes), que les trois sources ci-dessus corroborent sous des intitulés proches (rôle/persona, contexte, tâche, format/ton). Rien à corriger.
- Titre de l'image identique au titre canonique et au sujet du courriel d'origine : aucun écart à signaler.
- Format d'origine des images (512x279, ratio proche de 16:9 mais pas un schéma en 4:3 strict pour image-2) : le prompt image régénéré redemande un format 4:3 conforme au gabarit actuel, ce qui donnera un schéma légèrement différent en proportions de l'original, mais fidèle à ses libellés et à sa logique.

### 3 / 45 - Dites adieu au syndrome de la page blanche : rédiger et reformuler ses mails ou CR

- Le chiffre "une vingtaine de minutes à deux ou trois" (paragraphe 2) est une estimation ponctuelle non retrouvée telle quelle dans une source publique. L'étude *Science* la plus proche (Noy & Zhang, 2023) mesure une réduction moyenne d'environ 40 % du temps de rédaction, un ordre de grandeur bien inférieur à la division par 7-10 suggérée par le texte gelé. Correctif proposé si une future révision du texte est possible : remplacer par une formulation plus prudente, par exemple "un mail peut tomber à une fraction du temps habituel".
- Ponctuation d'origine incohérente conservée telle quelle par consigne (espace avant les deux-points tantôt présent, tantôt absent : "le vide:", "instantané:", "premier jet:", "éditorial:" sans espace, contre "là :" et "premier coup :" avec espace). Correctif possible si une harmonisation est un jour autorisée : mettre un espace avant chaque deux-points, par cohérence typographique française.
- Le titre du sujet du courriel d'origine ("Dites adieu au syndrome de la page blanche...") diffère légèrement du titre canonique de la liste des 45 ("Zéro syndrome de la page blanche...") ; conformément à la consigne, c'est le titre rendu dans image-1 (identique à celui du sujet) qui a été retenu, car il fait foi pour l'image.

### 4 / 45 - Dans les coulisses : comment une IA apprend (sans vraiment comprendre)

- Aucune erreur factuelle, chiffre douteux, tiret cadratin ou nom d'entreprise repéré dans le texte gelé : rien à signaler ici.
- Le titre rendu dans l'image 1 correspond au caractère près au titre du sujet du courriel et au titre canonique de la liste des 45 : aucun écart à signaler.
- Le bloc annexe "Le piège" est un ajout volontaire (conséquence de "le modèle a appris les formes, pas le monde") : à surveiller pour ne pas trop empiéter sur le futur sujet des hallucinations (pastille 13), mais l'angle ici reste la cause structurelle (apprentissage de la forme, pas du sens), pas le phénomène d'hallucination lui-même.

### 6 / 45 - L’art du Fact-Checking : comment ne pas gober les hallucinations de l’IA

- Aucun chiffre, date ou nom d'entreprise n'apparaît dans le texte gelé : rien à corriger ni à nuancer sur ce plan.
- Le texte gelé contient un caractère non standard hérité de la source (apostrophe typographique dans "coup d'oeil", rendue ’ dans le HTML d'origine) : conservé tel quel dans `pastille.html` conformément à la règle de gel mot pour mot: aucune harmonisation de ponctuation n'a été appliquée.
- Le titre retenu (image-1) est identique au titre du sujet du courriel et au titre canonique de la position 14 : aucun écart à signaler.

### 7 / 45 - Responsabilité : vous êtes le seul signataire de ce que produit l'IA

- Le texte gelé affirme qu'une IA "ne possède ni personnalité juridique ni responsabilité professionnelle". C'est exact en l'état actuel du droit (aucune juridiction ne reconnaît de personnalité juridique à un système d'IA), mais aucune des sources trouvées ne formule l'absence de personnalité juridique de façon aussi explicite et générale : c'est une déduction correcte du cadre juridique actuel plutôt qu'une citation directe. Rien à corriger, juste à garder en tête si le texte est un jour retouché.
- Aucun autre chiffre daté ni nom d'entreprise ne figure dans le texte gelé : rien d'autre à signaler.

### 8 / 45 - Le contexte : la "mémoire vive" de l'IA (ce qu'elle voit à un instant T)

- Aucune erreur factuelle, chiffre douteux, tiret cadratin ou nom d'entreprise repéré dans le texte gelé : rien à signaler ici.
- Le titre rendu dans l'image 1 correspond au caractère près au titre du sujet du courriel et au titre canonique de la liste des 45 : aucun écart à signaler.
- La formule "Pour l'IA, c'est une découverte totale à chaque interaction" porte, dans le HTML source, une mise en gras qui démarre après le "P" initial (soit "P" suivi de "our l'IA..." en gras) : c'est un artefact de mise en forme de l'e-mail d'origine, reproduit tel quel dans le réexport puisque le corps est gelé. Correctif que je proposerais si le gel était levé : faire porter le gras sur le mot entier, "Pour".
- Le bloc annexe "Le piège" est un ajout volontaire qui ne répète pas le corps (il distingue la fenêtre de contexte elle-même des fonctionnalités de mémoire ou de résumé ajoutées par certains outils) ; à surveiller pour ne pas empiéter sur le futur sujet de l'oubli d'une session à l'autre (pastille 5), mais l'angle retenu ici (mémoire d'outil vs fenêtre de contexte) reste distinct de celui de la pastille 5 (pourquoi l'IA oublie d'une session à l'autre).

### 9 / 45 - L'art de la discussion : pourquoi il faut itérer plutôt que tout demander d'un coup

- Le texte gelé évoque une IA qui "relit" ou "raisonne" sur les échanges précédents : c'est une simplification pédagogique (le modèle ne relit rien au sens humain, il retraite l'historique fourni dans le contexte à chaque appel), mais elle correspond à l'esprit des consignes de la série et n'est pas factuellement fausse ; je ne l'ai pas corrigée, conformément à la règle du corps gelé.
- Le titre diffusé dans le sujet du courriel et le titre rendu dans l'image-1 sont identiques au caractère près : aucun écart à signaler sur ce point.

### 10 / 45 - Les pièges du prompt : flou artistique et overdose d'instructions

- Le paragraphe sur l'overdose affirme, en emphase, que « mathématiquement, l'IA répartit sa capacité d'analyse sur l'ensemble du texte » et que « plus vous multipliez les contraintes secondaires, plus vous risquez qu'elle ignore l'instruction principale ». C'est une simplification pédagogique plausible et cohérente avec la littérature sur la dilution d'attention en contexte long (voir source Liu et al.), mais aucune des sources trouvées ne formule ce mécanisme en ces termes précis pour un empilement de « micro-consignes » dans un seul prompt court : le texte gelé n'a donc pas été modifié, mais l'affirmation reste une extrapolation à nuancer si le sujet est repris ailleurs.
- Trois paragraphes du corps dépassent la fourchette actuelle de 45 à 60 mots (50, 79 et 67 mots) : c'est assumé conformément à la consigne, le texte gelé n'a pas été redécoupé.
- Le titre canonique (position 17 de la liste des 45) et le titre lu dans l'image-titre sont identiques au caractère près : aucun écart à signaler sur ce point.

### 11 / 45 - Mise en situation : préparer une réunion ou un brief client avec l'IA

- Deux tirets cadratins du courriel d'origine (paragraphe 1, autour de "par exemple, un directeur financier pointilleux... acheteur sceptique") ont ete remplaces par des parentheses. C'est la seule derogation au gel du corps, decidee explicitement par le commanditaire parce que le tiret cadratin viole une contrainte dure de la serie. Elle est tracee dans `gel-exceptions.json`.
- Le titre diffusé dans le sujet du courriel, le titre canonique de la liste des 45 (position 28) et le titre rendu dans l'image 1 sont identiques au caractère près : aucun écart à signaler.
- Le paragraphe 3 porte cinq emphases en gras et deux en italique, largement au-delà de la norme actuelle (une à deux par paragraphe) : c'est un artefact du format d'origine, reproduit tel quel puisque le corps est gelé.

### 12 / 45 - Confidentialité : où vont vraiment les données que vous tapez ?

- Le texte gelé affirme que, côté entreprise, "les données ne servent jamais à l'entraînement et font l'objet d'une rétention nulle ou limitée, garantissant l'effacement automatique des sessions". C'est globalement exact comme politique par défaut des offres professionnelles/API des grands éditeurs, mais la documentation officielle d'OpenAI précise que la rétention nulle (Zero Data Retention) n'est pas automatique : elle nécessite une éligibilité et une approbation préalables, pas seulement la souscription à une offre payante ou "entreprise". Le bloc "Le piège" a été écrit pour porter cette nuance sans toucher au corps gelé.
- Le paragraphe 2 affirme que "l'IA ne conserve pas une copie brute de vos textes pour les recracher directement à d'autres utilisateurs" et que les requêtes "modifient de manière diffuse les réglages statistiques globaux du système". C'est une simplification pédagogique raisonnable (l'entraînement se fait par lots différés, pas en temps réel à chaque requête), mais aucune source officielle ne formule cette mécanique en ces termes précis : c'est une vulgarisation acceptable, pas une citation vérifiable telle quelle.
- Le paragraphe 3 porte neuf emphases en gras, largement au-dessus du maximum actuel de deux par paragraphe : c'est hérité du format d'origine (le corps est gelé, la mise en emphase n'a pas été retouchée), à garder en tête si le texte est un jour retravaillé.
- Aucun tiret cadratin, aucun nom d'entreprise ni mention d'ANEO dans le texte gelé : rien d'autre à signaler. Le titre diffusé dans l'image correspond au caractère près au titre canonique et au sujet du courriel : aucun écart à signaler sur ce point.

### 13 / 45 - L'IA repart de zéro à chaque session : on lui rappelle tout

- Aucune non-conformité constatée sur les éléments gelés : les 3 puces de L'essentiel respectent la limite (2 à 3), et un seul bloc annexe ("À essayer") est présent dans le courriel d'origine.
- Le texte alternatif que j'ai rédigé pour le schéma diverge légèrement de celui déjà diffusé (formulation resynthétisée plutôt que copiée), mais décrit le même contenu visuel ; les deux sont fidèles à l'image observée.
- La phrase "Un cache accélère le calcul, il ne retient rien" fait probablement référence au cache de préfixe de prompt (prompt caching / KV-cache) : les sources consultées ne le documentent pas explicitement dans ce vocabulaire, mais rien ne le contredit non plus ; c'est une simplification correcte du mécanisme.
- Rien d'autre à signaler : les affirmations du texte gelé (absence de mémoire interne, rejeu de l'historique, mémoire externe consultable/corrigible/désactivable) sont corroborées par les sources ci-dessus.

### 14 / 45 - Zéro pointé : pourquoi l’IA est structurellement nulle en calcul mental

- Le corps, l'encadré "L'essentiel", la légende et le bloc annexe "LE PIÈGE" sont repris tels quels du courriel déjà diffusé (extraction scriptée depuis `source.html`), conformément à la consigne : aucune correction n'a été apportée même si certains points auraient pu l'être (voir ci-dessous).
- L'exemple de découpage donné dans le texte et dans le schéma ("42235630" devient "422, 35, 630", soit des groupes de 3, 2 puis 3 chiffres) ne correspond pas exactement à la règle de tokenisation généralement décrite pour les modèles de la famille GPT (groupes de 3 chiffres au maximum, découpés depuis la gauche, ce qui donnerait plutôt "422, 356, 30"). Le principe général illustré (un nombre est fragmenté en morceaux qui font perdre la valeur de position) est bien corroboré par les sources, mais cet exemple chiffré précis n'a pas pu être vérifié tel quel : à signaler si la pastille est retravaillée.
- Les taux "près de six multiplications sur dix" (trois chiffres) et "moins d'une sur vingt" (quatre chiffres) collent de très près aux 59 % et 4 % mesurés sur GPT-4 par Dziri et al. (2023), mais la pastille ne nomme aucun modèle précis ("un grand modèle") : l'ordre de grandeur est bien corroboré, sans que l'on puisse garantir qu'il s'agit exactement de cette étude et non d'une mesure faite sur un autre modèle.
- Le bandeau reprend "Limites" en majuscules (comme diffusé), alors que les pastilles plus récentes de la série affichent la rubrique en casse "Titre" (ex. "Comprendre"). C'est un élément gelé du courriel d'origine, non corrigé ici.
- Les puces de "L'essentiel" sont entièrement en gras dans le courriel d'origine, alors que les pastilles plus récentes laissent ces puces en texte normal. Élément gelé, non corrigé ici.
- Le texte alternatif de l'image 2 proposé ici diverge légèrement de la formulation utilisée dans le courriel d'origine, mais décrit la même scène (nombre saisi, découpage, vote de règles, réponse retenue) : écart mineur de formulation, pas de fond.
