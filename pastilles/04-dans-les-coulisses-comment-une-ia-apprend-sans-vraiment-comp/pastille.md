# Dans les coulisses : comment une IA apprend (sans vraiment comprendre)

**Bandeau** : 4 / 45 · PASTILLE IA · Comprendre · 2 min de lecture

## L'essentiel
- Un LLM apprend seul en devinant le mot suivant dans des textes existants (apprentissage auto-supervisé).
- Chaque erreur ajuste très légèrement des milliards de réglages internes, sans qu'aucune règle ne soit jamais écrite.
- Une seconde phase, guidée par des humains qui notent ses réponses, en fait un assistant serviable.

## Corps

Un modèle ne naît pas en sachant parler, il l'apprend. Sa matière première ? Une **bibliothèque colossale** de textes écrits par des humains. Le tour de force, c'est que cette montagne de données n'a besoin d'aucune correction manuelle : *le texte est son propre corrigé*. On lui cache le mot qui suit, il tente de le deviner, et la vraie suite lui dit aussitôt s'il avait juste. Pas besoin d'une armée de professeurs pour noter ses copies : on appelle ça l'apprentissage **auto-supervisé**. Et c'est ce qui rend l'échelle possible, avec des milliards d'exemples qui défilent sans qu'un humain intervienne.

Mais que se passe-t-il quand il se trompe ? C'est là que tout se joue. Le modèle est fait de **milliards de réglages internes**, un peu comme une console de mixage aux boutons innombrables, tous placés au hasard le premier jour. Ses premières tentatives ne sont donc que du charabia. À chaque essai, on mesure **l'écart** entre le mot parié et le vrai mot, puis on tourne très légèrement chaque bouton dans le sens qui aurait réduit l'erreur. Une correction infime, presque rien, mais répétée un nombre astronomique de fois. Le point clé : personne n'écrit jamais la moindre règle, ni "l'adjectif s'accorde", ni aucune date. Tout ce que le modèle finit par savoir se **dépose** peu à peu, tout seul, dans ces réglages, *à la seule force des corrections statistiques*.

**[SCHÉMA ICI]** (voir description et légende ci-dessous).

À ce stade, le modèle est un érudit un peu sauvage : il sait prolonger n'importe quel texte, mais il ne fait que ça, prolonger, sans forcément répondre à la question. Vient alors un **second temps d'apprentissage**, avec des humains dans la boucle. On lui montre des exemples de bonnes réponses, on le laisse s'exercer, puis on **note** ses essais pour lui signaler les plus justes. De fil en aiguille, *il ajuste ses préférences* et devient l'assistant serviable qu'on utilise. À aucun moment le but n'a été de saisir le sens, ni de dire le vrai, seulement de produire la suite la plus **plausible**. Le modèle a appris à merveille les *formes* du langage, beaucoup moins le monde qu'elles désignent.

## Bloc annexe : LE PIÈGE
Le modèle n'a appris que les formes du langage, pas le monde qu'elles décrivent : un texte parfaitement fluide et bien construit peut donc être totalement faux, sans que rien dans son style ne le trahisse.

## Textes alternatifs et légende
- **Image 1 (illustration-titre)**, texte alternatif : « Dans les coulisses : comment une IA apprend (sans vraiment comprendre) »
- **Image 2 (schéma)**, texte alternatif : « Schéma en deux étapes : étape 1, Auto-apprentissage sur du texte, avec le cycle Deviner le mot suivant, Comparer au vrai mot (écart), Ajuster les milliards de réglages, Répété des milliards de fois ; étape 2, Mise au point avec des humains, avec Exemples de bonnes réponses et Noter ses essais menant à Assistant serviable. »
- **Légende sous le schéma** : « Le modèle passe d'abord par un cycle d'auto-apprentissage sur du texte, avant une phase de mise au point guidée par des humains. »

## Prompt image (à coller dans Gemini)

```
Prépares-toi à générer deux images séparées, dans deux fichiers distincts. Les deux partagent cette charte graphique : style propre, moderne et professionnel, fond blanc. Palette : orange vif et bleu corporate foncé en dominantes, blanc et gris pour les respirations, accents multiculturels discrets (rouge, vert, jaune, bleu) reprenant subtilement un motif de couleurs de logo. Superpositions graphiques épurées : motifs géométriques abstraits, quartiers de cercle, lignes claires. Composition aérée, jamais surchargée. Typographie sans serif, propre et corporate. Tout texte affiché dans les images est en français.

Contexte pour comprendre le sujet, à NE PAS afficher dans les images : Un modèle ne naît pas en sachant parler, il l'apprend, à partir d'une bibliothèque colossale de textes écrits par des humains, sans correction manuelle : le texte est son propre corrigé. On lui cache le mot qui suit, il tente de le deviner, et la vraie suite lui dit aussitôt s'il avait juste ; c'est l'apprentissage auto-supervisé, qui permet à des milliards d'exemples de défiler sans qu'un humain intervienne. Quand le modèle se trompe, on mesure l'écart entre le mot parié et le vrai mot, puis on ajuste très légèrement chacun de ses milliards de réglages internes (un peu comme une immense console de mixage) dans le sens qui aurait réduit l'erreur, une correction infime répétée un nombre astronomique de fois, sans qu'aucune règle ne soit jamais écrite. Puis vient un second temps d'apprentissage, avec des humains dans la boucle : on montre au modèle des exemples de bonnes réponses, on le laisse s'exercer, on note ses essais, et il ajuste peu à peu ses préférences jusqu'à devenir l'assistant serviable qu'on utilise. À aucun moment le but n'a été de saisir le sens ou de dire le vrai, seulement de produire la suite la plus plausible : le modèle a appris à merveille les formes du langage, beaucoup moins le monde qu'elles désignent.

Image 1, illustration-titre : composition épurée et moderne, focus graphique central iconique qui illustre le sujet (par exemple une main ou un bras robotique réglant les boutons d'une console de mixage géante, symbolisant l'ajustement des réglages internes du modèle). Ce n'est pas un schéma de processus. Seul texte à afficher : le titre, en en-tête, sans faute d'orthographe, police sans serif corporate, sans sous-titre ni texte secondaire. Le titre exact : "Dans les coulisses : comment une IA apprend (sans vraiment comprendre)". Format 16:9.

Image 2, schéma explicatif, distinct et cohérent avec l'image 1 : diagramme d'entreprise propre et net en deux blocs côte à côte, reliés par une flèche. Bloc 1, intitulé "Auto-apprentissage sur du texte" : un cycle en boucle de quatre étapes, "Deviner le mot suivant", "Comparer au vrai mot (écart)", "Ajuster les milliards de réglages", "Répété des milliards de fois", qui se répète en boucle. Bloc 2, intitulé "Mise au point avec des humains" : deux entrées, "Exemples de bonnes réponses" et "Noter ses essais", convergeant vers un résultat final, "Assistant serviable". Libellés exacts à afficher en français : Auto-apprentissage sur du texte, Deviner le mot suivant, Comparer au vrai mot (écart), Ajuster les milliards de réglages, Répété des milliards de fois, Mise au point avec des humains, Exemples de bonnes réponses, Noter ses essais, Assistant serviable. Très peu de fioritures, focus sur la clarté, n'inclus pas le titre. Format 4:3, cinq blocs au maximum, libellés assez grands pour rester lisibles une fois l'image réduite à 560 pixels de large.

Génère dans un premier temps seulement la première image (l'illustration-titre), et attends les instructions de l'utilisateur pour générer la 2e image.
```

## Sources
- Anthropic, glossaire officiel (définitions "Pretraining" et "RLHF") : https://platform.claude.com/docs/fr/about-claude/glossary (corrobore le mécanisme d'auto-apprentissage par prédiction du mot suivant, paragraphe 1, et la seconde phase de mise au point par retour humain, paragraphe 3).
- OpenAI, "Improving Language Understanding by Generative Pre-Training" (papier fondateur GPT) : https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf (corrobore le principe en deux temps, préentraînement non supervisé sur texte brut puis ajustement supervisé).
- OpenAI, "Training language models to follow instructions with human feedback" (InstructGPT) : https://arxiv.org/abs/2203.02155 (détaille la phase de mise au point avec des humains qui notent et classent les réponses, paragraphe 3).
- Google for Developers, "Neural Networks: Training using backpropagation" : https://developers.google.com/machine-learning/crash-course/neural-networks/backpropagation (corrobore le mécanisme d'ajustement progressif des poids/paramètres à partir de l'écart mesuré, paragraphe 2).

## Points de vigilance
- Aucune erreur factuelle, chiffre douteux, tiret cadratin ou nom d'entreprise repéré dans le texte gelé : rien à signaler ici.
- Le titre rendu dans l'image 1 correspond au caractère près au titre du sujet du courriel et au titre canonique de la liste des 45 : aucun écart à signaler.
- Le bloc annexe "Le piège" est un ajout volontaire (conséquence de "le modèle a appris les formes, pas le monde") : à surveiller pour ne pas trop empiéter sur le futur sujet des hallucinations (pastille 13), mais l'angle ici reste la cause structurelle (apprentissage de la forme, pas du sens), pas le phénomène d'hallucination lui-même.
