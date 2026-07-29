---
description: Générateur de pastilles LLM en vrais sous-agents parallèles (variante Claude Code): cinq brouillons sous des angles différents, une fusion, puis une revue critique déléguée au skill `review` et une correction. Livrable: un titre, un texte court en français, et un prompt unique de génération d'images à coller dans le chat Gemini. Utilise ce skill dès qu'on te demande de rédiger, produire ou générer une pastille, une fiche ou un contenu court d'acculturation sur les LLM, l'IA générative, le prompting, les agents, le RAG, la confidentialité IA ou tout sujet de la liste des 45 pastilles ci-dessous, que le mot "pastille" soit employé ou non, et dès qu'on te fournit un titre issu de cette liste. Utilise-le aussi quand une pastille existante réclame du matériau neuf: changement d'axe, le sujet précis traité (régénération complète), ou un seul morceau à re-produire (fan-out ciblé). Retouches, réagencements et simples changements d'angle restent dans le fil, sans appeler refine.
---

# Générateur de pastilles LLM, version multi-agents (Claude Code)

## Ce que fait ce skill
Produit une pastille pédagogique complète à partir d'un titre. À la différence de la version chat, il lance de vrais sous-agents parallèles: une passe de recherche, puis cinq sous-agents indépendants qui rédigent chacun un brouillon (titre compris) sous un angle différent, puis une fusion par l'orchestrateur qui retient les meilleures formulations (titre compris), et enfin une revue critique déléguée au skill `review` suivie d'une correction. Livrable: le titre, le texte de la pastille et un prompt unique de génération d'images à coller dans le chat Gemini. Ensuite, une fois les deux visuels générés et collés dans la conversation, le skill `email` fabrique le courriel de diffusion; ce skill ne s'en occupe pas.

## Spec partagée (à lire en premier)
Les normes de la série vivent dans un fichier partagé, source unique commune à ce skill et aux skills `refine`, `review` et `email`: liste des 45 pastilles et périmètre, vocabulaire de l'axe et de l'angle avec la bibliothèque d'angles, Règles du texte, Règles du titre, Règles d'écriture pour la pastille finale, spec du prompt image et gabarits, charte graphique, doctrine d'évolution (retoucher, réagencer ou régénérer), boite à outils de revue. Lis-le avant de commencer:

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
L'axe retenu est le sujet précis que traiteront les cinq rédacteurs: il devient le champ « Axe de la pastille » du gabarit de l'étape 3, identique pour les cinq. Ne le confonds pas avec leurs angles, qui ne sont que des manières de l'aborder (voir « Axe et angle » dans la spec partagée). Si aucun affinement n'a été nécessaire, l'axe est simplement toute l'étendue du titre canonique.
Note aussi ce que ce dialogue produit d'exploitable: préférences, exclusions, exemples à privilégier ou à fuir, public visé plus précis. Tu le transmettras aux sous-agents à l'étape 3 (voir « Ce que tu transmets en plus »), car ils n'en sauront rien autrement.

### Étape 3, fan-out (cinq sous-agents en parallèle)
Lance cinq sous-agents via l'outil Task, dans le même tour, pour qu'ils s'exécutent en parallèle. Sois explicite sur le parallélisme: par défaut Claude Code reste séquentiel, il ne parallélise que si tu le demandes clairement. Un sous-agent par angle.

**Choisis les angles avant de lancer**, selon la spec partagée, sections « Bibliothèque d'angles » et « Composer le jeu d'angles »: deux slots de noyau (mécanique, enjeu) et trois slots libres adaptés à l'axe et à la rubrique, avec le jeu par défaut (analogie, cas d'usage, idée reçue, mécanique, enjeu) comme choix de repli. Trois points s'appliquent ici et méritent d'être rappelés:
- La contrainte de diversité est la raison d'être du fan-out. Trois slots libres qui ouvrent sur la même porte ne valent qu'un seul brouillon payé trois fois.
- Ne choisis pas les angles d'après ce que tu écrirais toi-même: ce serait remplacer cinq points de vue par cinq versions du tien. L'angle qui te parait le moins naturel est souvent celui qui rapportera le plus.
- Annonce les angles retenus en une ligne quand tu t'écartes du jeu par défaut, et garde-en la trace: elle servira si l'utilisateur demande plus tard un autre traitement.

Ces angles sont des traitements, pas des sujets. Le sujet, lui, est l'axe: il est le même pour tous les rédacteurs. Ne confonds pas les deux, la spec partagée y consacre une section (« Axe et angle »), et la confusion coûte cher au moment de relancer.

#### Fan-out relancé sur un nouvel axe (régénération)
Quand la régénération vient d'un changement d'axe (voir étape 6), **les angles ne changent pas**: c'est le sujet qui change, pas la manière de l'aborder. Tu relances le même jeu d'angles sur le nouvel axe, avec le brief mis à jour si l'axe appelle des faits que l'ancien ne portait pas. Une exception raisonnable: si le nouvel axe rend un slot libre manifestement inadapté (un angle « ordre de grandeur » sur un axe sans chiffres), remplace ce slot et dis-le, sans toucher au noyau ni aux autres. Le champ « Angle imposé » du gabarit garde sa valeur habituelle, un angle par sous-agent, et c'est la formulation de l'axe (dans le titre canonique et le brief) qui porte le changement.

Si la régénération est demandée sans axe nouveau (« recommence », « je n'aime aucun des cinq »), garde l'axe. Là, en revanche, rejouer exactement le même jeu d'angles a peu de chances de mieux tomber: change les trois slots libres pour d'autres portes d'entrée de la bibliothèque, et garde le noyau. C'est le fan-out qui n'a pas produit, autant l'ouvrir ailleurs.

#### Angle imposé par l'utilisateur (cas plus rare)
Il arrive que l'utilisateur impose non pas un sujet mais un traitement: « pars d'une situation de travail », « prends-le par l'idée reçue ». Alors seulement le jeu d'angles tombe, puisqu'il vient d'en choisir un.

Premier réflexe, avant tout fan-out: **regarde si tu n'as pas déjà ce brouillon.** Consulte la trace des angles employés: si celui qu'il demande en faisait partie, son brouillon existe. Repartir de ce brouillon et le réécrire en une seule voix coûte zéro sous-agent et donne exactement ce qu'il demande. C'est le cas le plus fréquent, et le plus économique.

Ne lance un fan-out que si ce brouillon n'est plus disponible (contexte perdu) ou si l'angle demandé ne figurait pas dans le jeu retenu. Dans ce cas, les cinq sous-agents partagent l'angle imposé et se distinguent par leur traitement à l'intérieur de cet angle: cinq situations de travail différentes, cinq malentendus différents, cinq entrées différentes dans le mécanisme. Le champ « Angle imposé » porte alors l'angle commun, suivi de la variante propre à chaque sous-agent.

#### Fan-out ciblé (reprise d'une partie seulement)
Quand seul un morceau délimité est à re-produire et que le reste tient (voir étape 6), ne relance pas cinq brouillons de pastille entière: tu jetterais ce que l'utilisateur vient de valider, et tu aurais cinq textes complets à départager pour remplacer un paragraphe. Trois rédacteurs sur le seul morceau suffisent. Adapte le gabarit:
- **Remplace « Angle imposé » par la commande du morceau**: ce qu'il doit faire, où il s'insère, son format exact (un paragraphe de 45 à 60 mots, deux à trois puces, un titre, une description de schéma).
- **Ajoute le texte conservé**, en clair, avec son mandat: « Voici la pastille telle qu'elle reste. Ne la réécris pas. Accorde-toi à sa voix, et ne répète rien de ce qu'elle dit déjà. » C'est cette pièce qui rend le fragment raccordable, et c'est ici que l'ancien texte sert vraiment: il ne fixe pas l'écriture, il en donne le cadre.
- **Ajoute le passage écarté et le grief**, marqué comme écarté: à éviter, pas à corriger. À cette échelle un fragment balise sans enfermer, contrairement au texte entier d'une régénération complète (voir la spec partagée, « Ce qu'on transmet de l'ancien texte »).
- **Demande une seule sortie, le fragment**, dans le format voulu. Pas de pastille complète: un rédacteur à qui on laisse la bride réécrit tout, et tu te retrouves à arbitrer ce que tu ne voulais pas changer.

Fan-in: retiens le meilleur fragment ou synthétises-en un, insère-le, puis vérifie le raccord, transitions, redites avec le texte conservé, comptages (45 à 60 mots, puces, emphases), enjeu toujours en clôture. Re-synchronise le prompt image seulement si le morceau touchait au mécanisme illustré ou au titre. Revue proposée et non imposée: la pastille n'est pas neuve. En sortie, affiche le texte complet une fois recomposé, en signalant ce qui a changé.

#### Ce que tu transmets en plus (aiguillage des sous-agents)
Les sous-agents ne voient rien de la conversation. Tout ce qui a orienté la demande doit donc leur être écrit, sinon ils rejouent exactement la version que l'utilisateur vient de refuser: ils n'ont aucun moyen de savoir qu'elle a existé. C'est le bloc « Consignes de l'utilisateur » du gabarit ci-dessous, à remplir quand tu as de la matière, à omettre sinon.

Trois choses à y transmettre, quand elles existent:
- **Le retour de l'utilisateur**: ce qu'il demande, ce qu'il a rejeté, et pourquoi. Cite ses mots plutôt que de les paraphraser: « trop scolaire », « ça ne parle pas à un non-technique », « l'analogie tombe à plat » portent le grief exact, là où ta reformulation le lisse et le rend inoffensif.
- **Ce qui est validé et doit survivre**: un titre qui lui plaît, un exemple qu'il veut garder, une formule réussie, une contrainte de longueur qu'il a fixée. Sans cela, la régénération jette aussi ce qui marchait.
- **Ce qui est écarté**: une analogie déjà vue ailleurs, un exemple qui a raté, un angle refusé, un chiffre qu'il conteste.

Comment le formuler:
- Distingue le ferme du préférable, et dis lequel est lequel. « Le titre reste tel quel » est une contrainte; « il trouvait la métaphore un peu scolaire » est une préférence. Un sous-agent qui ne peut pas faire la différence traite tout comme un ordre.
- Reste court, quelques lignes. Plus tu contrains, plus les cinq brouillons se ressemblent, et c'est leur diversité qui fait la valeur de la fusion. Ne transmets que ce qui change vraiment l'écriture.
- N'invente pas de consigne et ne comble pas les silences: si tu n'as rien reçu, omets le bloc. Une consigne inventée est une contrainte que l'utilisateur n'a pas posée.
- **Le texte refusé ne part jamais aux rédacteurs.** Un sous-agent qui le lit en écrit une variante: c'est un ancrage, pas une information, et les défauts de l'ancien texte voyagent avec lui. Les cinq brouillons convergeraient alors vers une réécriture de ce qu'on vient d'écarter, ce qui vide le fan-out de son intérêt et coûte aux cinq leur liberté de trouver autre chose. Le grief se transmet, le texte non: c'est le rôle des champs RETOUR et À ÉVITER, qui disent ce qui n'allait pas sans montrer ce qui n'allait pas.
- Exception étroite: une formulation précise que l'utilisateur a validée (une phrase, un exemple, un titre) se transmet dans À CONSERVER. Un fragment choisi n'ancre pas, il oriente; c'est le texte entier qui ancre.
- Si tu te dis que les rédacteurs ont besoin de l'ancien texte pour comprendre quoi faire, la demande n'est probablement pas une régénération mais un réagencement: dans ce cas, ne lance pas de fan-out et réorganise toi-même (voir la spec partagée, section « Faire évoluer une pastille »).
- Ce bloc sert aussi à la première génération, quand l'étape 2 a produit des préférences ou des exclusions: mêmes règles.

Comme le contexte n'est pas hérité, chaque prompt de sous-agent doit être autonome et contenir tout le nécessaire. Utilise ce gabarit, en remplaçant les crochets:
```
Tu rédiges un brouillon d'une pastille pédagogique interne sur les LLM. Tu travailles seul, sans accès au reste de la conversation.

Titre canonique de la pastille (issu de la série, ancre de périmètre et libellé par défaut): [TITRE]
Axe de la pastille (le sujet précis à traiter dans ce thème, commun aux cinq rédacteurs, non négociable): [AXE, ou "toute l'étendue du titre canonique" si aucun axe particulier n'a été retenu]
Angle imposé (ta manière d'aborder cet axe, propre à toi): [ANGLE, par exemple "Analogie: expliquer via une métaphore concrète du quotidien"]

Consignes de l'utilisateur (elles priment sur tes préférences de rédaction, mais pas sur les Règles ci-dessous: si une consigne les contredit, respecte les Règles et dis-le en fin de réponse; bloc à supprimer s'il n'y en a pas):
[RETOUR: ce que l'utilisateur demande et ce qu'il a rejeté, avec ses mots]
[À CONSERVER: ce qui est validé et doit survivre, en précisant ce qui est une contrainte ferme]
[À ÉVITER: analogies, exemples, angles ou formulations écartés]

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
- Reste sur l'axe indiqué: c'est le sujet, tu ne le déplaces pas. Ton angle ne porte que sur la manière de l'aborder.
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
CONFLIT:
[une ligne, seulement si une consigne de l'utilisateur contredit une Règle ci-dessus, en disant laquelle tu as respectée. Rien à signaler: omets ce champ]
```

### Étape 4, fan-in et fusion (orchestrateur)
Attends les cinq retours, puis fusionne en une seule pastille finale:
- Retiens la structure la plus claire, la meilleure image, l'exemple le plus parlant, la correction la plus nette, la formulation la plus précise et le "pourquoi ça compte" le plus fort. Les apports attendus dépendent du jeu d'angles que tu as retenu: cherche dans chaque brouillon ce que son angle était seul à pouvoir produire.
- Réécris en une seule voix cohérente. Pas d'effet patchwork.
- Choisis le titre: une fois le texte fusionné, retiens le titre qui lui correspond le mieux parmi les cinq propositions, ou synthétise-en un. Même méthode pour les puces de l'encadré, qui arrivent elles aussi en cinq versions. Le titre canonique n'a qu'une préférence faible: retiens-le seulement à qualité vraiment égale, sinon préfère sans hésiter la variante qui sert mieux le texte final (même périmètre, style de série respecté). Le titre retenu remplace le canonique partout en aval, prompt image compris.
- Respecte la longueur adaptée à la profondeur et le ton décontracté, précis et léger, sans name-dropping.
- Le schéma est systématique: fusionne les meilleures idées de schéma reçues. Il illustre le mécanisme exposé dans les deux premiers paragraphes, jamais la conclusion, puisqu'il s'insère avant le dernier paragraphe.
- Vérifie l'ordre des paragraphes: le dernier doit porter l'enjeu. Les cinq angles peuvent produire une fusion où l'enjeu se retrouve au milieu, c'est à toi de le remettre en clôture.
- Si tu as transmis des consignes de l'utilisateur, vérifie que la fusion y répond, titre et encadré compris: c'est toi qui en réponds, pas les brouillons. Regarde aussi les champs CONFLIT éventuels: quand plusieurs sous-agents signalent la même contradiction entre une consigne et une norme de la spec, c'est la consigne qui pose problème, pas eux. Tout point non satisfait (consigne contraire à la spec, ou deux consignes qui s'opposent) se dit en une ligne dans la sortie, à l'utilisateur de trancher; ne le laisse pas passer en silence.
- Fusionne l'encadré de synthèse "L'essentiel" une fois le texte fusionné, jamais avant: retiens les meilleures puces parmi les cinq propositions reçues, ou synthétise-en de nouvelles si aucune ne dénoue vraiment le titre. Deux à trois puces, douze mots ou soixante-dix signes chacune au maximum, ou une phrase unique si le sujet n'a qu'un seul angle. Compte les mots: une puce qui déborde porte en général deux idées, coupe-la ou choisis. L'encadré dénoue ce que le titre annonce au lieu de le reformuler, et il ne doit pas pouvoir se substituer à l'article.
- Décide s'il y a lieu d'ajouter un bloc annexe, un seul au maximum: un encadré actionnable (prompt à copier, méthode courte) ou un encadré de mise en garde.
- Construis ensuite le prompt image unique (voir la spec partagée, section « Prompt de génération d'images » et « Charte graphique »).

Règles d'écriture pour la pastille finale: voir la spec partagée, section « Règles d'écriture pour la pastille finale ».

### Étape 5, revue critique (déléguée au skill `review`) et correction
Tu ne conduis pas la revue toi-même: invoque le skill `review` via l'outil Skill, et passe-lui le dossier complet, à savoir le titre canonique et le titre retenu, le texte fusionné, le bloc prompt image, le brief de recherche de l'étape 1, la liste "déjà traité ailleurs", les textes voisins s'ils sont disponibles, et les consignes de l'utilisateur si tu en as transmis aux rédacteurs: les relecteurs doivent savoir ce qui a été imposé, sans quoi ils le compteront comme un défaut. Précise que tu l'appelles depuis `generate`: dans ce mode, il rend la liste consolidée des constats et n'affiche pas de rapport.

Quand la déclencher: systématiquement à la première génération, une fois le texte fusionné et le prompt image construits. Ensuite, si l'utilisateur demande des ajustements, ne la relance pas d'office: propose-la, et ne la déclenche qu'avec son accord (elle coûte trois sous-agents de plus).

Correction (toi, orchestrateur): la revue rend des constats déjà dédoublonnés et arbitrés, à toi de les appliquer. Réécris la version corrigée en une seule voix, jamais par recollage des formulations des relecteurs, puis prépare le court résumé "Ce que la revue a corrigé" (voir Format de sortie). Les règles d'arbitrage sont dans la spec partagée, section « Arbitrage des constats »: si un constat contredit une norme de la spec, écarte-le en le disant.

### Étape 6, demandes après livraison (elles restent ici)
Le livrable rendu, l'utilisateur demande presque toujours des changements. **Ils se traitent ici, dans le fil de la conversation, sans invoquer aucun skill.** Tu as tout le dossier sous les yeux: le brief et ses sources, le périmètre et la liste "déjà traité ailleurs", les cinq brouillons, le texte fusionné, les deux titres, le prompt image et les constats de revue déjà appliqués.

Commence par trancher l'ampleur, comme le demande la spec partagée, section « Faire évoluer une pastille »: retouche de surface, réagencement, reprise ciblée, changement d'angle, ou changement d'axe ? Distingue bien l'axe (le sujet précis, dont un changement demande du matériau neuf) de l'angle (le traitement, dont le matériau est souvent déjà là): voir « Axe et angle » dans la spec. Deux questions suffisent: as-tu besoin de matière que tu n'as pas, et s'il faut produire, combien faut-il jeter ? Prends toujours la réponse la plus légère qui fait le travail.

**Retouche de surface**, le cas courant: applique la spec partagée (diff minimal, re-synchronisation du prompt image au strict nécessaire, revue proposée et non imposée, sortie réduite à ce qui change). N'appelle pas `refine`: il sert à reconstituer un dossier perdu, situation exactement inverse de la tienne, et l'appeler ici te ferait redemander des artefacts que tu possèdes et remplacer ton vrai brief par un brief reconstitué. Deux points qui reviennent souvent:
- Pas de nouvelle recherche pour une retouche de style: le brief de l'étape 1 est en contexte et fait foi. Ne recherche que si la retouche touche un fait ou un chiffre qu'il ne couvre pas.
- Les cinq brouillons restent utilisables: si la retouche demande une autre formulation d'un passage, va chercher dans les brouillons reçus avant d'en inventer une, l'angle voulu y est peut-être déjà.

**Réagencement**, quand l'axe et le matériau tiennent mais que l'architecture ne va pas (ordre des paragraphes, point secondaire à promouvoir en coeur, encadré à redécouper, schéma à recentrer sur un autre moment du texte): réorganise toi-même, dans le fil, sans relancer de sous-agents. Tu as le texte, le brief et les cinq brouillons: le matériau existe déjà, seul son agencement change. Applique les consignes de réagencement de la spec partagée, et sers-toi des brouillons comme réserve, un passage mieux tourné par l'un d'eux valant mieux qu'une reformulation improvisée. Réserve le fan-out aux cas où il faut vraiment de la matière neuve.

**Reprise ciblée**, le cas intermédiaire: un morceau délimité doit être re-produit (un paragraphe qui n'explique rien, une analogie qui tombe à plat, l'encadré à refaire, un titre à retrouver) alors que le reste tient. Une retouche ne suffit pas puisqu'il faut vraiment produire autre chose, et une régénération complète jetterait du travail validé. Lance un fan-out ciblé sur ce seul morceau, voir « Fan-out ciblé » à l'étape 3, en transmettant le texte conservé comme cadre. Ici, pas de confirmation solennelle à demander: trois sous-agents, rien de validé n'est menacé, le prompt image ne bouge que si le morceau touchait au mécanisme illustré. Dis en une ligne ce que tu fais, et fais-le.

**Changement d'angle** (« pars plutôt d'une situation de travail », « prends-le par l'idée reçue »): ce n'est pas une demande structurelle, l'axe ne bouge pas. Le brouillon écrit sous cet angle est probablement dans ton contexte: reprends-le comme base, réécris en une seule voix et en réappliquant les normes de la série, sans relancer de sous-agents. Voir « Angle imposé par l'utilisateur » à l'étape 3 pour le cas où ce brouillon manque.

**Demande structurelle** (changement d'axe, déplacement du thème): là ni la retouche, ni le réagencement, ni la reprise ciblée ne suffisent, il faut du matériau neuf sur toute la pastille, donc relancer la génération. Demande-le à l'utilisateur avant de le faire, en une question qui dit ce que cela implique (cinq nouveaux brouillons, titre possiblement différent, visuels périmés et courriel à refabriquer), sauf s'il a déjà été explicite sur la régénération: dans ce cas relance sans redemander. Les règles complètes (signaux structurels, question à poser, exception, ce qui se garde) sont dans la spec partagée, section « Régénération ».

Comment relancer, concrètement: tu ne repars pas de l'étape 1. Tu reprends à l'étape 3 (fan-out) avec le brief déjà en contexte, ou à l'étape 2 si le nouvel axe appelle des sources que le brief ne porte pas. Le titre canonique et le périmètre restent les tiens. Le nouvel axe est partagé par les cinq sous-agents, qui conservent leurs cinq angles (voir « Fan-out relancé sur un nouvel axe » à l'étape 3): un axe nouveau ne rend pas les angles caducs. La fusion suit son cours normal, et la revue redevient d'office puisqu'il s'agit d'un texte neuf.

Le point à ne pas manquer: **transmets le retour de l'utilisateur aux cinq sous-agents** (son grief avec ses mots, ce qui est validé, ce qui est écarté), comme décrit dans « Ce que tu transmets en plus » à l'étape 3. Tu es le seul à l'avoir entendu; eux repartent de zéro et refont, sans le savoir, exactement la pastille qu'il vient de refuser. En revanche, le texte refusé lui-même ne leur est pas transmis: il les ancrerait sur ce qu'on veut quitter. Le livrable reprend alors le format complet de la première génération, prompt image compris, avec la mention que les visuels précédents sont à refaire.

Ce régime vaut pour toute la suite de la conversation, quel que soit le nombre d'échanges, et y compris après un passage par `email`.

### Points de vigilance Claude Code
- Parallélisme explicite: demande clairement cinq sous-agents en parallèle, sinon l'exécution sera séquentielle.
- Contexte non hérité: mets tout dans le prompt du sous-agent, en particulier le brief de recherche.
- Pas d'imbrication: un sous-agent ne peut pas en lancer un autre, garde recherche et fusion chez l'orchestrateur.
- Coût et limites: cinq sous-agents en parallèle multiplient l'usage de jetons et peuvent déclencher des limites de débit. En cas de limite, replie-toi sur une exécution séquentielle.
- Revue: elle est portée par le skill `review`, qui ajoute trois sous-agents. Elle est déclenchée d'office à la première génération; sur les demandes d'ajustement ultérieures, propose-la et ne la déclenche qu'avec l'accord de l'utilisateur. Les replis (séquentiel, relecteur global unique) sont gérés par `review`, pas ici.
- Retouches et réagencements: ils restent dans ce skill (étape 6), et le réagencement ne relance aucun sous-agent. Entre eux et la régénération complète, la reprise ciblée ne mobilise que trois rédacteurs sur un fragment: c'est souvent la bonne réponse, ne saute pas directement au fan-out complet. Le réflexe d'appeler `refine` dès que l'utilisateur demande une modification est l'erreur la plus fréquente: `refine` réhydrate un contexte perdu, or ici il est intact.
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
- Quand tu t'es écarté du jeu d'angles par défaut, une ligne discrète disant lesquels tu as retenus et pourquoi. Elle sert de trace: sans elle, une demande ultérieure de traitement particulier ne peut plus être rapprochée des brouillons existants.
- Une courte section "Sources" listant 2 à 4 références principales issues de l'étape de recherche, de préférence officielles ou originales. Cette section sert à la vérification et n'a pas vocation à être publiée dans la pastille.

Termine toujours par cette question exacte:
"Comment trouvez-vous le titre, le texte, l'image titre et le diagramme (si généré) ? Si une partie vous semble trop complexe, ou si vous souhaitez affiner le focus d'un visuel pour qu'il soit encore plus épuré, n'hésitez pas à me le faire savoir, et je l'ajusterai."
