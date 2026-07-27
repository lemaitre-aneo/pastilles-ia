---
description: Revue critique d'une pastille LLM par trois relecteurs indépendants et parallèles (fond et exactitude, forme et pédagogie, conformité et visuel), qui rendent des constats localisés avec gravité et correctif, consolidés et arbitrés, sans réécrire le texte. Utilise ce skill dès qu'on demande un avis critique, une relecture, une revue, une validation ou un diagnostic sur une pastille existante, sans demander de modification. Les skills generate et refine l'invoquent aussi au moment de leur revue. Si l'utilisateur demande une modification du texte, c'est refine qu'il faut, pas ce skill; pour créer une pastille, generate.
---

# Revue critique d'une pastille (trois relecteurs)

## Ce que fait ce skill
Fait relire une pastille par trois relecteurs indépendants, un par grille, puis consolide leurs constats: dédoublonnés, arbitrés, classés par gravité. Il ne réécrit rien. Le diagnostic et le soin sont séparés, exprès: un relecteur qui réécrit fait disparaître le défaut sans que personne ne l'ait vu, et trois relecteurs qui réécrivent produisent un patchwork.

Deux façons d'arriver ici, et la sortie n'est pas la même:
- **Invoqué par un humain**, sur une pastille existante: le livrable est le rapport de revue, et rien d'autre. Tu ne touches pas au texte. Tu proposes ensuite `refine` pour appliquer.
- **Invoqué par `generate` ou `refine`**, au moment de leur revue: le livrable est la liste consolidée des constats, rendue au processus appelant, qui applique et réécrit. N'affiche pas le rapport comme un livrable, et ne réécris pas: ce n'est pas ton rôle dans ce mode.

## Spec partagée (à lire en premier)
Les normes de la série vivent dans un fichier partagé, source unique commune aux quatre skills. La section « Boite à outils de revue » porte le principe des constats, ce que la revue peut juger, les trois grilles, les règles d'arbitrage et le gabarit de relecteur. Applique-les tels quels, ne les réinvente pas ici.

`${CLAUDE_SKILL_DIR}/references/regles-pastille.md`

## Environnement requis
Trois sous-agents (outil Task) en parallèle. Si les sous-agents ne sont pas disponibles, replie-toi sur un relecteur global unique porté par l'orchestrateur, en le disant clairement: une seule voix qui applique les trois grilles vaut moins que trois lectures indépendantes, l'utilisateur doit le savoir. En cas de limite de débit, exécute les relecteurs en séquentiel plutôt que d'en supprimer un.

## Entrées attendues
1. **Le texte de la pastille**, dans sa version à relire, et le **titre retenu**. Si le titre retenu diffère du titre canonique de la série, il faut les deux: le canonique est l'ancre de périmètre, le retenu est ce qui est jugé.
2. **Le prompt image**, s'il existe. Les relecteurs ne voient aucune image: la revue du visuel porte sur le prompt, jamais sur un rendu. S'il n'y a pas de prompt, dis-le au relecteur conformité pour qu'il ne juge pas dans le vide.
3. **Un brief de référence**, qui fait foi pour l'exactitude. C'est la pièce la plus souvent absente, et la plus indispensable: sans lui, la grille exactitude tourne à vide et la revue se réduit à du style. Si l'utilisateur fournit des sources, elles font le brief. Sinon, reconstitue-le par une petite recherche web ciblée, ancrée sur la date du jour (champ currentDate), en priorité sur des sources officielles ou originales, avant de lancer les relecteurs. Si l'utilisateur refuse la recherche, respecte-le mais signale que la grille exactitude en pâtira.
4. **Le périmètre**: la liste "déjà traité ailleurs" et, si disponibles, les textes des pastilles voisines. À défaut, déduis les voisines de la liste des 45 dans la spec.

Ce qui manque se demande, ne s'invente pas. En particulier, ne fabrique jamais un chiffre pour donner une référence à la grille exactitude.

## Processus

### 1. Réunir le dossier
Rassemble les quatre entrées ci-dessus. Le contexte n'étant pas hérité par les sous-agents, tout devra tenir dans leur prompt: vérifie que rien ne manque avant de lancer, une relecture sur dossier incomplet coûte trois sous-agents pour rien.

### 2. Lancer les trois relecteurs, en parallèle
Trois sous-agents dans le même tour, un par grille, avec le gabarit de relecteur de la spec. Sois explicite sur le parallélisme: par défaut l'exécution reste séquentielle. Chaque prompt est autonome et complet: titre canonique et titre retenu, texte à relire, bloc prompt image, brief de référence, liste "déjà traité ailleurs" et textes voisins si disponibles, liste des 45 titres, et la grille du relecteur, une seule.

Rappelle à chacun qu'il ne voit pas les images et qu'il ne réécrit pas.

### 3. Consolider
Applique les règles d'arbitrage de la spec, section « Arbitrage des constats »: dédoublonnage, arbitrage des contradictions, garde-fou anti-gonflement, bloquants et recommandés retenus, mineurs écartés ou mentionnés, la spec qui l'emporte sur un relecteur qui la contredit, une seule passe.

Ne relance pas de deuxième tour de revue. Si les constats sont massifs, dis-le plutôt que de boucler.

### 4. Rendre
En mode humain, le rapport: les constats consolidés classés par gravité, chacun localisé avec son correctif, puis un verdict en une phrase (publiable tel quel, corrections mineures, corrections nécessaires), puis les sources du brief si tu l'as reconstitué. Termine en proposant `refine` pour appliquer, sans l'appliquer toi-même.

En mode appelé, la liste consolidée, rendue au processus appelant, sans mise en scène ni verdict séparé.

Dans les deux cas, dis ce que la revue n'a pas pu juger: pas de rendu d'image, brief reconstitué plutôt que d'origine, textes voisins absents. Une revue qui taît ses angles morts se fait passer pour plus complète qu'elle n'est.

## Frontière avec les autres skills
`generate` crée la pastille, `refine` la retouche, `email` la met en courriel, `review` la juge. La distinction qui compte est l'intention: une modification demandée relève de `refine`, un avis demandé relève de ce skill. « Relis et corrige » est une demande de modification, donc `refine`, qui déclenchera cette revue si elle est utile. « Qu'est-ce qui cloche dans cette pastille » est une demande d'avis, donc ce skill, qui ne touchera à rien.
