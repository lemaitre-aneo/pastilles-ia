# Au fait, c'est quoi un LLM ?

**Bandeau** : 1 / 45 · PASTILLE IA · Comprendre · 2 min de lecture

## L'essentiel
- Un LLM ne consulte aucune base de connaissances : il devine, mot après mot, le texte le plus probable.
- Cette simple prédiction, répétée à très grande échelle, fait émerger grammaire, raisonnement et bien d'autres compétences jamais enseignées une par une.
- Le résultat reste un pari statistique, pas une vérité : à vérifier, et à guider par une consigne précise.

## Corps

Vous connaissez la petite fonction qui, sur le clavier de votre téléphone, propose le mot suivant pendant que vous tapez ? Un *grand modèle de langage*, un "**LLM**" pour "**Large Language Model**", c'est cette idée poussée à une échelle vertigineuse. On l'imagine souvent en train de comprendre nos questions et d'aller chercher la réponse dans une immense base de données. C'est le malentendu le plus répandu, et il est trompeur. Au moment où il répond, le modèle ne consulte aucune archive : il fait tout autre chose, en apparence beaucoup plus simple. Sa seule et unique tâche, c'est de *deviner le morceau de texte le plus probable* qui vient juste après ce qu'on lui a donné. Ce qu’il a appris à faire tout seul, en devinant des milliards de fois la suite de textes dont on lui masquait le mot suivant, rectifié un peu à chaque erreur.

Pour deviner juste, le modèle ne peut pas se contenter du dernier mot. Il s'appuie sur un mécanisme dit d'*attention*, qui lui permet de peser l'importance relative des différents mots du contexte et de saisir les liens qui comptent, même lointains, par exemple à quel nom se rapporte un pronom. Et quand il génère une réponse, il tire un mot selon les **probabilités calculées**, l'ajoute au texte, puis recommence à partir de ce texte allongé : la sortie se construit de **proche en proche**, un fragment à la fois. Le plus surprenant, c'est ce qui émerge de cet objectif minimaliste. À force de prédire la suite, le modèle finit par manier la grammaire, le sens, le style, des liens factuels, et par savoir résumer, traduire, coder ou tenir une conversation, *alors qu'on ne lui a jamais enseigné ces tâches une par une*.

**[SCHEMA ICI]** (légende : À chaque étape, le modèle choisit le mot le plus probable puis recommence avec la phrase allongée, jusqu'à construire toute la réponse.)

Reste un réflexe à garder en tête, car il change concrètement votre façon de l'utiliser. Ce qui tourne sous le capot est un moteur de probabilités, **pas une base de vérités**. *Le modèle ne "comprend" pas* au sens humain : il calcule quelle suite de mots est la plus **plausible**. Il excellera donc à reformuler, condenser, traduire ou faire jaillir des idées, mais restera faillible dès qu'il s'agit d'un fait précis, d'un chiffre ou d'une référence, qu'il peut énoncer *avec le même aplomb* qu'une vérité. D'où deux habitudes utiles : **vérifier** ce qui doit l'être plutôt que de prendre la sortie pour argent comptant, et **soigner sa demande**, car plus la consigne est claire et contextualisée, plus le pari sur la suite tombe juste.

## Bloc annexe : LE PIEGE
Le modèle ne sait pas qu'il ne sait pas. Il produit toujours une suite de mots la plus probable, même face à une question sans réponse fiable : rien dans son fonctionnement ne le pousse spontanément à répondre "je ne sais pas" plutôt qu'à inventer une suite plausible.

## Textes alternatifs et légende
- Image 1 (illustration-titre), texte alternatif : Au fait, c'est quoi un LLM ?
- Image 2 (schéma), texte alternatif : Schéma du cycle de prédiction du mot suivant : à partir de "Le chat dort sur le ...", le modèle calcule des probabilités pour les mots candidats (canapé 62 %, tapis 21 %, toit 9 %, vélo 1 %), choisit "canapé", puis recommence avec "Le chat dort sur le canapé".
- Légende sous le schéma : À chaque étape, le modèle choisit le mot le plus probable puis recommence avec la phrase allongée, jusqu'à construire toute la réponse.

## Prompt image (à coller dans Gemini)

```
Prépares-toi à générer deux images séparées, dans deux fichiers distincts. Les deux partagent cette charte graphique : style propre, moderne et professionnel, fond blanc. Palette : orange vif et bleu corporate foncé en dominantes, blanc et gris pour les respirations, accents multiculturels discrets (rouge, vert, jaune, bleu) reprenant subtilement un motif de couleurs de logo. Superpositions graphiques épurées : motifs géométriques abstraits, quartiers de cercle, lignes claires. Composition aérée, jamais surchargée. Typographie sans serif, propre et corporate. Tout texte affiché dans les images est en français.
Contexte pour comprendre le sujet, à NE PAS afficher dans les images : Un grand modèle de langage (LLM) ne consulte aucune base de connaissances : sa seule tâche est de deviner le morceau de texte le plus probable qui suit ce qu'on lui a donné, un talent acquis en devinant des milliards de fois la suite de textes dont on lui masquait le mot suivant. Pour deviner juste, il s'appuie sur un mécanisme d'attention qui pèse l'importance des mots du contexte, même lointains. Il tire un mot selon les probabilités calculées, l'ajoute au texte, puis recommence à partir de ce texte allongé : la sortie se construit de proche en proche. De cet objectif minimaliste émergent la grammaire, le sens, le style, et des compétences comme résumer, traduire ou coder, jamais enseignées une par une. C'est un moteur de probabilités, pas une base de vérités : il peut énoncer une erreur avec le même aplomb qu'une vérité, d'où l'intérêt de vérifier et de soigner sa demande.
Image 1, illustration-titre : composition épurée et moderne, focus graphique central iconique qui illustre l'idée d'un modèle qui devine et assemble du texte mot après mot. Ce n'est pas un schéma de processus. Seul texte à afficher : le titre, en en-tête, sans faute d'orthographe, police sans serif corporate, sans sous-titre ni texte secondaire. Le titre exact : "Au fait, c'est quoi un LLM ?". Format 16:9.
Image 2, schéma explicatif, distinct et cohérent avec l'image 1 : diagramme de type flowchart, présentant le cycle de prédiction du mot suivant : une phrase de départ incomplète, une case représentant le modèle qui calcule des probabilités pour plusieurs mots candidats, une liste de ces mots avec leur probabilité, puis une flèche de bouclage qui revient vers le début avec la phrase complétée par le mot choisi. Libellés exacts à afficher en français : "Le chat dort sur le ...", "Modèle : prédiction du mot suivant", "canapé 62 %", "tapis 21 %", "toit 9 %", "vélo 1 %", "On recommence avec Le chat dort sur le canapé". Très peu de fioritures, focus sur la clarté, n'inclus pas le titre. Format 4:3, cinq blocs au maximum, libellés assez grands pour rester lisibles une fois l'image réduite à 560 pixels de large.
Génère dans un premier temps seulement la première image (l'illustration-titre), et attends les instructions de l'utilisateur pour générer la 2e image.
```

## Sources
- [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762) : le papier de référence qui introduit le mécanisme d'attention utilisé par les LLM pour pondérer l'importance des mots du contexte, y compris les dépendances lointaines (corrobore le paragraphe 2).
- [Emergent Abilities of Large Language Models (Wei et al., 2022)](https://arxiv.org/abs/2206.07682) : montre que des compétences (raisonnement, traduction, etc.) apparaissent à grande échelle sans avoir été enseignées tâche par tâche, ce qui corrobore l'idée que le modèle "finit par manier la grammaire, le sens... alors qu'on ne lui a jamais enseigné ces tâches une par une".
- [Why language models hallucinate (OpenAI, 2025)](https://openai.com/index/why-language-models-hallucinate/) : explique que les modèles peuvent produire des réponses fausses avec la même confiance qu'une réponse correcte, et que rien ne les pousse structurellement à répondre "je ne sais pas" ; corrobore le paragraphe 3 et le bloc "Le piège".
- [Tracing the thoughts of a large language model (Anthropic, 2025)](https://www.anthropic.com/research/tracing-thoughts-language-model) : nuance utile sur le mécanisme, au-delà de la prédiction mot à mot, certains modèles planifient en interne sur plusieurs mots à venir (voir Points de vigilance).

## Points de vigilance
- Le texte gelé présente le fonctionnement du modèle comme une prédiction strictement "mot après mot" ("il tire un mot... puis recommence"). C'est la description standard et pédagogiquement correcte du mécanisme d'entraînement et de génération (prédiction du token suivant), mais les travaux d'interprétabilité d'Anthropic montrent que certains modèles peuvent, en interne, anticiper plusieurs mots à venir (par exemple planifier une rime avant d'écrire le vers). Correctif possible si on retouchait un jour ce texte : nuancer "un fragment à la fois" par une remarque du type "même si, en coulisses, le calcul anticipe parfois plus loin que le mot immédiat". Non corrigé ici, conformément à la consigne de gel du corps.
- Les chiffres de probabilité du schéma (canapé 62 %, tapis 21 %, toit 9 %, vélo 1 %) sont un exemple pédagogique illustratif et non une mesure sourcée : aucune vérification externe n'est nécessaire ni possible, mais il convient de garder à l'esprit qu'ils ne représentent pas une sortie réelle d'un modèle précis.
- Aucun autre chiffre daté ou nom d'entreprise ne figure dans le texte gelé : rien d'autre à signaler.

## Fichiers produits
- pastilles/01-au-fait-c-est-quoi-un-llm/pastille.html
- pastilles/01-au-fait-c-est-quoi-un-llm/image-titre.png
- pastilles/01-au-fait-c-est-quoi-un-llm/image-schema.png
- pastilles/01-au-fait-c-est-quoi-un-llm/meta.json
- pastilles/01-au-fait-c-est-quoi-un-llm/pastille.md
- pastilles/01-au-fait-c-est-quoi-un-llm/pastille.eml
