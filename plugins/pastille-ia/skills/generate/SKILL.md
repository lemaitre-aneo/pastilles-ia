---
description: Variante Claude Code du générateur de pastilles LLM, qui lance réellement plusieurs sous-agents en parallèle. Génère une pastille de communication interne sur les LLM (un titre, un texte court en français, plus un prompt unique de génération d'images à coller dans le chat Gemini), via cinq sous-agents indépendants qui proposent chacun aussi un titre, une fusion, puis une revue critique déléguée au skill `review` et une correction. Utilise ce skill dès qu'on te demande de rédiger, produire ou générer une pastille, une fiche ou un contenu court d'acculturation sur les LLM, l'IA générative, le prompting, les agents, le RAG, la confidentialité IA ou tout sujet de la liste des 45 pastilles ci-dessous, que le mot "pastille" soit employé ou non. Utilise-le aussi dès qu'on te fournit un titre issu de cette liste. Les retouches demandées ensuite restent dans ce skill, dans le fil: n'appelle pas refine, réservé aux pastilles recollées sans leur contexte.
---

# Générateur de pastilles LLM, version multi-agents (Claude Code)

## Ce que fait ce skill
Produit une pastille pédagogique complète à partir d'un titre. À la différence de la version chat, il lance de vrais sous-agents parallèles: une passe de recherche, puis cinq sous-agents indépendants qui rédigent chacun un brouillon (titre compris) sous un angle différent, puis une fusion par l'orchestrateur qui retient les meilleures formulations (titre compris), et enfin une revue critique déléguée au skill `review` suivie d'une correction. Livrable: le titre, le texte de la pastille et un prompt unique de génération d'images à coller dans le chat Gemini. Ensuite, une fois les deux visuels générés et collés dans la conversation, le skill `email` fabrique le courriel de diffusion; ce skill ne s'en occupe pas.

## Spec partagée (à lire en premier)
Les normes de la série vivent dans un fichier partagé, source unique commune à ce skill et aux skills `refine`, `review` et `email`: liste des 45 pastilles et périmètre, Règles du texte, Règles du titre, Règles d'écriture pour la pastille finale, spec du prompt image et gabarits, charte graphique, doctrine de retouche, boite à outils de revue. Lis-le avant de commencer:

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
- Encadré « L'essentiel »: une fois ton texte écrit, propose deux à trois puces, ou une seule phrase si ton angle n'a qu'une idée. Chaque puce tient en douze mots ou soixante-dix signes au maximum: au delà elle passe sur deux lignes à la diffusion et l'encadré cesse d'être un balayage. Elle dénoue ce que le titre annonce au lieu de le reformuler, et l'encadré ne doit pas pouvoir remplacer le texte.
- Titre: rédige d'abord ton texte, puis propose le titre qui lui va le mieux. Le titre canonique ci-dessus est un point de départ, pas une contrainte: reprends-le tel quel, ajuste-le ou propose-en un nouveau, du moment qu'il reste dans le périmètre et le style de série (accroche courte et imagée, souvent deux-points puis glose en langage clair, ou question). N'hésite pas à t'en éloigner si ton angle appelle un meilleur titre; ne garde le canonique que s'il fait au moins aussi bien. Titre en français, sans tiret cadratin, sans nom d'entreprise, assez court pour un rendu image fiable.

Réponds exactement dans ce format:
TEXTE:
[les 3 à 4 paragraphes, 45 à 60 mots chacun]
ESSENTIEL:
- [puce 1, douze mots ou soixante-dix signes au maximum]
- [puce 2]
- [puce 3, facultative]
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
- Choisis le titre: une fois le texte fusionné, retiens le titre qui lui correspond le mieux parmi les cinq propositions, ou synthétise-en un. Même méthode pour les puces de l'encadré, qui arrivent elles aussi en cinq versions. Le titre canonique n'a qu'une préférence faible: retiens-le seulement à qualité vraiment égale, sinon préfère sans hésiter la variante qui sert mieux le texte final (même périmètre, style de série respecté). Le titre retenu remplace le canonique partout en aval, prompt image compris.
- Respecte la longueur adaptée à la profondeur et le ton décontracté, précis et léger, sans name-dropping.
- Le schéma est systématique: fusionne les meilleures idées de schéma reçues. Il illustre le mécanisme exposé dans les deux premiers paragraphes, jamais la conclusion, puisqu'il s'insère avant le dernier paragraphe.
- Vérifie l'ordre des paragraphes: le dernier doit porter l'enjeu. Les cinq angles peuvent produire une fusion où l'enjeu se retrouve au milieu, c'est à toi de le remettre en clôture.
- Fusionne l'encadré de synthèse "L'essentiel" une fois le texte fusionné, jamais avant: retiens les meilleures puces parmi les cinq propositions reçues, ou synthétise-en de nouvelles si aucune ne dénoue vraiment le titre. Deux à trois puces, douze mots ou soixante-dix signes chacune au maximum, ou une phrase unique si le sujet n'a qu'un seul angle. Compte les mots: une puce qui déborde porte en général deux idées, coupe-la ou choisis. L'encadré dénoue ce que le titre annonce au lieu de le reformuler, et il ne doit pas pouvoir se substituer à l'article.
- Décide s'il y a lieu d'ajouter un bloc annexe, un seul au maximum: un encadré actionnable (prompt à copier, méthode courte) ou un encadré de mise en garde.
- Construis ensuite le prompt image unique (voir la spec partagée, section « Prompt de génération d'images » et « Charte graphique »).

Règles d'écriture pour la pastille finale: voir la spec partagée, section « Règles d'écriture pour la pastille finale ».

### Étape 5, revue critique (déléguée au skill `review`) et correction
Tu ne conduis pas la revue toi-même: invoque le skill `review` via l'outil Skill, et passe-lui le dossier complet, à savoir le titre canonique et le titre retenu, le texte fusionné, le bloc prompt image, le brief de recherche de l'étape 1, la liste "déjà traité ailleurs" et les textes voisins s'ils sont disponibles. Précise que tu l'appelles depuis `generate`: dans ce mode, il rend la liste consolidée des constats et n'affiche pas de rapport.

Quand la déclencher: systématiquement à la première génération, une fois le texte fusionné et le prompt image construits. Ensuite, si l'utilisateur demande des ajustements, ne la relance pas d'office: propose-la, et ne la déclenche qu'avec son accord (elle coûte trois sous-agents de plus).

Correction (toi, orchestrateur): la revue rend des constats déjà dédoublonnés et arbitrés, à toi de les appliquer. Réécris la version corrigée en une seule voix, jamais par recollage des formulations des relecteurs, puis prépare le court résumé "Ce que la revue a corrigé" (voir Format de sortie). Les règles d'arbitrage sont dans la spec partagée, section « Arbitrage des constats »: si un constat contredit une norme de la spec, écarte-le en le disant.

### Étape 6, retouches après livraison (elles restent ici)
Le livrable rendu, l'utilisateur demande presque toujours des ajustements: un paragraphe à alléger, un titre à resserrer, une puce trop longue, un schéma à recadrer. **Ces retouches se traitent ici, dans le fil de la conversation, sans invoquer aucun skill.** Tu as tout le dossier sous les yeux: le brief et ses sources, le périmètre et la liste "déjà traité ailleurs", les cinq brouillons, le texte fusionné, les deux titres, le prompt image et les constats de revue déjà appliqués.

N'appelle pas `refine`. Ce skill sert à reconstituer un dossier perdu, situation exactement inverse de la tienne: l'appeler ici te ferait redemander des artefacts que tu possèdes et remplacer ton vrai brief par un brief reconstitué, donc moins fiable. Ne relance pas `generate` non plus: on ne repart pas de cinq brouillons pour changer un mot.

Comment retoucher: applique la spec partagée, section « Retouche d'une pastille » (diff minimal, re-synchronisation du prompt image au strict nécessaire, revue proposée et non imposée, sortie réduite à ce qui change). Deux points qui reviennent souvent à ce stade:
- Pas de nouvelle recherche pour une retouche de style: le brief de l'étape 1 est en contexte et fait foi. Ne recherche que si la retouche touche un fait ou un chiffre qu'il ne couvre pas.
- Les cinq brouillons restent utilisables: si la retouche demande une autre formulation d'un passage, va chercher dans les brouillons reçus avant d'en inventer une, l'angle voulu y est peut-être déjà.

Ce régime vaut pour toute la suite de la conversation, quel que soit le nombre de retouches, et y compris après un passage par `email`.

### Points de vigilance Claude Code
- Parallélisme explicite: demande clairement cinq sous-agents en parallèle, sinon l'exécution sera séquentielle.
- Contexte non hérité: mets tout dans le prompt du sous-agent, en particulier le brief de recherche.
- Pas d'imbrication: un sous-agent ne peut pas en lancer un autre, garde recherche et fusion chez l'orchestrateur.
- Coût et limites: cinq sous-agents en parallèle multiplient l'usage de jetons et peuvent déclencher des limites de débit. En cas de limite, replie-toi sur une exécution séquentielle.
- Revue: elle est portée par le skill `review`, qui ajoute trois sous-agents. Elle est déclenchée d'office à la première génération; sur les demandes d'ajustement ultérieures, propose-la et ne la déclenche qu'avec l'accord de l'utilisateur. Les replis (séquentiel, relecteur global unique) sont gérés par `review`, pas ici.
- Retouches: elles restent dans ce skill (étape 6). Le réflexe d'appeler `refine` dès que l'utilisateur demande une modification est l'erreur la plus fréquente: `refine` réhydrate un contexte perdu, or ici il est intact.
- Réemploi optionnel: tu peux définir les cinq angles comme sous-agents personnalisés dans .claude/agents/ pour les réutiliser, mais ce n'est pas obligatoire, les sous-agents polyvalents suffisent.

## Format de sortie
Le travail des sous-agents reste dans leur propre contexte, seuls leurs retours te reviennent. N'affiche donc que le livrable final (déjà corrigé par l'étape de revue), la conversation principale reste propre. Si l'utilisateur demande à voir l'atelier, restitue les cinq brouillons reçus et les constats de revue.

Livrable final, dans cet ordre:
- Quand une revue a eu lieu (systématiquement à la première génération), un court résumé "Ce que la revue a corrigé" (2 à 4 lignes) présentant les principaux ajustements, avant le reste.

Ce format complet vaut pour la première livraison. Les retouches ultérieures (étape 6) n'affichent que ce qui change, sans résumé de revue et sans rejouer le livrable entier: l'utilisateur a déjà tout le reste plus haut dans la conversation.
- Le titre retenu, affiché en tête comme titre de la pastille. S'il diffère du titre canonique de la série, ajoute juste en dessous une ligne discrète, par exemple: Titre canonique de la série: "...". Dites-moi si vous préférez le conserver, je reviens dessus en un mot. S'il est identique au canonique, n'ajoute pas cette ligne.
- L'encadré "L'essentiel", puis le texte de la pastille (3 à 4 paragraphes de 45 à 60 mots) dans sa version corrigée, puis le bloc annexe s'il y en a un.
- La légende du schéma, une phrase, et les deux textes alternatifs à renseigner à la diffusion: le titre exact pour l'illustration-titre, une phrase décrivant le schéma pour le second visuel.
- La rubrique de la pastille et le temps de lecture estimé, à reporter dans le bandeau du gabarit de diffusion (voir la spec partagée, section « Gabarit de diffusion »). La rubrique se déduit de la position du sujet dans la liste des 45. Le numéro affiché, lui, est le numéro de diffusion et appartient à l'utilisateur: s'il ne l'a pas donné, propose la position dans la liste et demande confirmation, sans la retenir en silence.
- Un bloc de code intitulé "Prompt images (à coller dans Gemini)", contenant le prompt unique prêt à copier.
- Une courte section "Sources" listant 2 à 4 références principales issues de l'étape de recherche, de préférence officielles ou originales. Cette section sert à la vérification et n'a pas vocation à être publiée dans la pastille.

Termine toujours par cette question exacte:
"Comment trouvez-vous le titre, le texte, l'image titre et le diagramme (si généré) ? Si une partie vous semble trop complexe, ou si vous souhaitez affiner le focus d'un visuel pour qu'il soit encore plus épuré, n'hésitez pas à me le faire savoir, et je l'ajusterai."
