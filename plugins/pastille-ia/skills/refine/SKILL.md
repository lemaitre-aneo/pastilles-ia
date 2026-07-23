---
description: Raffine (itérativement) une pastille LLM déjà rédigée quand la conversation d'origine n'est plus disponible. L'utilisateur fournit le texte de la pastille (et selon le cas son titre, son prompt image, ses sources) plus la retouche voulue; ce skill réhydrate le contexte à partir des normes de la série et applique un diff minimal fidèle, sans relancer la génération complète (pas de fan-out à cinq brouillons). Utilise ce skill dès qu'on te demande de retoucher, ajuster, corriger, reformuler, raccourcir, allonger, retitrer, changer le ton ou faire évoluer une pastille existante déjà écrite, que le mot "pastille" soit employé ou non, dès lors qu'un texte de pastille est fourni avec une demande de modification. Pour créer une pastille à partir d'un simple titre (sans texte existant), utilise plutôt le skill generate.
---

# Raffineur de pastilles LLM (Claude Code)

## Ce que fait ce skill
Fait évoluer une pastille déjà produite, à partir des artefacts que l'utilisateur recolle (au minimum le texte), sans repasser par la génération complète. Il réhydrate le contexte à partir des normes de la série, classe la retouche demandée, applique un diff minimal en une seule voix, re-synchronise le prompt image au strict nécessaire, et propose (sans l'imposer) la revue critique à trois relecteurs.

Frontière avec `generate`: `generate` crée une pastille à partir d'un titre (recherche, cinq brouillons, fusion, revue). `refine` part d'une pastille existante fournie et ne fait que la retoucher. Si l'utilisateur n'a pas de texte existant et veut une nouvelle pastille, bascule sur `generate`.

## Spec partagée (à lire en premier)
Les normes de la série vivent dans un fichier partagé, source unique commune à ce skill et au skill `generate`: liste des 45 pastilles et périmètre, Règles du texte, Règles du titre, Règles d'écriture pour la pastille finale, spec du prompt image et gabarits, charte graphique, boite à outils de revue. Lis-le avant de commencer:

`${CLAUDE_SKILL_DIR}/references/regles-pastille.md` (c'est le fichier `references/regles-pastille.md` situé dans le dossier de ce skill).

Toute retouche que tu appliques doit rester conforme à ces normes. Ne recopie pas ces règles ici: si elles doivent évoluer, modifie la spec partagée.

## Environnement
Le coeur du skill (édition et, au besoin, recherche web ciblée) ne requiert pas de sous-agents et fonctionne partout. Seule la revue critique optionnelle lance trois sous-agents (outil Task); si les sous-agents ne sont pas disponibles, propose une relecture globale unique par l'orchestrateur à la place.

## Entrées
L'entrée type est soit le texte seul, soit le texte plus le prompt image.

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

## Étape 2, classer la retouche
- Retouche éditoriale, stylistique ou structurelle (ton, longueur, rythme, emphases, clarté, reformulation, changement de titre à périmètre constant): aucune recherche. N'introduis aucun fait nouveau.
- Retouche factuelle (ajout ou modification d'un chiffre, d'une date, d'un fait, ou demande d'actualiser une donnée): il lui faut une base factuelle fiable, et le brief d'origine est perdu avec la conversation.
  - Si l'utilisateur a fourni les Sources d'origine et qu'elles couvrent le point touché, appuie-toi dessus. Ne relance une recherche que si elles ne couvrent pas ce point, ou si la donnée est mouvante et risque d'être périmée (coûts, empreinte, modèles, réglementation).
  - Sinon (pas de sources fournies, ou sources insuffisantes pour le point touché): relance une petite recherche web ciblée, ancrée sur la date du jour (champ currentDate), en priorité sur des sources officielles ou originales, juste assez pour sécuriser le point. C'est le cas clé: une retouche factuelle sans source disponible impose de refaire la recherche, jamais d'affirmer de mémoire.
  - Dans tous les cas, n'invente jamais un chiffre. Si tu ne peux vérifier ni par une source fournie ni par une recherche, dis-le et demande la donnée à l'utilisateur plutôt que d'affirmer.
En cas de doute sur la catégorie, traite la retouche comme factuelle.

## Étape 3, appliquer le diff minimal
- Applique uniquement ce qui est demandé et ce qui en découle nécessairement. Préserve tout le reste: n'en profite pas pour réécrire des passages non concernés.
- Réécris en une seule voix cohérente, sans effet patchwork à la jointure de la retouche.
- Respecte toutes les normes de la spec partagée (Règles du texte, Règles du titre, Règles d'écriture pour la pastille finale), y compris les contraintes dures: français, pas de tiret cadratin ni caractère non standard, aucun nom d'entreprise ni ANEO, prose sans listes.
- Titre: si la retouche implique le titre, applique les Règles du titre; garde le périmètre ancré sur le canonique. Sinon, laisse le titre retenu tel quel.

## Étape 4, re-synchronisation du prompt image (diff minimal)
Principe directeur: ne régénère jamais le prompt image gratuitement. Si la retouche ne change pas ce que les images doivent montrer, le prompt image reste inchangé.

- Prompt image non fourni: n'en fabrique pas, sauf demande explicite. Si la retouche modifie le titre retenu ou le concept illustré, signale à l'utilisateur que son prompt image (s'il en a un ailleurs) devra être mis à jour, et propose de le régénérer selon la spec partagée.
- Prompt image fourni: pars de CE prompt et applique le plus petit changement nécessaire.
  - Titre retenu modifié: remplace le titre exact (la ligne du type `Le titre exact: "..."`) au caractère près, et rien d'autre.
  - Concept central déplacé par la retouche (l'illustration-titre ou le schéma ne colle plus au texte): ajuste la description de l'illustration (et/ou du schéma) en conservant la charte, le style et la structure du prompt fourni. Diff minimal, pas de réécriture complète.
  - Besoin de schéma modifié par la retouche (le texte devient, ou cesse d'être, un vrai processus, flux ou comparaison): ajoute ou retire la seconde image en conséquence, selon les gabarits de la spec partagée.
  - Ni le titre rendu ni le concept illustré ne changent: laisse le prompt image entièrement inchangé. Le contexte caché "à ne pas afficher" n'affecte pas le rendu; ne le rafraîchis que si l'utilisateur le demande.

## Étape 5, revue critique (proposée, non imposée)
Ne relance pas de revue d'office. Propose-la, et ne la lance qu'avec l'accord de l'utilisateur (elle coûte trois sous-agents).

Si l'utilisateur accepte: applique la boite à outils de revue de la spec partagée (principe des constats, périmètre de jugement, les trois grilles, gabarit de relecteur). Lance trois sous-agents en parallèle (parallélisme explicite, sinon exécution séquentielle), un par grille, chaque prompt autonome et complet: titre canonique et titre retenu, texte raffiné, bloc prompt image (ou mention "inchangé"), brief de référence (les Sources fournies, ou le brief de la recherche ciblée si tu en as lancé une, sinon signale son absence au relecteur), liste "déjà traité ailleurs" et textes voisins si disponibles, et la liste des 45 titres. Puis, en orchestrateur: rassemble et dédoublonne les constats, arbitre les contradictions, garde-fou anti-gonflement (à conseil équivalent, la concision l'emporte sauf erreur de fond), applique bloquants et recommandés, écarte ou mentionne les mineurs, réécris en une seule voix. Une seule passe, pas de boucle.

En l'absence de sous-agents, propose une relecture globale unique par l'orchestrateur contre les trois grilles.

## Format de sortie
N'affiche que le livrable, dans cet ordre:
- Si une revue a eu lieu: un court résumé "Ce que la revue a corrigé" (2 à 4 lignes), avant le reste. Sinon, pas de résumé.
- Le titre retenu, en tête. S'il diffère du titre canonique de la série, ajoute juste en dessous une ligne discrète, par exemple: Titre canonique de la série: "...". Dites-moi si vous préférez le conserver, je reviens dessus en un mot.
- Le texte raffiné.
- Le prompt image seulement s'il a changé: un bloc de code intitulé "Prompt images (à coller dans Gemini)", prêt à copier. S'il n'a pas changé, écris une seule ligne: "Prompt images: inchangé (la retouche n'affecte pas le rendu)." S'il n'y a pas de prompt image et que rien n'en impose un, n'en parle pas.
- Une section "Sources" si la retouche a touché aux faits: les références effectivement utilisées pour vérifier ou ajouter la donnée, qu'elles viennent d'une recherche relancée ou des Sources fournies par l'utilisateur (2 à 4, de préférence officielles). Inutile pour une retouche purement éditoriale.

Termine toujours par cette question exacte:
"Comment trouvez-vous le titre, le texte, l'image titre et le diagramme (si généré) ? Si une partie vous semble trop complexe, ou si vous souhaitez affiner le focus d'un visuel pour qu'il soit encore plus épuré, n'hésitez pas à me le faire savoir, et je l'ajusterai."
