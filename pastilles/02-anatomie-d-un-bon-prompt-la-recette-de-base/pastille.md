# Anatomie d'un bon prompt : la recette de base

**Bandeau** : 2 / 45 · PASTILLE IA · Prompting · 2 min de lecture

## L'essentiel
- Un bon prompt tient sur quatre ingrédients : rôle, contexte, tâche et contraintes.
- Sans ces repères, l'IA devine et livre une réponse générique ou à côté du sujet.
- Ce cadrage initial évite les allers-retours et fait gagner du temps dès la première réponse.

## Texte

Quand vous échangez avec une intelligence artificielle, vous lui envoyez des messages sous forme de questions, de consignes ou de demandes : c'est ce qu'on appelle le **prompt**. *C'est le point de départ de votre discussion*. L'erreur la plus courante est de penser que l'IA est capable de deviner vos intentions magiquement. Si vous lui jetez un laconique « rédige un message », le résultat sera souvent tiède, trop long ou à côté de la plaque, car la machine manque cruellement de repères.

Pour obtenir une réponse idéale du premier coup, il existe une structure de base incontournable, une sorte de recette en quatre ingrédients. Le premier est le **rôle** : vous demandez à l'IA de se glisser dans la peau d'un personnage (par exemple, un conseiller client ou un relecteur pointilleux). Le deuxième est le **contexte** : vous lui expliquez la situation (le profil du destinataire, le projet concerné). Le troisième est la **tâche**, c'est-à-dire l'action précise à réaliser. Enfin, le quatrième ingrédient regroupe vos **contraintes**, comme le ton à employer ou le format visuel attendu.

**[SCHEMA ICI : image-schema.png]**

En adoptant ce réflexe, vous transformez un outil généraliste en un assistant sur mesure pour votre quotidien. Vous n'avez plus besoin de passer de longues minutes à faire des allers-retours ou à corriger un texte qui ne vous convient pas. Prendre le temps de bien composer sa demande initiale est le moyen le plus simple et le plus rapide de gagner en efficacité et de faire de l'IA un véritable allié de travail.

## Bloc annexe : A ESSAYER
Copiez ce squelette et remplissez les quatre blancs avant d'envoyer votre prochain prompt : "Tu es [rôle]. Contexte : [situation, destinataire]. Tâche : [action précise]. Contraintes : [ton, longueur, format]."

## Textes alternatifs et légende
- **image-titre (alt)** : Anatomie d'un bon prompt : la recette de base
- **image-schema (alt)** : Schéma en quatre étapes menant à une réponse précise : 1. Le rôle (Qui parle ? ex: Expert, Critique), 2. Le contexte (De quoi s'agit-il ? Sujet, Public), 3. La tâche (Qu'attend-on ? Action précise), 4. Les contraintes (Comment le veut-on ? Ton, Format).
- **Légende sous le schéma** : Les quatre ingrédients du prompt, du rôle à la réponse précise qu'ils permettent d'obtenir.

## Prompt image (à coller dans Gemini)

```
Prépares-toi à générer deux images séparées, dans deux fichiers distincts. Les deux partagent cette charte graphique : Style propre, moderne et professionnel, fond blanc. Palette : orange vif et bleu corporate foncé en dominantes, blanc et gris pour les respirations, accents multiculturels discrets (rouge, vert, jaune, bleu) reprenant subtilement un motif de couleurs de logo. Superpositions graphiques épurées : motifs géométriques abstraits, quartiers de cercle, lignes claires. Composition aérée, jamais surchargée. Typographie sans serif, propre et corporate. Tout texte affiché dans les images est en français.
Contexte pour comprendre le sujet, à NE PAS afficher dans les images : Quand vous échangez avec une intelligence artificielle, vous lui envoyez des messages sous forme de questions, de consignes ou de demandes : c'est ce qu'on appelle le prompt. C'est le point de départ de votre discussion. L'erreur la plus courante est de penser que l'IA est capable de deviner vos intentions magiquement. Si vous lui jetez un laconique « rédige un message », le résultat sera souvent tiède, trop long ou à côté de la plaque, car la machine manque cruellement de repères. Pour obtenir une réponse idéale du premier coup, il existe une structure de base incontournable, une sorte de recette en quatre ingrédients. Le premier est le rôle : vous demandez à l'IA de se glisser dans la peau d'un personnage (par exemple, un conseiller client ou un relecteur pointilleux). Le deuxième est le contexte : vous lui expliquez la situation (le profil du destinataire, le projet concerné). Le troisième est la tâche, c'est-à-dire l'action précise à réaliser. Enfin, le quatrième ingrédient regroupe vos contraintes, comme le ton à employer ou le format visuel attendu. En adoptant ce réflexe, vous transformez un outil généraliste en un assistant sur mesure pour votre quotidien. Vous n'avez plus besoin de passer de longues minutes à faire des allers-retours ou à corriger un texte qui ne vous convient pas. Prendre le temps de bien composer sa demande initiale est le moyen le plus simple et le plus rapide de gagner en efficacité et de faire de l'IA un véritable allié de travail.
Image 1, illustration-titre : composition épurée et moderne, focus graphique central iconique qui illustre le sujet : un personnage qui compose une recette (livre de recette, ustensiles, ingrédients graphiques stylisés) en écho à l'idée de "recette de base" du prompt. Ce n'est pas un schéma de processus. Seul texte à afficher : le titre, en en-tête, sans faute d'orthographe, police sans serif corporate, sans sous-titre ni texte secondaire. Le titre exact : "Anatomie d'un bon prompt : la recette de base". Format 16:9.
Image 2, schéma explicatif, distincte et cohérente avec l'image 1 : diagramme d'entreprise propre et net de type processus, présentant quatre étapes qui s'enchaînent de gauche à droite jusqu'à un résultat final. Libellés exacts à afficher en français : "1. Le rôle : Qui parle ? (ex: Expert, Critique)", "2. Le contexte : De quoi s'agit-il ? (Sujet, Public)", "3. La tâche : Qu'attend-on ? (Action précise)", "4. Les contraintes : Comment le veut-on ? (Ton, Format)", puis un bloc final "Réponse précise". Très peu de fioritures, focus sur la clarté, n'inclus pas le titre. Format 4:3, cinq blocs au maximum, libellés assez grands pour rester lisibles une fois l'image réduite à 560 pixels de large.
Génère dans un premier temps seulement la première image (l'illustration-titre), et attends les instructions de l'utilisateur pour générer la 2e image.
```

## Sources
- [Prompt engineering, "Be clear and direct" (Claude Docs, Anthropic)](https://docs.anthropic.com/en/docs/be-clear-direct) : recommande d'assigner un rôle/persona à l'IA et de fournir explicitement le contexte de la tâche, faute de quoi le modèle "devine" comme un nouvel employé sans repères.
- [Best practices for prompt engineering with the OpenAI API (OpenAI Help Center)](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api) : confirme qu'un prompt clair doit préciser le contexte, la tâche, le format et le ton attendus pour éviter une réponse générique ou hors sujet.
- [Prompt design strategies (Gemini API, Google AI for Developers)](https://ai.google.dev/gemini-api/docs/prompting-strategies) : détaille le cadre Persona / Tâche / Contexte / Format (PTCF), qui recoupe directement les quatre ingrédients (rôle, contexte, tâche, contraintes) de la pastille.

## Points de vigilance
- Aucun chiffre ni date à vérifier dans le texte gelé : la pastille décrit une structure conceptuelle (rôle, contexte, tâche, contraintes), que les trois sources ci-dessus corroborent sous des intitulés proches (rôle/persona, contexte, tâche, format/ton). Rien à corriger.
- Titre de l'image identique au titre canonique et au sujet du courriel d'origine : aucun écart à signaler.
- Format d'origine des images (512x279, ratio proche de 16:9 mais pas un schéma en 4:3 strict pour image-2) : le prompt image régénéré redemande un format 4:3 conforme au gabarit actuel, ce qui donnera un schéma légèrement différent en proportions de l'original, mais fidèle à ses libellés et à sa logique.

## Fichiers écrits
- `pastilles/02-anatomie-d-un-bon-prompt-la-recette-de-base/pastille.html`
- `pastilles/02-anatomie-d-un-bon-prompt-la-recette-de-base/image-titre.png`
- `pastilles/02-anatomie-d-un-bon-prompt-la-recette-de-base/image-schema.png`
- `pastilles/02-anatomie-d-un-bon-prompt-la-recette-de-base/meta.json`
- `pastilles/02-anatomie-d-un-bon-prompt-la-recette-de-base/pastille.md`
- `pastilles/02-anatomie-d-un-bon-prompt-la-recette-de-base/pastille.eml`
