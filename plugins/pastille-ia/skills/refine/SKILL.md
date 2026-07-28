---
description: Réhydrate le dossier d'une pastille LLM venue d'ailleurs, puis lui applique la retouche demandée. À n'utiliser QUE si le contexte de production est perdu: l'utilisateur recolle le texte d'une pastille écrite dans une autre conversation ou session, et il n'y a en contexte ni brief, ni sources, ni périmètre, ni prompt image. Ce skill reconstitue ce dossier manquant, puis applique un diff minimal fidèle. N'utilise PAS ce skill quand la pastille est déjà dans la conversation courante (produite, retouchée ou travaillée ici): son dossier est intact, la retouche s'applique alors directement dans le fil, sans skill, selon la section « Retouche d'une pastille » de la spec partagée. Les mots de la demande ne déclenchent rien: retoucher, corriger, reformuler, raccourcir, retitrer se disent pareil dans les deux cas, seule l'absence de contexte déclenche ce skill. Pour créer une pastille depuis un titre, generate.
---

# Réhydratation puis retouche d'une pastille (Claude Code)

## Quand ce skill sert, et quand il ne sert pas
Ce skill ne sert qu'à un cas: **la pastille existe, mais son dossier de production a disparu**. L'utilisateur recolle un texte produit ailleurs (autre conversation, session antérieure, courriel déjà diffusé) et demande une modification. Il n'y a en contexte ni brief de recherche, ni sources, ni périmètre, ni prompt image. Le travail utile est alors la réhydratation: reconstituer ce dossier avant de toucher au texte.

Il ne sert pas à retoucher une pastille dont le dossier est déjà là. Si la pastille a été produite, retouchée ou déjà travaillée dans la conversation courante, tu as le texte, les deux titres, le brief, les sources, le périmètre et le prompt image: il n'y a rien à réhydrater, et la retouche s'applique directement dans le fil, sans invoquer de skill.

Le test qui décide, ses cas limites et les règles de retouche communes aux deux situations vivent dans la spec partagée, section « Retouche d'une pastille ». C'est la référence: applique-la, ne la réinvente pas ici.

Ce qu'il faut retenir de la frontière:
- La demande de l'utilisateur ne dit rien du bon chemin. « corrige ce paragraphe » se formule à l'identique avec ou sans contexte.
- Le déclencheur est l'absence de dossier, jamais l'intention de modifier.
- Un texte recollé qui avait été produit plus haut dans la même conversation n'est pas un contexte perdu.

### Sortie anticipée
Si tu arrives ici (typiquement parce que l'utilisateur a tapé `/refine`) alors que le dossier de la pastille est présent dans la conversation, ne déroule pas le processus. Dis-le en une ligne, du genre: « Le contexte de la pastille est déjà là, je retouche directement sans repasser par une réhydratation. » Puis applique la retouche selon la spec partagée, section « Retouche d'une pastille » (lis quand même le fichier, il porte les règles du diff minimal et la re-synchronisation du prompt image). Surtout, ne redemande pas des artefacts que tu as déjà et ne reconstitue pas un brief par recherche quand le vrai brief est en contexte: un brief reconstitué est moins fiable que celui d'origine.

Frontière avec les autres skills: `generate` crée une pastille à partir d'un titre (recherche, cinq brouillons, fusion, revue). `review` juge sans rien modifier. `email` met en courriel. Si l'utilisateur n'a pas de texte existant et veut une nouvelle pastille, bascule sur `generate`.

Après une retouche, si la pastille a déjà été mise en courriel, le skill `email` régénère le `.msg` sans rien relancer d'autre.

## Spec partagée (à lire en premier)
Les normes de la série vivent dans un fichier partagé, source unique commune à ce skill et aux skills `generate`, `review` et `email`: liste des 45 pastilles et périmètre, Règles du texte, Règles du titre, Règles d'écriture pour la pastille finale, spec du prompt image et gabarits, charte graphique, doctrine de retouche, boite à outils de revue. Lis-le avant de commencer:

`${CLAUDE_SKILL_DIR}/references/regles-pastille.md` (c'est le fichier `references/regles-pastille.md` situé dans le dossier de ce skill).

Toute retouche que tu appliques doit rester conforme à ces normes. Ne recopie pas ces règles ici: si elles doivent évoluer, modifie la spec partagée.

## Environnement
Le coeur du skill (édition et, au besoin, recherche web ciblée) ne requiert pas de sous-agents et fonctionne partout. Seule la revue critique optionnelle en lance trois, et elle est déléguée au skill `review`, qui gère aussi ses replis quand les sous-agents ne sont pas disponibles.

## Entrées
L'entrée type est soit le texte seul, soit le texte plus le prompt image, recollés par l'utilisateur.

Requis pour travailler:
- La demande de retouche: quoi changer, et si possible pourquoi.
- Le texte actuel de la pastille. C'est l'objet même du raffinement: sans lui, il n'y a rien à raffiner.

Utiles (demande-les quand ils comptent, voir « Si des entrées manquent »):
- Le titre retenu actuel (celui affiché sur la pastille et rendu dans l'image).
- Le titre canonique de la série, s'il diffère du titre retenu (ancre de périmètre).
- Le prompt image actuel (le bloc collé dans Gemini), si l'utilisateur l'a.
- La section Sources d'origine, si elle existe: elle remplace en partie le brief de recherche perdu avec la conversation.

Dans le cas texte plus prompt image, le prompt que tu produis en sortie doit rester cohérent avec celui fourni (voir Étape 4): on part du sien, on n'y touche qu'au strict nécessaire.

### Si des entrées manquent
- Seul le titre est fourni, pas de texte: ne raffine rien et n'invente aucun texte. Demande explicitement le texte actuel de la pastille avant de continuer. Si en réalité aucune pastille n'existe encore (rien à raffiner, l'utilisateur veut la créer de zéro), c'est le skill `generate` qu'il faut utiliser: signale-le et bascule.
- Seul le texte est fourni, pas de titre: distingue les deux titres, car ils n'ont pas le même enjeu.
  - Titre canonique (ancre de périmètre): infère-le en rapprochant le texte de la liste des 45 (spec partagée). C'est un jugement de périmètre, sans risque de rendu; ne demande confirmation que si la retouche risque de déplacer le sujet.
  - Titre retenu (la chaine exacte affichée et rendue dans l'image): ne le reconstruis pas en douce. Propose le libellé le plus probable et demande à l'utilisateur de le confirmer ou de coller l'exact. Exige l'exact avant de l'écrire dans un prompt image, et dès que la retouche touche au titre: à cet endroit le titre est reproduit au caractère près, une reconstruction approximative désynchroniserait l'image du vrai visuel. Pour une simple retouche de texte qui ne touche ni au titre ni à l'image, un libellé proposé et validé suffit; ne bloque pas.

## Étape 1, réhydratation du contexte
Reconstitue le cadre à partir de la spec partagée et des entrées:
- Situe la pastille dans la liste des 45 (spec partagée). Si le titre canonique n'est pas fourni, déduis la pastille de la série la plus proche et prends-la comme ancre de périmètre; ne demande confirmation que si la retouche risque de déplacer le sujet.
- Repère les 1 à 3 pastilles voisines et la liste "déjà traité ailleurs, à ne pas ré-expliquer". Demande les textes voisins seulement si la retouche touche à la frontière entre pastilles.
- Note le titre retenu, le titre canonique, le texte, le prompt image (si fourni) et les sources (si fournies). Ce sont tes artefacts de départ.

## Étape 2, reconstituer la base factuelle (le brief)
Le brief de recherche d'origine est perdu avec la conversation. Or il ne sert pas qu'à valider un chiffre isolé: il ancre la justesse de toute la pastille, il guide la qualité de n'importe quel ajustement (même stylistique: on reformule mieux en sachant précisément de quoi on parle), et il est indispensable à la revue (la grille "exactitude" n'a aucune référence sans lui et tourne à vide). Donc on ne raffine pas à l'aveugle: tu dois disposer d'un brief avant de toucher au texte.

- Sources fournies par l'utilisateur: elles tiennent lieu de brief. Appuie-toi dessus. Ne relance une recherche que si elles ne couvrent pas le point touché, ou si une donnée est mouvante et risque d'être périmée (coûts, empreinte, modèles, réglementation).
- Sources manquantes ou insuffisantes: relance une recherche web ciblée pour reconstituer un brief compact (faits clés, chiffres utiles, 2 à 4 sources), ancrée sur la date du jour (champ currentDate), en priorité sur des sources officielles ou originales. Fais-le dès que les sources manquent, sans attendre que la retouche porte explicitement sur un fait: le brief sécurise la reformulation et rend la revue exploitable. Garde la recherche proportionnée (une petite passe suffit pour une simple retouche), mais ne l'escamote pas.

Cette étape est le coeur du skill, et la raison pour laquelle il n'a pas de sens quand le contexte est intact: reconstituer un brief que l'on a déjà, c'est le remplacer par une approximation.

Seule exception: si l'utilisateur demande explicitement de ne pas rechercher, respecte-le, mais signale que la justesse et la revue en pâtiront. Dans tous les cas, n'invente jamais un chiffre: si tu ne peux vérifier ni par une source fournie ni par une recherche, dis-le et demande la donnée à l'utilisateur plutôt que d'affirmer.

## Étape 3, appliquer le diff minimal
Applique les règles de la spec partagée, section « Retouche d'une pastille », sous-section « Règles du diff minimal »: ne changer que ce qui est demandé et ce qui en découle, une seule voix, conformité aux normes de la série, et vérification des contraintes de comptage que la retouche déplace (taille des paragraphes, place de l'enjeu, longueur des puces, emphases).

## Étape 4, re-synchronisation du prompt image (diff minimal)
Applique la sous-section « Re-synchronisation du prompt image » de la même section de la spec partagée. Rappel du cas propre à ce skill: quand l'utilisateur a fourni un prompt image, pars de CE prompt et n'y applique que le plus petit changement nécessaire; s'il n'en a pas fourni, n'en fabrique pas sans demande explicite.

## Étape 5, revue critique (déléguée au skill `review`, proposée et non imposée)
Ne déclenche pas de revue d'office. Propose-la, et ne la déclenche qu'avec l'accord de l'utilisateur (elle coûte trois sous-agents).

Si l'utilisateur accepte: invoque le skill `review` via l'outil Skill, et passe-lui le dossier complet, à savoir le titre canonique et le titre retenu, le texte raffiné, le bloc prompt image (ou la mention "inchangé", ou son absence), le brief de référence (les Sources fournies ou le brief reconstitué à l'étape 2, et signale-le s'il manque vraiment), la liste "déjà traité ailleurs" et les textes voisins si disponibles. Précise que tu l'appelles depuis `refine`: dans ce mode, il rend la liste consolidée des constats et n'affiche pas de rapport.

Puis applique: la revue rend des constats déjà dédoublonnés et arbitrés selon la spec partagée, section « Arbitrage des constats ». Réécris en une seule voix, une seule passe, sans boucler. Si un constat contredit une norme de la spec, écarte-le en le disant.

## Format de sortie
Ce format vaut pour le cas de ce skill, le contexte perdu: l'utilisateur n'a rien d'autre sous les yeux que ce que tu affiches, donc le livrable est complet. (Pour une retouche menée dans le fil avec le contexte intact, la sortie est réduite à ce qui change, voir la spec partagée.)

N'affiche que le livrable, dans cet ordre:
- Si une revue a eu lieu: un court résumé "Ce que la revue a corrigé" (2 à 4 lignes), avant le reste. Sinon, pas de résumé.
- Le titre retenu, en tête. S'il diffère du titre canonique de la série, ajoute juste en dessous une ligne discrète, par exemple: Titre canonique de la série: "...". Dites-moi si vous préférez le conserver, je reviens dessus en un mot.
- L'encadré "L'essentiel", puis le texte raffiné, puis le bloc annexe s'il y en a un. Si la pastille fournie n'en comportait pas, rédige-les: ils sont désormais requis par la spec.
- Le prompt image seulement s'il a changé: un bloc de code intitulé "Prompt images (à coller dans Gemini)", prêt à copier, suivi d'une ligne qui dit ce que cela implique: les visuels déjà diffusés sont périmés et doivent être régénérés avant toute nouvelle diffusion, l'illustration portant un titre qui n'est plus le titre retenu. S'il n'a pas changé, écris une seule ligne: "Prompt images: inchangé (la retouche n'affecte pas le rendu), les visuels existants restent valables." S'il n'y a pas de prompt image et que rien n'en impose un, n'en parle pas.
- Une section "Sources" listant les références du brief effectivement mobilisé, qu'il vienne des Sources fournies par l'utilisateur ou d'une recherche relancée (2 à 4, de préférence officielles). À omettre seulement si, exceptionnellement, aucune source n'a été mobilisée.

Termine toujours par cette question exacte:
"Comment trouvez-vous le titre, le texte, l'image titre et le diagramme (si généré) ? Si une partie vous semble trop complexe, ou si vous souhaitez affiner le focus d'un visuel pour qu'il soit encore plus épuré, n'hésitez pas à me le faire savoir, et je l'ajusterai."

Les retouches suivantes, elles, se font dans le fil: à partir de maintenant le dossier est en contexte, donc plus aucune réhydratation et plus aucun appel à ce skill.
