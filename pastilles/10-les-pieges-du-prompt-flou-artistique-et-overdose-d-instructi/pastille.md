# Les pièges du prompt : flou artistique et overdose d'instructions

**Bandeau** : 10 / 45 · PASTILLE IA · Prompting · 2 min de lecture

## L'essentiel
- Le flou artistique laisse l'IA deviner votre besoin et broder au hasard.
- L'overdose d'instructions dilue son attention et noie la consigne principale.
- La bonne dose tient en quatre ingrédients : rôle, tâche, contexte, format.

## Texte

Lorsqu'on commence à interagir avec une intelligence artificielle, il est facile de tomber dans l'un des deux pièges opposés du prompt : le **flou artistique** ou l'**overdose d'instructions**.

Dans le premier cas, on se montre trop évasif en demandant par exemple d'*« écrire un rapport sur le marché »*. L'IA, privée de cadre, est alors forcée de deviner vos attentes opérationnelles. Elle comble ce vide en faisant des **choix arbitraires** qui tombent souvent à côté de la plaque.

À l'inverse, par excès de zèle, on a tendance à rédiger de véritables cahiers des charges de trois pages pour une tâche simple. C'est l'overdose. En submergeant le modèle sous une avalanche de micro-consignes de ton, de style, de structure et de mise en forme, on s'expose à un phénomène de **dilution de l'attention**. Mathématiquement, l'IA répartit sa capacité d'analyse sur l'ensemble de votre texte : ***plus vous multipliez les contraintes secondaires, plus vous risquez qu'elle ignore l'instruction principale***.

**[SCHÉMA]** Entre le flou total et la surcharge d'instructions, la zone d'impact tient en quatre repères : rôle clair, tâche principale simple, contexte strictement nécessaire et format attendu.

Pour obtenir un résultat optimal, la solution consiste à viser un **équilibre sobre**. Donnez à l'IA un **rôle clair**, formulez **une seule tâche principale** bien définie, fournissez le **contexte strictement nécessaire**, et précisez le **format attendu**. Si le sujet est vraiment complexe, ne cherchez pas à tout résoudre en un seul prompt : **découpez votre travail** en plusieurs étapes logiques pour éviter les laborieux allers-retours de correction.

## Bloc annexe : A ESSAYER
Sur votre prochain prompt, écrivez seulement quatre lignes : le rôle attendu, la tâche unique à réaliser, le contexte strictement nécessaire, et le format de sortie voulu (tableau, JSON, liste à puces...). Si une ligne reste vide, supprimez-la plutôt que de la remplir par convenance.

## Textes alternatifs et légende
- **Illustration-titre (alt)** : Les pièges du prompt : flou artistique et overdose d'instructions
- **Schéma (alt)** : Schéma montrant l'axe du niveau de détail du prompt, entre trop vague (flou) à gauche et trop complexe (overdose) à droite, avec au centre la zone d'impact : équilibre sobre (rôle clair, tâche principale simple, contexte strictement nécessaire, format attendu), menant à un résultat optimal et gagné en efficacité.
- **Légende sous le schéma** : Entre le flou total et la surcharge d'instructions, la zone d'impact tient en quatre repères : rôle clair, tâche principale simple, contexte strictement nécessaire et format attendu.

## Prompt image (à coller dans Gemini)
```
Prépares-toi à générer deux images séparées, dans deux fichiers distincts. Les deux partagent cette charte graphique : style propre, moderne et professionnel, fond blanc. Palette : orange vif et bleu corporate foncé en dominantes, blanc et gris pour les respirations, accents multiculturels discrets (rouge, vert, jaune, bleu) reprenant subtilement un motif de couleurs de logo. Superpositions graphiques épurées : motifs géométriques abstraits, quartiers de cercle, lignes claires. Composition aérée, jamais surchargée. Typographie sans serif, propre et corporate. Tout texte affiché dans les images est en français.
Contexte pour comprendre le sujet, à NE PAS afficher dans les images : Lorsqu'on commence à interagir avec une intelligence artificielle, il est facile de tomber dans l'un des deux pièges opposés du prompt : le flou artistique ou l'overdose d'instructions. Dans le premier cas, on se montre trop évasif (par exemple "écrire un rapport sur le marché"), et l'IA privée de cadre comble ce vide par des choix arbitraires. À l'inverse, par excès de zèle, on rédige de véritables cahiers des charges de trois pages pour une tâche simple : c'est l'overdose, qui provoque une dilution de l'attention du modèle, au point qu'il risque d'ignorer l'instruction principale. La solution consiste à viser un équilibre sobre : un rôle clair, une seule tâche principale bien définie, le contexte strictement nécessaire, et le format attendu ; et à découper les sujets complexes en plusieurs étapes plutôt que de tout demander d'un coup.
Image 1, illustration-titre : composition épurée et moderne, focus graphique central iconique qui illustre le sujet. Ce n'est pas un schéma de processus. Seul texte à afficher : le titre, en en-tête, sans faute d'orthographe, police sans serif corporate, sans sous-titre ni texte secondaire. Le titre exact : "Les pièges du prompt : flou artistique et overdose d'instructions". Format 16:9.
Image 2, schéma explicatif, distincte et cohérente avec l'image 1 : diagramme d'entreprise propre et net de type comparaison, présentant un axe horizontal du niveau de détail d'un prompt, avec quatre blocs : un bloc à gauche pour un prompt trop vague, un bloc central pour la zone d'équilibre listant ses quatre critères, un bloc à droite pour un prompt trop complexe, et un dernier bloc pour le résultat obtenu quand l'équilibre est respecté. Libellés exacts à afficher en français : "Trop vague (flou)", "Zone d'impact : équilibre sobre" avec sous-libellés "Rôle clair", "Tâche principale simple", "Contexte strictement nécessaire", "Format attendu", "Trop complexe (overdose)", "Résultat optimal et gagné en efficacité". Très peu de fioritures, focus sur la clarté, n'inclus pas le titre. Format 4:3, cinq blocs au maximum, libellés assez grands pour rester lisibles une fois l'image réduite à 560 pixels de large.
Génère dans un premier temps seulement la première image (l'illustration-titre), et attends les instructions de l'utilisateur pour générer la 2e image.
```

Note : le titre exact fait 66 caractères. Le rendu d'origine y est parvenu, mais en cas de nouvelle tentative infructueuse, proposer à l'utilisateur de basculer sur Nano Banana Pro pour un rendu de texte plus fiable.

## Sources
- OpenAI Help Center, « Prompt engineering best practices for ChatGPT » : https://help.openai.com/en/articles/10032626-prompt-engineering-best-practices-for-chatgpt (le flou d'une consigne pousse le modèle à deviner l'intention et produit des réponses incohérentes ou hors sujet ; corrobore le paragraphe sur le flou artistique).
- Anthropic, Claude Docs, « Be clear, direct, and detailed » : https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct (une consigne ambiguë est la première cause de mauvais résultats ; il faut expliciter rôle, format et contraintes, ce qui corrobore la solution en quatre points du dernier paragraphe).
- Google Cloud, Vertex AI, « Overview of prompting strategies » : https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-design-strategies (recommande des prompts concis et explicites plutôt qu'une accumulation de contraintes, ce qui corrobore le risque de surcharge décrit dans le paragraphe sur l'overdose).
- Liu et al., « Lost in the Middle: How Language Models Use Long Contexts », arXiv:2307.03172 : https://arxiv.org/abs/2307.03172 (montre que les modèles exploitent moins bien l'information noyée au milieu d'un contenu long, ce qui appuie l'idée d'une dilution de l'attention quand les consignes s'accumulent).

## Points de vigilance
- Le paragraphe sur l'overdose affirme, en emphase, que « mathématiquement, l'IA répartit sa capacité d'analyse sur l'ensemble du texte » et que « plus vous multipliez les contraintes secondaires, plus vous risquez qu'elle ignore l'instruction principale ». C'est une simplification pédagogique plausible et cohérente avec la littérature sur la dilution d'attention en contexte long (voir source Liu et al.), mais aucune des sources trouvées ne formule ce mécanisme en ces termes précis pour un empilement de « micro-consignes » dans un seul prompt court : le texte gelé n'a donc pas été modifié, mais l'affirmation reste une extrapolation à nuancer si le sujet est repris ailleurs.
- Trois paragraphes du corps dépassent la fourchette actuelle de 45 à 60 mots (50, 79 et 67 mots) : c'est assumé conformément à la consigne, le texte gelé n'a pas été redécoupé.
- Le titre canonique (position 17 de la liste des 45) et le titre lu dans l'image-titre sont identiques au caractère près : aucun écart à signaler sur ce point.

## Fichiers écrits
- pastilles/10-les-pieges-du-prompt-flou-artistique-et-overdose-d-instructi/pastille.html
- pastilles/10-les-pieges-du-prompt-flou-artistique-et-overdose-d-instructi/image-titre.png
- pastilles/10-les-pieges-du-prompt-flou-artistique-et-overdose-d-instructi/image-schema.png
- pastilles/10-les-pieges-du-prompt-flou-artistique-et-overdose-d-instructi/meta.json
- pastilles/10-les-pieges-du-prompt-flou-artistique-et-overdose-d-instructi/pastille.md
