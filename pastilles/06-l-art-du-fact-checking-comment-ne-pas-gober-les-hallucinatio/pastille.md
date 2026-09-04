# L'art du Fact-Checking : comment ne pas gober les hallucinations de l'IA

**Bandeau** : 6 / 45 · PASTILLE IA · Limites · 2 min de lecture

## L'essentiel
- Une réponse d'IA est un brouillon à relire, jamais une vérité établie.
- La vérification cible les points à enjeu (chiffres, dates, citations, sources), recoupés dans une source indépendante.
- Redemander "tu es sûr ?" à l'IA ne prouve rien : sa confiance affichée n'est pas fiable.

## Corps

Pensez à un **stagiaire brillant** : rapide, cultivé, mais qui invente parfois, toujours avec le même aplomb tranquille. C'est ce qu'on appelle une *hallucination*. Vous ne le renvoyez pas pour autant : vous relisez son travail avant de le signer. Voilà le bon réflexe face à l'IA : une réponse n'est pas une source de vérité, c'est un **brouillon**. Et surtout, *le ton assuré n'est pas un indice de fiabilité* : le modèle énonce une bêtise avec la même assurance qu'une évidence.

Pas question pour autant de tout vérifier : ce serait perdre le temps qu'on venait de gagner. Concentrez l'effort sur ce qui est **vérifiable et à enjeu** : noms, chiffres, dates, citations, références, liens, affirmations juridiques ou techniques. Ce sont les points où le modèle se trompe le plus, et ceux qui coûtent cher dans un document qui sort de la maison ; le plan et les reformulations, eux, se relisent comme d'habitude. Calez ensuite le niveau de contrôle sur l'enjeu : un simple coup d'oeil pour un brouillon interne, une vraie vérification pour un chiffre publié ou un livrable client. Et redoublez de prudence sur les sujets pointus et l'actualité récente, là où l'IA invente le plus.

Un bon point de départ, dès la question : demandez au modèle de **chercher et de citer ses sources**. L'effet est double. D'abord, il s'appuie sur des documents réels plutôt que sur sa seule mémoire, ce qui réduit déjà le risque d'invention. Ensuite, vous obtenez une piste directe à contrôler. Mais ce n'est pas une garantie : une source citée peut être **inventée**, ou réelle mais détournée. Il ne suffit donc pas qu'elle *existe*, encore faut-il l'ouvrir et vérifier qu'elle dit bien cela. Et ce contrôle se fait *ailleurs*, dans une **source indépendante** (publication d'origine, documentation officielle) : c'est la **lecture latérale**, on quitte la conversation pour recouper plutôt que de creuser la réponse elle-même.

**[SCHEMA]**

Reste un réflexe à désapprendre : relancer l'IA d'un "tu es sûr ?" n'est *pas* une vérification. Par complaisance, le modèle se rétracte souvent dès qu'on le conteste, même quand il avait raison, ou campe sur sa position avec le même aplomb : dans les deux cas, sa confiance n'est pas calibrée sur la vérité. L'interroger sur ses propres dires, c'est un peu comme demander au suspect de témoigner pour lui-même. Et c'est bien là que tout se joue : plus une réponse est fluide, plus on baisse la garde, si bien que les inventions les mieux emballées sont les plus dangereuses. Bien menée, la vérification n'est pourtant pas un frein : elle transforme l'IA d'oracle risqué en **accélérateur fiable**. Au bout du compte, l'IA propose, une source extérieure dispose, et c'est vous qui signez.

## Bloc annexe : A essayer
Sur la prochaine réponse chiffrée ou datée, pratiquez la lecture latérale : ouvrez un nouvel onglet, cherchez l'information avec deux ou trois mots clés, et ne validez que si une source indépendante dit la même chose.

## Textes alternatifs et légende
- **Image 1 (illustration-titre), texte alternatif** : L'art du Fact-Checking : comment ne pas gober les hallucinations de l'IA
- **Image 2 (schéma), texte alternatif** : Schéma du circuit de vérification : réponse + sources citées = brouillon, puis repérage des points à enjeu (chiffres, citations, dates, liens), recoupement dans une source indépendante (publication d'origine, documentation officielle), pour aboutir à confirmé ou à faux ou déformé, à corriger ; à l'écart, la boucle "tu es sûr ? : fausse vérification".
- **Légende sous le schéma** : Le circuit va d'une réponse sourcée au recoupement indépendant, jusqu'à confirmé ou à corriger ; redemander "tu es sûr ?" à l'IA court-circuite ce recoupement.

## Prompt image (a coller dans Gemini)

```
Prépares-toi à générer deux images séparées, dans deux fichiers distincts. Les deux partagent cette charte graphique : style propre, moderne et professionnel, fond blanc. Palette : orange vif et bleu corporate foncé en dominantes, blanc et gris pour les respirations, accents multiculturels discrets (rouge, vert, jaune, bleu) reprenant subtilement un motif de couleurs de logo. Superpositions graphiques épurées : motifs géométriques abstraits, quartiers de cercle, lignes claires. Composition aérée, jamais surchargée. Typographie sans serif, propre et corporate. Tout texte affiché dans les images est en français.
Contexte pour comprendre le sujet, à NE PAS afficher dans les images : Pensez à un stagiaire brillant : rapide, cultivé, mais qui invente parfois, toujours avec le même aplomb tranquille. C'est ce qu'on appelle une hallucination. Vous ne le renvoyez pas pour autant : vous relisez son travail avant de le signer. Voila le bon réflexe face à l'IA : une réponse n'est pas une source de vérité, c'est un brouillon. Et surtout, le ton assuré n'est pas un indice de fiabilité : le modèle énonce une bêtise avec la même assurance qu'une évidence. Pas question pour autant de tout vérifier : ce serait perdre le temps qu'on venait de gagner. Concentrez l'effort sur ce qui est vérifiable et à enjeu : noms, chiffres, dates, citations, références, liens, affirmations juridiques ou techniques. Calez le niveau de contrôle sur l'enjeu, et redoublez de prudence sur les sujets pointus et l'actualité récente. Un bon point de départ, dès la question : demandez au modèle de chercher et de citer ses sources, ce qui réduit le risque d'invention et donne une piste à contrôler. Mais une source citée peut être inventée, ou réelle mais détournée : il faut l'ouvrir et la recouper ailleurs, dans une source indépendante (publication d'origine, documentation officielle), c'est la lecture latérale. Reste un réflexe à désapprendre : relancer l'IA d'un "tu es sûr ?" n'est pas une vérification, car par complaisance le modèle se rétracte ou campe sur sa position avec le même aplomb, sans que sa confiance soit calibrée sur la vérité. Bien menée, la vérification transforme l'IA d'oracle risqué en accélérateur fiable : l'IA propose, une source extérieure dispose, et c'est l'humain qui signe.
Image 1, illustration-titre : composition épurée et moderne, focus graphique central iconique qui illustre le sujet. Ce n'est pas un schéma de processus. Seul texte à afficher : le titre, en en-tête, sans faute d'orthographe, police sans serif corporate, sans sous-titre ni texte secondaire. Le titre exact : "L'art du Fact-Checking : comment ne pas gober les hallucinations de l'IA". Format 16:9.
Image 2, schéma explicatif, distincte et cohérente avec l'image 1 : diagramme d'entreprise propre et net de type flowchart, présentant le circuit de vérification d'une réponse d'IA, de la réponse sourcée jusqu'au verdict, avec une boucle annexe qui écarte la fausse vérification. Libellés exacts à afficher en français : "Réponse + sources citées = brouillon", "Repérage des points à enjeu (chiffres, citations, dates, liens)", "Recoupement dans une source indépendante (publication d'origine, documentation officielle)", "Confirmé", "Faux ou déformé, à corriger". Très peu de fioritures, focus sur la clarté, n'inclus pas le titre. Format 4:3, cinq blocs au maximum, libellés assez grands pour rester lisibles une fois l'image réduite à 560 pixels de large.
Génère dans un premier temps seulement la première image (l'illustration-titre), et attends les instructions de l'utilisateur pour générer la 2e image.
```

## Sources
- OpenAI, "Why language models hallucinate" (rapport de recherche, septembre 2026) : https://openai.com/index/why-language-models-hallucinate/ — corrobore le paragraphe 1 : les modèles sont entraînés à deviner plutôt qu'à reconnaître leur incertitude, d'où des réponses fausses énoncées avec la même assurance que des réponses justes.
- Anthropic, "Towards Understanding Sycophancy in Language Models" (arXiv 2310.13548) : https://arxiv.org/abs/2310.13548 — corrobore le paragraphe 4 : les assistants IA ont tendance à se rétracter ou à flatter l'avis de l'utilisateur plutôt qu'à rester calibrés sur la vérité quand on les conteste.
- Mike Caulfield, "SIFT (The Four Moves)" (Hapgood, méthode de lecture latérale des fact-checkers professionnels) : https://hapgood.us/2019/06/19/sift-the-four-moves/ — corrobore le paragraphe 3 : la vérification se fait en quittant la source pour la recouper ailleurs, principe repris dans le bloc "A essayer".
- U.S. District Court, S.D.N.Y., *Mata v. Avianca, Inc.*, Opinion and Order on Sanctions, 22 juin 2023 : https://law.justia.com/cases/federal/district-courts/new-york/nysdce/1:2022cv01461/575368/54/ — illustre concrètement, par un cas sanctionné en justice, l'affirmation du paragraphe 3 selon laquelle une source citée par l'IA peut être entièrement inventée.

## Points de vigilance
- Aucun chiffre, date ou nom d'entreprise n'apparaît dans le texte gelé : rien à corriger ni à nuancer sur ce plan.
- Le texte gelé contient un caractère non standard hérité de la source (apostrophe typographique dans "coup d'oeil", rendue ’ dans le HTML d'origine) : conservé tel quel dans `pastille.html` conformément à la règle de gel mot pour mot: aucune harmonisation de ponctuation n'a été appliquée.
- Le titre retenu (image-1) est identique au titre du sujet du courriel et au titre canonique de la position 14 : aucun écart à signaler.
