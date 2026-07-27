---
description: Variante Claude Code du générateur de pastilles LLM, qui lance réellement plusieurs sous-agents en parallèle. Génère une pastille de communication interne sur les LLM (un titre, un texte court en français, plus un prompt unique de génération d'images à coller dans le chat Gemini), via cinq sous-agents indépendants qui proposent chacun aussi un titre, une fusion, puis une revue critique par trois sous-agents et une correction. Utilise ce skill dès qu'on te demande de rédiger, produire ou générer une pastille, une fiche ou un contenu court d'acculturation sur les LLM, l'IA générative, le prompting, les agents, le RAG, la confidentialité IA ou tout sujet de la liste des 45 pastilles ci-dessous, que le mot "pastille" soit employé ou non. Utilise-le aussi dès qu'on te fournit un titre issu de cette liste. Pour retoucher une pastille déjà rédigée (texte fourni), utilise plutôt le skill refine.
---

# Générateur de pastilles LLM, version multi-agents (Claude Code)

## Ce que fait ce skill
Produit une pastille pédagogique complète à partir d'un titre. À la différence de la version chat, il lance de vrais sous-agents parallèles: une passe de recherche, puis cinq sous-agents indépendants qui rédigent chacun un brouillon (titre compris) sous un angle différent, puis une fusion par l'orchestrateur qui retient les meilleures formulations (titre compris), et enfin une revue critique par trois sous-agents suivie d'une correction. Livrable: le titre, le texte de la pastille et un prompt unique de génération d'images à coller dans le chat Gemini.

## Spec partagée (à lire en premier)
Les normes de la série vivent dans un fichier partagé, source unique commune à ce skill et au skill `refine`: liste des 45 pastilles et périmètre, Règles du texte, Règles du titre, Règles d'écriture pour la pastille finale, spec du prompt image et gabarits, charte graphique, boite à outils de revue. Lis-le avant de commencer:

`${CLAUDE_SKILL_DIR}/references/regles-pastille.md` (c'est le fichier `references/regles-pastille.md` situé dans le dossier de ce skill).

Ci-dessous, chaque renvoi "voir la spec partagée, section X" pointe vers ce fichier. Ne recopie pas ces normes ici: si elles doivent évoluer, modifie la spec partagée.

## Environnement requis
Ce skill suppose Claude Code, avec les sous-agents (outil Task) et la recherche web disponibles. Si les sous-agents ne sont pas disponibles dans ton environnement, n'improvise pas: utilise la variante chat, qui fait le même travail en self-ensemble séquentiel.

## Entrée
Un titre de pastille, idéalement issu de la liste de la spec partagée. Si le titre est ambigu ou hors liste, demande une clarification avant de générer.
Ce titre est le titre canonique de la série: il sert d'ancre de périmètre et de libellé par défaut. Le processus peut en proposer une variante mieux alignée sur le texte final (voir Règles du titre dans la spec partagée), mais la délimitation du sujet reste toujours ancrée sur l'entrée canonique et ses voisines, jamais sur le libellé retenu.

## Périmètre et continuité
La liste des 45 pastilles et les consignes de périmètre sont dans la spec partagée, section « Liste des 45 pastilles (pour la continuité) ». Applique-les avant de rédiger: situe la pastille, repère les 1 à 3 voisines qui recouvrent le sujet, dresse la courte liste "déjà traité ailleurs, à ne pas ré-expliquer", et garde le périmètre ancré sur le titre canonique (et non sur le libellé finalement retenu).

## Règles du texte et du titre
Voir la spec partagée, sections « Règles du texte » et « Règles du titre ». Elles s'appliquent à la pastille produite ici.

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

Titre canonique de la pastille (issu de la série, ancre de périmètre et libellé par défaut): [TITRE]
Angle imposé: [ANGLE, par exemple "Analogie: expliquer via une métaphore concrète du quotidien"]

À NE PAS ré-expliquer (déjà couvert par d'autres pastilles), à mentionner en une phrase au maximum:
[LISTE des points déjà traités ailleurs, à ne pas retraiter]

Brief de recherche (appuie-toi dessus, ne relance pas de recherche):
[BRIEF: faits clés, chiffres, sources]

Règles:
- Longueur selon la profondeur du sujet: 3 paragraphes si le sujet est léger, jusqu'à 4 s'il est dense. Chaque paragraphe fait 45 à 60 mots et 2 à 3 phrases, contrainte ferme. Prose continue, pas de listes ni de puces.
- Ordre des paragraphes: le dernier porte l'enjeu, ce que le sujet change concrètement pour le lecteur.
- Mets en gras et/ou en italique les termes qui portent vraiment le sens, une à deux emphases par paragraphe au maximum. Au-delà, le lecteur n'a plus de chemin de lecture privilégié.
- Ton décontracté, précis et léger, accessible mais techniquement juste. Évite le name-dropping: pas d'accumulation de noms de modèles, outils, entreprises ou chercheurs, privilégie l'explication du mécanisme.
- Rythme: privilégie des phrases plutôt courtes et directes, mais varie leur longueur et ajoute du liant (connecteurs, deux-points, points-virgules) pour éviter le style haché ou télégraphique. La lecture à voix haute doit rester fluide.
- Français. Ne mentionne aucune entreprise. Pas de tiret cadratin.
- Contenu autonome, compréhensible seul.
- Titre: rédige d'abord ton texte, puis propose le titre qui lui va le mieux. Le titre canonique ci-dessus est un point de départ, pas une contrainte: reprends-le tel quel, ajuste-le ou propose-en un nouveau, du moment qu'il reste dans le périmètre et le style de série (accroche courte et imagée, souvent deux-points puis glose en langage clair, ou question). N'hésite pas à t'en éloigner si ton angle appelle un meilleur titre; ne garde le canonique que s'il fait au moins aussi bien. Titre en français, sans tiret cadratin, sans nom d'entreprise, assez court pour un rendu image fiable.

Réponds exactement dans ce format:
TEXTE:
[les 3 à 4 paragraphes, 45 à 60 mots chacun]
TITRE:
[le titre retenu pour ce brouillon: le titre canonique tel quel, ou ta variante mieux alignée]
ILLUSTRATION_TITRE:
[une phrase décrivant le concept central à illustrer]
SCHEMA:
[décris en 2 à 3 lignes le diagramme et ses libellés en français. Le schéma est systématique. Il illustre le mécanisme exposé dans les deux premiers paragraphes, jamais la conclusion. Cinq blocs au maximum]
```

### Étape 4, fan-in et fusion (orchestrateur)
Attends les cinq retours, puis fusionne en une seule pastille finale:
- Retiens la structure la plus claire, la meilleure analogie, l'exemple le plus parlant, la correction la plus nette, la formulation la plus précise et le "pourquoi ça compte" le plus fort.
- Réécris en une seule voix cohérente. Pas d'effet patchwork.
- Choisis le titre: une fois le texte fusionné, retiens le titre qui lui correspond le mieux parmi les cinq propositions, ou synthétise-en un. Le titre canonique n'a qu'une préférence faible: retiens-le seulement à qualité vraiment égale, sinon préfère sans hésiter la variante qui sert mieux le texte final (même périmètre, style de série respecté). Le titre retenu remplace le canonique partout en aval, prompt image compris.
- Respecte la longueur adaptée à la profondeur et le ton décontracté, précis et léger, sans name-dropping.
- Le schéma est systématique: fusionne les meilleures idées de schéma reçues. Il illustre le mécanisme exposé dans les deux premiers paragraphes, jamais la conclusion, puisqu'il s'insère avant le dernier paragraphe.
- Vérifie l'ordre des paragraphes: le dernier doit porter l'enjeu. Les cinq angles peuvent produire une fusion où l'enjeu se retrouve au milieu, c'est à toi de le remettre en clôture.
- Rédige l'encadré de synthèse "L'essentiel" une fois le texte fusionné, jamais avant: deux à trois puces d'une ligne chacune, ou une phrase unique si le sujet n'a qu'un seul angle. Il dénoue ce que le titre annonce au lieu de le reformuler, et il ne doit pas pouvoir se substituer à l'article.
- Décide s'il y a lieu d'ajouter un bloc annexe, un seul au maximum: un encadré actionnable (prompt à copier, méthode courte) ou un encadré de mise en garde.
- Construis ensuite le prompt image unique (voir la spec partagée, section « Prompt de génération d'images » et « Charte graphique »).

Règles d'écriture pour la pastille finale: voir la spec partagée, section « Règles d'écriture pour la pastille finale ».

### Étape 5, revue critique et correction (trois sous-agents en parallèle, puis orchestrateur)
Quand la lancer: systématiquement à la première génération, une fois le texte fusionné et le prompt image construits. Ensuite, si l'utilisateur demande des ajustements, ne relance pas la revue d'office: propose-la, et ne la lance qu'avec son accord (elle coûte trois sous-agents de plus).

Le principe (les relecteurs rendent des constats, jamais une réécriture), ce que la revue peut juger (pas de rendu d'image, seulement le prompt image), les trois grilles et le gabarit de relecteur sont dans la spec partagée, section « Boite à outils de revue ». Applique-les tels quels.

Lance trois sous-agents en parallèle (parallélisme explicite, sinon l'exécution sera séquentielle), un par grille. Le contexte n'étant pas hérité, chaque prompt doit être autonome et contenir tout le nécessaire: le titre canonique et le titre retenu, le texte fusionné, le bloc prompt image, le brief de recherche, la liste "déjà traité ailleurs" (et les textes des pastilles voisines s'ils sont disponibles), et la liste des 45 titres pour repérer les chevauchements.

Fan-in et correction (orchestrateur): rassemble les constats, dédoublonne, arbitre les conseils contradictoires. Garde-fou anti-gonflement: entre "ajouter" et "raccourcir", la concision l'emporte, sauf erreur de fond avérée. Applique les constats bloquants et recommandés, écarte ou mentionne les mineurs. Le titre retenu est corrigé au même titre que le texte. Une seule passe, pas de boucle. Réécris la version corrigée en une seule voix, puis prépare le court résumé "Ce que la revue a corrigé" (voir Format de sortie).

### Points de vigilance Claude Code
- Parallélisme explicite: demande clairement cinq sous-agents en parallèle, sinon l'exécution sera séquentielle.
- Contexte non hérité: mets tout dans le prompt du sous-agent, en particulier le brief de recherche.
- Pas d'imbrication: un sous-agent ne peut pas en lancer un autre, garde recherche et fusion chez l'orchestrateur.
- Coût et limites: cinq sous-agents en parallèle multiplient l'usage de jetons et peuvent déclencher des limites de débit. En cas de limite, replie-toi sur une exécution séquentielle.
- Revue: la phase de revue ajoute trois sous-agents. Elle tourne d'office à la première génération; sur les demandes d'ajustement ultérieures, propose-la et ne la lance qu'avec l'accord de l'utilisateur. En cas de limite de débit, exécute les relecteurs en séquentiel ou replie-toi sur un relecteur global unique.
- Réemploi optionnel: tu peux définir les cinq angles comme sous-agents personnalisés dans .claude/agents/ pour les réutiliser, mais ce n'est pas obligatoire, les sous-agents polyvalents suffisent.

## Format de sortie
Le travail des sous-agents reste dans leur propre contexte, seuls leurs retours te reviennent. N'affiche donc que le livrable final (déjà corrigé par l'étape de revue), la conversation principale reste propre. Si l'utilisateur demande à voir l'atelier, restitue les cinq brouillons reçus et les constats de revue.

Livrable final, dans cet ordre:
- Quand une revue a eu lieu (systématiquement à la première génération), un court résumé "Ce que la revue a corrigé" (2 à 4 lignes) présentant les principaux ajustements, avant le reste. Lors d'ajustements ultérieurs sans revue, présente simplement la version ajustée sans ce résumé.
- Le titre retenu, affiché en tête comme titre de la pastille. S'il diffère du titre canonique de la série, ajoute juste en dessous une ligne discrète, par exemple: Titre canonique de la série: "...". Dites-moi si vous préférez le conserver, je reviens dessus en un mot. S'il est identique au canonique, n'ajoute pas cette ligne.
- L'encadré "L'essentiel", puis le texte de la pastille (3 à 4 paragraphes de 45 à 60 mots) dans sa version corrigée, puis le bloc annexe s'il y en a un.
- La légende du schéma, une phrase, et les deux textes alternatifs à renseigner à la diffusion: le titre exact pour l'illustration-titre, une phrase décrivant le schéma pour le second visuel.
- La rubrique de la pastille et le temps de lecture estimé, à reporter dans le bandeau du gabarit de diffusion (voir la spec partagée, section « Gabarit de diffusion »).
- Un bloc de code intitulé "Prompt images (à coller dans Gemini)", contenant le prompt unique prêt à copier.
- Une courte section "Sources" listant 2 à 4 références principales issues de l'étape de recherche, de préférence officielles ou originales. Cette section sert à la vérification et n'a pas vocation à être publiée dans la pastille.

Termine toujours par cette question exacte:
"Comment trouvez-vous le titre, le texte, l'image titre et le diagramme (si généré) ? Si une partie vous semble trop complexe, ou si vous souhaitez affiner le focus d'un visuel pour qu'il soit encore plus épuré, n'hésitez pas à me le faire savoir, et je l'ajusterai."
