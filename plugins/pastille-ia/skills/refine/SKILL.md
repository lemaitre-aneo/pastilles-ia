---
description: Reprend une pastille LLM produite ailleurs, quand le contexte de la conversation d'origine est perdu. Entrée de référence: le fichier HTML de la pastille, qui porte son dossier complet en commentaire (texte, titre canonique, axe, prompt d'images, sources, notes) et ses visuels incorporés; le skill le relit avec dossier.py et n'a alors rien à reconstituer. À défaut d'artefact, il travaille sur le texte recollé et reconstitue ce qui manque. N'utilise PAS ce skill quand la pastille est déjà dans la conversation courante: son dossier est intact, la retouche s'applique directement dans le fil, sans skill, selon la section « Faire évoluer une pastille » de la spec partagée. Ne l'utilise pas non plus quand il faut du matériau neuf sur toute la pastille, un changement d'axe: cela se régénère avec generate.
---

# Reprise d'une pastille (Claude Code)

## Quand ce skill sert, et quand il ne sert pas
Ce skill ne sert qu'à un cas: **la pastille existe, mais le contexte de sa production a disparu**. Autre conversation, session antérieure, courriel déjà diffusé. Le travail utile est de retrouver son dossier avant de toucher au texte.

Il ne sert pas à retoucher une pastille dont le dossier est déjà dans la conversation courante: il n'y aurait rien à retrouver, et la retouche s'applique directement dans le fil, sans invoquer de skill. Il ne sert pas non plus quand la demande réclame du matériau neuf sur toute la pastille, un changement d'axe: cela se régénère avec `generate`. Entre les deux, le réagencement et la reprise d'un morceau délimité restent à ta portée.

Le test qui décide, ses cas limites et les règles communes vivent dans la spec partagée, section « Faire évoluer une pastille ». C'est la référence: applique-la, ne la réinvente pas ici.

## Deux entrées possibles, et elles ne demandent pas le même travail

### Avec l'artefact HTML: rien à reconstituer
Depuis que le skill `email` incorpore un dossier dans le fichier HTML de la pastille, **ce fichier est l'entrée de référence**. Il porte tout: le texte, le titre retenu et le titre canonique, l'axe, le prompt d'images et l'aperçu des visuels, les sources, les notes d'échange, et les deux visuels en base64. Demande-le une fois, en ouverture: « avez-vous le fichier HTML de la pastille ? » vaut mieux que dix questions de reconstitution. Si la réponse est non, n'insiste pas et prends l'autre chemin, qui reste entier.

```
python3 ${CLAUDE_SKILL_DIR}/../email/scripts/dossier.py "pastille NN accroche.html" --dossier .
```

Le script écrit une `fiche.json` et les deux visuels, prêts pour `build.py`. Sans `--dossier`, il affiche le dossier en JSON, ce qui suffit pour lire un axe ou un prompt d'images.

Ce que cela change, et il faut le mesurer: **pas de recherche pour reconstituer un brief**, les sources d'origine étant là; **pas de titre à deviner ni de prompt image à réinventer**; **pas de visuel à redemander**. Tu passes directement à la retouche, avec le vrai dossier plutôt qu'une approximation. Si des champs manquent (le script les liste), ne demande que ceux-là.

Le formalisme, pour le connaitre sans avoir à le déduire: le dossier est un commentaire HTML `<!--pastille:dossier ... pastille:fin-->` contenant la fiche en JSON, à la fin du corps. Un commentaire, précisément pour qu'aucun rendu ni aucun import ne le fasse apparaitre. Ne le modifie jamais à la main: retouche la fiche, puis refabrique les deux fichiers avec `build.py`, qui réécrit le dossier à partir d'elle. Un dossier édité à la main et un texte affiché qui divergent, c'est une archive qui ment.

### Sans artefact, avec le texte recollé: reconstitution
**Chemin pleinement supporté, et il le restera.** Toutes les pastilles diffusées avant l'introduction du dossier n'ont pas d'artefact, et il n'y a aucune raison de les rendre intraitables: l'artefact est une commodité quand il existe, jamais une condition d'entrée. Ne demande donc pas le fichier HTML deux fois, et ne bloque jamais faute de l'avoir.

L'utilisateur recolle un texte, parfois un prompt d'images, parfois des sources. Il faut alors reconstituer le dossier, et les étapes ci-dessous décrivent ce travail, inchangé. Dis simplement, en une ligne, que le dossier reconstitué sera moins fiable que celui d'origine, et que s'il retrouve le fichier HTML, tout devient plus simple et plus juste.

Au terme d'une reprise sans artefact, produis l'artefact: c'est ce qui évitera la même reconstitution la fois suivante, et c'est ainsi que les anciennes pastilles rejoignent le formalisme, une par une, au fil des reprises.

Cas voisin à traiter pareil: un artefact HTML **antérieur** au dossier, donc sans commentaire à relire. `dossier.py` le dit clairement plutôt que d'échouer obscurément. Le texte affiché dans ce fichier reste exploitable: reprends-le comme un texte recollé.

Ce qu'il faut retenir de la frontière:
- La demande de l'utilisateur ne dit rien du bon chemin. « corrige ce paragraphe » se formule à l'identique avec ou sans contexte.
- Le déclencheur est l'absence de contexte, jamais l'intention de modifier.
- Un texte recollé qui avait été produit plus haut dans la même conversation n'est pas un contexte perdu.
- Ce skill traite les retouches de surface, les réagencements, et la reprise d'un morceau délimité. Ce qui demande du matériau neuf sur toute la pastille se régénère, cela ne se raffine pas.

### Demande structurelle
Avant de raffiner, tranche l'ampleur de la demande selon la spec partagée, section « Faire évoluer une pastille », sous-section « Test de l'ampleur ». Deux questions décident: la demande réclame-t-elle du matériau que le texte fourni ne contient pas, et s'il faut produire, faut-il tout jeter ? Rien à produire: poursuis (retouche ou réagencement, selon ce qui bouge). Un morceau à produire, le reste conservé: poursuis aussi, en reprise ciblée. Toute la pastille à refaire, parce que l'axe change ou que le thème se déplace: ne déroule pas les étapes ci-dessous; dis-le, et propose la régénération par `generate` en disant ce qu'elle implique (six brouillons, une passe de recherche, titre possiblement différent, visuels périmés). Ne régénère pas de ta propre initiative; mais si l'utilisateur a déjà été explicite (« régénère », « reprends de zéro sur ce nouvel axe »), bascule sur `generate` sans redemander de confirmation. Le texte recollé et ses sources ne sont pas perdus pour autant: ils servent de matériau et de point de départ du brief.

### Sortie anticipée
Si tu arrives ici (typiquement parce que l'utilisateur a tapé `/refine`) alors que le dossier de la pastille est présent dans la conversation, ne déroule pas le processus. Dis-le en une ligne, du genre: « Le contexte de la pastille est déjà là, je retouche directement sans repasser par une réhydratation. » Puis applique la retouche selon la spec partagée, section « Faire évoluer une pastille » (lis quand même le fichier, il porte les règles du diff minimal et la re-synchronisation du prompt image). Surtout, ne redemande pas des artefacts que tu as déjà et ne reconstitue pas un brief par recherche quand le vrai brief est en contexte: un brief reconstitué est moins fiable que celui d'origine.

Frontière avec les autres skills: `generate` crée une pastille à partir d'un titre (recherche, six brouillons, fusion pondérée, revue). `review` juge sans rien modifier. `email` met en courriel. Si l'utilisateur n'a pas de texte existant et veut une nouvelle pastille, bascule sur `generate`.

Après une retouche, si la pastille a déjà été mise en courriel, le skill `email` régénère le `.msg` sans rien relancer d'autre.

## Spec partagée (à lire en premier)
Les normes de la série vivent dans un fichier partagé, source unique commune à ce skill et aux skills `generate`, `review` et `email`: liste des 45 pastilles et périmètre, vocabulaire de l'axe et de l'angle avec la bibliothèque d'angles, Règles du texte, Règles du titre, Règles d'écriture pour la pastille finale, spec du prompt image et gabarits, charte graphique, doctrine d'évolution (retoucher, réagencer ou régénérer), boite à outils de revue. Lis-le avant de commencer:

`${CLAUDE_SKILL_DIR}/references/regles-pastille.md` (c'est le fichier `references/regles-pastille.md` situé dans le dossier de ce skill).

Toute retouche que tu appliques doit rester conforme à ces normes. Ne recopie pas ces règles ici: si elles doivent évoluer, modifie la spec partagée.

## Environnement
Le coeur du skill (édition et, au besoin, recherche web ciblée) ne requiert pas de sous-agents et fonctionne partout. Seule la revue critique optionnelle en lance trois, et elle est déléguée au skill `review`, qui gère aussi ses replis quand les sous-agents ne sont pas disponibles.

## Entrées
Deux entrées possibles, et l'ordre de préférence n'est pas négociable:

1. **Le fichier HTML de la pastille**, si l'utilisateur l'a. Il porte le dossier complet et les visuels: c'est tout ce qu'il faut. Demande-le avant toute autre question.
2. **Le texte recollé**, à défaut, avec la demande de retouche. Tout le reste est alors à reconstituer.

Requis dans les deux cas:
- La demande de retouche: quoi changer, et si possible pourquoi.
- Le texte de la pastille, qu'il vienne du dossier ou d'un copier-coller. Sans lui, il n'y a rien à reprendre.

Utiles quand il n'y a pas d'artefact (demande-les quand ils comptent, voir « Si des entrées manquent »):
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

## Étape 1, retrouver le contexte
Avec l'artefact HTML, cette étape se réduit à lire le dossier: le titre canonique, l'axe, le prompt d'images et les sources y sont, et les notes disent souvent pourquoi tel choix a été fait. Vérifie seulement que la pastille est bien celle que l'utilisateur croit, puis passe à l'étape 3.

Sans artefact, reconstitue le cadre à partir de la spec partagée et des entrées:
- Situe la pastille dans la liste des 45 (spec partagée). Si le titre canonique n'est pas fourni, déduis la pastille de la série la plus proche et prends-la comme ancre de périmètre; ne demande confirmation que si la retouche risque de déplacer le sujet.
- Repère les 1 à 3 pastilles voisines et la liste "déjà traité ailleurs, à ne pas ré-expliquer". Demande les textes voisins seulement si la retouche touche à la frontière entre pastilles.
- Note le titre retenu, le titre canonique, le texte, le prompt image (si fourni) et les sources (si fournies). Ce sont tes artefacts de départ.

## Étape 2, reconstituer la base factuelle (le brief)
Étape sans objet quand l'artefact HTML est là: ses sources **sont** le brief d'origine, pas une approximation. Ne relance une recherche que si la retouche touche une donnée mouvante qu'elles ne couvrent pas (coûts, empreinte, modèles, réglementation), et dis-le.

Sans artefact, le brief de recherche d'origine est perdu avec la conversation. Or il ne sert pas qu'à valider un chiffre isolé: il ancre la justesse de toute la pastille, il guide la qualité de n'importe quel ajustement (même stylistique: on reformule mieux en sachant précisément de quoi on parle), et il est indispensable à la revue (la grille "exactitude" n'a aucune référence sans lui et tourne à vide). Donc on ne raffine pas à l'aveugle: tu dois disposer d'un brief avant de toucher au texte.

- Sources fournies par l'utilisateur: elles tiennent lieu de brief. Appuie-toi dessus. Ne relance une recherche que si elles ne couvrent pas le point touché, ou si une donnée est mouvante et risque d'être périmée (coûts, empreinte, modèles, réglementation).
- Sources manquantes ou insuffisantes: relance une recherche web ciblée pour reconstituer un brief compact (faits clés, chiffres utiles, 2 à 4 sources), ancrée sur la date du jour (champ currentDate), en priorité sur des sources officielles ou originales. Fais-le dès que les sources manquent, sans attendre que la retouche porte explicitement sur un fait: le brief sécurise la reformulation et rend la revue exploitable. Garde la recherche proportionnée (une petite passe suffit pour une simple retouche), mais ne l'escamote pas.

Reconstituer un brief que l'on a déjà, sous une forme ou une autre, c'est le remplacer par une approximation: c'est pourquoi cette étape tombe dès que le dossier est disponible, en contexte ou dans l'artefact.

Seule exception: si l'utilisateur demande explicitement de ne pas rechercher, respecte-le, mais signale que la justesse et la revue en pâtiront. Dans tous les cas, n'invente jamais un chiffre: si tu ne peux vérifier ni par une source fournie ni par une recherche, dis-le et demande la donnée à l'utilisateur plutôt que d'affirmer.

Si le brief reconstitué révèle que le problème n'est pas la formulation mais l'angle même de la pastille (le texte explique mal ce que les sources disent, l'axe ne tient pas), dis-le et propose la régénération plutôt que d'enchainer des retouches: à ce stade tu as le titre canonique, le périmètre et un brief, c'est-à-dire tout ce dont `generate` a besoin.

## Étape 3, appliquer le diff minimal
Applique les règles de la spec partagée, section « Faire évoluer une pastille », sous-section « Règles du diff minimal »: ne changer que ce qui est demandé et ce qui en découle, une seule voix, conformité aux normes de la série, et vérification des contraintes de comptage que la retouche déplace (taille des paragraphes, place de l'enjeu, longueur des puces, emphases).

## Étape 4, re-synchronisation du prompt image (diff minimal)
Applique la sous-section « Re-synchronisation du prompt image » de la même section de la spec partagée. Rappel du cas propre à ce skill: quand l'utilisateur a fourni un prompt image, pars de CE prompt et n'y applique que le plus petit changement nécessaire; s'il n'en a pas fourni, n'en fabrique pas sans demande explicite.

Deux points propres à une reprise, puisque les pastilles antérieures n'ont pas d'aperçu des visuels:
- **Rédige l'aperçu à partir du prompt fourni**, même si la retouche ne touche pas aux images. Il se déduit du prompt sans rien inventer, il coûte trois lignes, et il donne à l'utilisateur comme à la revue de quoi juger des visuels qu'aucun de vous ne peut regarder. Il part ensuite dans le dossier (champ `apercu_visuels`), donc la reprise suivante n'aura plus à le refaire.
- **Si le prompt bouge, l'aperçu bouge avec lui**, dans le même mouvement: un livrable qui annonce une image et un bloc qui en commande une autre est plus trompeur que pas d'aperçu du tout.

## Étape 5, revue critique (déléguée au skill `review`, proposée et non imposée)
Ne déclenche pas de revue d'office. Propose-la, et ne la déclenche qu'avec l'accord de l'utilisateur (elle coûte trois sous-agents).

Si l'utilisateur accepte: invoque le skill `review` via l'outil Skill, et passe-lui le dossier complet, à savoir le titre canonique et le titre retenu, le texte raffiné, le bloc prompt image (ou la mention "inchangé", ou son absence) et l'aperçu des visuels, le brief de référence (les Sources fournies ou le brief reconstitué à l'étape 2, et signale-le s'il manque vraiment), la liste "déjà traité ailleurs", les textes voisins si disponibles, et les consignes que l'utilisateur a posées en demandant la retouche (ce qu'il voulait, ce qu'il a exclu): un relecteur qui les ignore reproche au texte ce qui vient d'être décidé. Précise que tu l'appelles depuis `refine`: dans ce mode, il rend la liste consolidée des constats et n'affiche pas de rapport.

Puis applique: la revue rend des constats déjà dédoublonnés et arbitrés selon la spec partagée, section « Arbitrage des constats ». Réécris en une seule voix, une seule passe, sans boucler. Si un constat contredit une norme de la spec, écarte-le en le disant.

## Refabriquer les fichiers
Une reprise ne s'arrête pas au texte affiché en conversation. Si tu es parti d'un artefact, ou si la pastille a déjà été diffusée, refabrique les deux fichiers avec le skill `email`: le `.msg` et l'artefact HTML, depuis la fiche retouchée. C'est ce qui garde le dossier, le texte et les visuels d'accord entre eux, et c'est ce qui fera de la prochaine reprise une lecture au lieu d'une reconstitution.

Deux cas à signaler franchement à l'utilisateur au moment de refabriquer:
- **Le prompt d'images a changé**: les visuels du dossier sont périmés, il faut les régénérer dans Gemini avant de refabriquer, sinon l'artefact porterait un texte neuf et une image ancienne.
- **Le titre retenu a changé**: l'illustration affiche l'ancien, et le nom du fichier ne correspond plus à l'accroche. Les deux se règlent, mais pas en silence.

## Format de sortie
Ce format vaut pour le cas de ce skill, le contexte perdu: l'utilisateur n'a rien d'autre sous les yeux que ce que tu affiches, donc le livrable est complet. Quand tu as refabriqué les fichiers, ajoute une ligne disant lesquels et où. (Pour une retouche menée dans le fil avec le contexte intact, la sortie est réduite à ce qui change, voir la spec partagée.)

N'affiche que le livrable, dans cet ordre:
- Si une revue a eu lieu: un court résumé "Ce que la revue a corrigé" (2 à 4 lignes), avant le reste. Sinon, pas de résumé.
- Le titre retenu, en tête. S'il diffère du titre canonique de la série, ajoute juste en dessous une ligne discrète, par exemple: Titre canonique de la série: "...". Dites-moi si vous préférez le conserver, je reviens dessus en un mot.
- L'encadré "L'essentiel", puis le texte raffiné, puis le bloc annexe s'il y en a un. Si la pastille fournie n'en comportait pas, rédige-les: ils sont désormais requis par la spec.
- L'aperçu des visuels, deux courtes descriptions de ce que montrent les deux images (motif central et titre exact rendu pour l'illustration; forme retenue, mécanisme rendu visible, structure, libellés et format pour le schéma). Affiche-le dans les deux cas, prompt changé ou non: c'est ce qui permet à l'utilisateur de vérifier que les visuels qu'il a sous la main correspondent encore au texte retouché, ce que tu ne peux pas constater à sa place.
- Le prompt image seulement s'il a changé: un bloc de code intitulé "Prompt images (à coller dans Gemini)", prêt à copier, suivi d'une ligne qui dit ce que cela implique: les visuels déjà diffusés sont périmés et doivent être régénérés avant toute nouvelle diffusion, l'illustration portant un titre qui n'est plus le titre retenu. S'il n'a pas changé, écris une seule ligne: "Prompt images: inchangé (la retouche n'affecte pas le rendu), les visuels existants restent valables." S'il n'y a pas de prompt image et que rien n'en impose un, n'en parle pas, et n'affiche pas d'aperçu non plus: il n'y a rien dont il serait le reflet.
- Une section "Sources" listant les références du brief effectivement mobilisé, qu'il vienne des Sources fournies par l'utilisateur ou d'une recherche relancée (2 à 4, de préférence officielles). À omettre seulement si, exceptionnellement, aucune source n'a été mobilisée.

Termine toujours par cette question exacte:
"Comment trouvez-vous le titre, le texte, l'image titre et le diagramme (si généré) ? Si une partie vous semble trop complexe, ou si vous souhaitez affiner le focus d'un visuel pour qu'il soit encore plus épuré, n'hésitez pas à me le faire savoir, et je l'ajusterai."

Les retouches suivantes, elles, se font dans le fil: à partir de maintenant le dossier est en contexte, donc plus aucune reprise et plus aucun appel à ce skill.
