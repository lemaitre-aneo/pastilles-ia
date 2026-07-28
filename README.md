# Pastilles IA

Outils multi-agents pour les **pastilles** pédagogiques internes sur les LLM: un texte court en français, un prompt unique de génération d'images à coller dans Gemini, puis le courriel de diffusion. Quatre skills:

- **`generate`**: crée une pastille à partir d'un titre. Lance de vrais sous-agents en parallèle (rédaction sous cinq angles, fusion, puis revue critique par trois relecteurs et correction). C'est aussi lui qui régénère une pastille existante quand la demande réclame du matériau neuf, un changement d'axe par exemple; l'axe demandé s'impose alors aux cinq brouillons.
- **`refine`**: réhydrate une pastille venue d'ailleurs, puis lui applique une retouche de surface. Réservé au cas où le contexte de production est perdu: on recolle le texte (et selon le cas le titre, le prompt image, les sources) plus la retouche voulue; le skill reconstitue le dossier manquant (périmètre, brief, sources) et applique un diff minimal, sans relancer la génération complète. **Une retouche demandée alors que la pastille est déjà dans la conversation ne passe pas par ce skill**, et une demande qui réclame du matériau neuf non plus (voir « Faire évoluer une pastille »).
- **`review`**: fait relire une pastille par trois relecteurs indépendants et parallèles (fond et exactitude, forme et pédagogie, conformité et visuel), qui rendent des constats localisés, consolidés et arbitrés, sans rien réécrire. Invocable seul pour un diagnostic, et déclenché par `generate` (d'office), par `refine` (sur accord) ou depuis une retouche dans le fil (sur accord).
- **`email`**: fabrique le courriel de diffusion, un `.msg` Outlook prêt à compléter et à envoyer, à partir du texte validé et des deux visuels collés dans la conversation. Corps HTML au gabarit, images affichées dans le corps, typographie française appliquée.

Les quatre skills partagent **une seule source de vérité pour les normes de la série** (`plugins/pastille-ia/shared/regles-pastille.md`): liste des 45 pastilles et périmètre, Règles du texte et du titre, spec du prompt image, charte graphique, doctrine d'évolution (retoucher, réagencer ou régénérer), gabarit de diffusion, boite à outils de revue. Le gabarit HTML de diffusion vit à côté, dans `plugins/pastille-ia/shared/template-pastille.html`. Chaque skill n'y ajoute que son propre processus.

## Faire évoluer une pastille

Une pastille se retouche plus souvent qu'elle ne se crée, et **la retouche n'est pas un skill par défaut**. Deux tests tranchent, dans cet ordre: l'ampleur de la demande, puis le contexte disponible.

| Situation | Chemin |
| --- | --- |
| **Retouche** (l'axe et le fond restent) et la pastille a été produite ou déjà travaillée dans cette conversation | Retouche directe dans le fil, **aucun skill**. Le dossier est intact, il n'y a rien à réhydrater. |
| **Retouche** d'une pastille recollée, produite ailleurs (autre conversation, session antérieure, courriel déjà diffusé) | `/refine`, qui reconstitue d'abord le dossier manquant |
| **Réagencement**: l'architecture change (ordre des paragraphes, coeur déplacé, encadré redécoupé) mais le matériau est bon | Réorganisation sur place, **sans fan-out**. Relancer cinq rédacteurs pour réarranger ce qu'on a déjà, c'est payer cinq fois pour du matériau qu'on ne cherche pas. |
| **Structurel**: il faut du matériau neuf, changement d'axe ou déplacement du sujet | Régénération par `generate`, **après confirmation** de l'utilisateur (sauf s'il l'a déjà demandée explicitement). Un diff minimal sur un axe qui change ne produit qu'un patchwork. |

La question qui sépare les deux derniers cas: **ai-je besoin de matière que je n'ai pas ?** Les mots de la demande, eux, ne décident de rien: « corrige », « raccourcis », « change le titre » se disent pareil dans les quatre cas. La doctrine complète (test de l'ampleur et signaux structurels, consignes de réagencement, régénération et ce qu'elle garde, test du contexte et ses cas limites, règles du diff minimal, re-synchronisation du prompt image, revue proposée et non imposée, sortie réduite à ce qui change) est dans la spec partagée, section « Faire évoluer une pastille »; `generate` la suit à son étape 6 et `refine` à ses étapes 3 à 5.

Une régénération n'est pas gratuite: cinq nouveaux brouillons, un titre possiblement différent, un prompt image reconstruit, donc des visuels à refaire dans Gemini et un courriel à refabriquer. C'est pour cela qu'elle se confirme avant d'être lancée. En revanche, quand l'axe est imposé, le fan-out ne se disperse plus sur cinq angles: les cinq brouillons partagent l'axe demandé et ne varient que par leur traitement.

Les sous-agents n'héritent d'aucun contexte, donc l'orchestrateur leur transmet aussi **ce qui a orienté la demande**: le retour de l'utilisateur avec ses mots, ce qui est validé et doit survivre, ce qui est écarté. Sans cela ils rejoueraient la pastille qui vient d'être refusée, faute de savoir qu'elle a existé. Le texte refusé, en revanche, ne leur est jamais transmis: il les ancrerait sur ce qu'on veut quitter, et ses défauts voyageraient avec lui. Le grief part, le texte non; seul un fragment expressément validé peut faire le voyage. Les mêmes consignes partent aux relecteurs de `review`, pour qu'ils ne prennent pas une contrainte assumée pour un défaut. Le dosage compte: trop de consignes uniformise les cinq brouillons, et c'est leur diversité qui fait la valeur de la fusion.

| Entrée | Invocation | Installation |
| --- | --- | --- |
| Ouvrir le dépôt dans Claude Code (local **ou** cloud web) | `/generate`, `/refine`, `/review`, `/email` | aucune, chargé automatiquement |
| Installer le plugin (Cowork, autres postes) | `/pastille-ia:generate`, `/pastille-ia:refine`, `/pastille-ia:review`, `/pastille-ia:email` | via la marketplace GitHub |

Les dossiers `.claude/skills/generate`, `.claude/skills/refine`, `.claude/skills/review` et `.claude/skills/email` sont des liens symboliques vers les sources; ce sont des **skills de projet simples**, donc Claude Code les charge sans aucune action quand on ouvre le dépôt, en local comme en session cloud (le dossier `.claude/` fait partie du clone).

## Structure

```
.claude/skills/generate -> ../../plugins/pastille-ia/skills/generate   # skill projet (symlink) -> /generate
.claude/skills/refine   -> ../../plugins/pastille-ia/skills/refine     # skill projet (symlink) -> /refine
.claude/skills/review   -> ../../plugins/pastille-ia/skills/review     # skill projet (symlink) -> /review
.claude/skills/email    -> ../../plugins/pastille-ia/skills/email      # skill projet (symlink) -> /email
.claude-plugin/marketplace.json                                        # catalogue "alliance-ia" (pour Cowork / CLI)
plugins/pastille-ia/
  .claude-plugin/plugin.json                                           # manifeste du plugin
  shared/regles-pastille.md                                            # LA source unique des normes (les 4 skills la lisent)
  shared/template-pastille.html                                        # gabarit HTML de diffusion, PRODUIT par build.py --gabarit
  skills/generate/
    SKILL.md                                                           # processus de création
    references -> ../../shared                                         # symlink -> ${CLAUDE_SKILL_DIR}/references/regles-pastille.md
  skills/refine/
    SKILL.md                                                           # processus de réhydratation puis retouche
    references -> ../../shared                                         # symlink -> ${CLAUDE_SKILL_DIR}/references/regles-pastille.md
  skills/review/
    SKILL.md                                                           # processus de revue critique (trois relecteurs)
    references -> ../../shared                                         # symlink -> ${CLAUDE_SKILL_DIR}/references/regles-pastille.md
  skills/email/
    SKILL.md                                                           # processus de mise en courriel
    references -> ../../shared                                         # symlink -> ${CLAUDE_SKILL_DIR}/references/regles-pastille.md
    exemple/fiche-modele.json                                          # modele de fiche a copier (aucun contenu reel)
    scripts/build.py                                                   # fiche JSON -> .msg (+ apercu HTML, + gabarit partage)
    scripts/render.py                                                  # corps HTML et texte, typographie FR, contournements Word
    scripts/msg.py                                                     # proprietes MAPI et pieces jointes en ligne
    scripts/cfb.py                                                     # ecriture du conteneur OLE2 du .msg, sans dependance
    scripts/extract_images.py                                          # recupere les images collees dans la conversation
    scripts/verify.py                                                  # relit le .msg produit et echoue si une regle est violee
```

Le symlink interne `references -> ../../shared` reste dans le dossier du plugin: c'est le contournement officiel documenté pour partager un fichier entre skills, préservé à l'installation du plugin comme à l'ouverture du dépôt. Chaque SKILL.md lit la spec via `${CLAUDE_SKILL_DIR}/references/regles-pastille.md`.

## Utilisation

### 1. Ce dépôt, dans Claude Code (local ou cloud web)

Rien à installer. Ouvrez le dépôt, accordez la confiance du dossier, puis:

```
/generate      # créer une pastille à partir d'un titre
/refine        # reprendre une pastille venue d'une autre conversation (recollez son texte)
/review        # faire relire une pastille, sans la modifier
/email         # fabriquer le courriel .msg (collez les deux visuels générés)
```

Le parcours complet d'une pastille: `/generate` produit le texte et le prompt d'images, vous générez les deux visuels dans Gemini et vous les collez dans la conversation, `/email` fabrique le `.msg`. Les retouches se demandent en langage naturel, sans commande: tant que la pastille est dans la conversation, elles s'appliquent dans le fil, puis `/email` se rejoue sans rien régénérer d'autre. `/refine` ne sert qu'à reprendre une pastille dont la conversation d'origine est perdue. `/review` juge sans modifier: `generate` le déclenche d'office, et vous pouvez l'appeler seul sur n'importe quelle pastille.

Fonctionne à l'identique en local et en session Claude Code sur le web (les skills sont lus depuis `.claude/skills/` du clone). Aucune marketplace, aucun `/plugin install`, aucun rafraîchissement de cache.

### 2. Cowork / claude.ai

Customize > Plugins > **Add from a repository**, puis l'URL du dépôt (`https://github.com/lemaitre-aneo/pastilles-ia`). Les skills apparaissent via `/` ou le bouton `+`, sous `/pastille-ia:generate` et `/pastille-ia:refine`.

### 3. Autres postes / autres dépôts (Claude Code CLI)

```
/plugin marketplace add lemaitre-aneo/pastilles-ia
/plugin install pastille-ia@alliance-ia
/reload-plugins
```

Puis `/pastille-ia:generate`, `/pastille-ia:refine`, `/pastille-ia:review` ou `/pastille-ia:email`.

## Développement

Les normes de la série sont centralisées dans `plugins/pastille-ia/shared/regles-pastille.md`: modifiez-les là, et les quatre skills en héritent (pas de duplication à synchroniser). Les processus propres à chaque skill vivent dans leur `SKILL.md`. En ouvrant le dépôt, `/generate` et `/refine` pointent (via les symlinks) directement sur ces fichiers: vos modifications sont prises en compte tout de suite, `/reload-plugins` recharge après édition. Pour publier vers Cowork et les autres postes, poussez sur GitHub (ils rafraîchissent ensuite la marketplace).

## Notes

- **Sous-agents parallèles:** `generate` en lance cinq pour ses brouillons; `review` en lance trois, un par grille de relecture; `refine` n'en lance aucun lui-même et se contente de proposer `review`; `email` n'en lance aucun. Une retouche menée dans le fil n'en lance aucun non plus, sauf si l'utilisateur accepte la revue proposée. Une régénération, en revanche, en relance cinq puis trois: c'est le coût qui justifie de la confirmer d'abord. Le processus tourne dans Claude Code et dans Cowork. Dans le chat simple de claude.ai (hors Cowork), les sous-agents ne s'exécutent pas; `generate` bascule sur son repli séquentiel documenté et `review` se replie sur un relecteur global unique.
- **Symlinks:** valables sous Linux/WSL et dans le cloud Linux d'Anthropic, aussi bien pour les skills projet (`.claude/skills/*`) que pour les `references -> ../../shared` internes. Un clone Windows sans support des symlinks git verrait des liens cassés; remplacer alors le lien concerné par une copie réelle du fichier cible. Même solution de repli si une session cloud ne suivait pas un symlink.
- **Courriel et Outlook:** le rendu du `.msg` est contraint par le moteur de rendu de Word, qui affiche les messages ouverts dans Outlook pour Windows. Les contournements (couleur jamais portée par un `<td>`, `color` avant `font-family`, aucun nom de police entre apostrophes, mise en forme doublée en balises `<font>`, plafond de largeur en commentaire conditionnel) sont documentés dans la spec partagée et appliqués par `render.py`. `verify.py` échoue si l'un d'eux est défait. Aucun Outlook n'existe dans l'environnement de génération: la validation finale du rendu appartient toujours à l'humain.
- **Dépendances du skill `email`:** `olefile` (vérification) et `pillow` (conversion webp et aplatissement de la transparence). Le conteneur `.msg` lui-même est écrit sans aucune dépendance.
- **Nom de marketplace vs dépôt:** la marketplace s'appelle `alliance-ia`, le dépôt GitHub `pastilles-ia`; les installations lisent `pastille-ia@alliance-ia`.
```
