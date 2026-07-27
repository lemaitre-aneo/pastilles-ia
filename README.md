# Pastilles IA

Outils multi-agents pour les **pastilles** pédagogiques internes sur les LLM: un texte court en français, un prompt unique de génération d'images à coller dans Gemini, puis le courriel de diffusion. Trois skills:

- **`generate`**: crée une pastille à partir d'un titre. Lance de vrais sous-agents en parallèle (rédaction sous cinq angles, fusion, puis revue critique par trois relecteurs et correction).
- **`refine`**: raffine une pastille déjà rédigée dont la conversation d'origine est perdue. On recolle le texte (et selon le cas le titre, le prompt image, les sources) plus la retouche voulue; le skill réhydrate le contexte et applique un diff minimal, sans relancer la génération complète.
- **`email`**: fabrique le courriel de diffusion, un `.msg` Outlook prêt à compléter et à envoyer, à partir du texte validé et des deux visuels collés dans la conversation. Corps HTML au gabarit, images affichées dans le corps, typographie française appliquée.

Les deux skills partagent **une seule source de vérité pour les normes de la série** (`plugins/pastille-ia/shared/regles-pastille.md`): liste des 45 pastilles et périmètre, Règles du texte et du titre, spec du prompt image, charte graphique, gabarit de diffusion, boite à outils de revue. Le gabarit HTML de diffusion vit à côté, dans `plugins/pastille-ia/shared/template-pastille.html`. Chaque skill n'y ajoute que son propre processus.

| Entrée | Invocation | Installation |
| --- | --- | --- |
| Ouvrir le dépôt dans Claude Code (local **ou** cloud web) | `/generate`, `/refine`, `/email` | aucune, chargé automatiquement |
| Installer le plugin (Cowork, autres postes) | `/pastille-ia:generate`, `/pastille-ia:refine`, `/pastille-ia:email` | via la marketplace GitHub |

Les dossiers `.claude/skills/generate`, `.claude/skills/refine` et `.claude/skills/email` sont des liens symboliques vers les sources; ce sont des **skills de projet simples**, donc Claude Code les charge sans aucune action quand on ouvre le dépôt, en local comme en session cloud (le dossier `.claude/` fait partie du clone).

## Structure

```
.claude/skills/generate -> ../../plugins/pastille-ia/skills/generate   # skill projet (symlink) -> /generate
.claude/skills/refine   -> ../../plugins/pastille-ia/skills/refine     # skill projet (symlink) -> /refine
.claude/skills/email    -> ../../plugins/pastille-ia/skills/email      # skill projet (symlink) -> /email
.claude-plugin/marketplace.json                                        # catalogue "alliance-ia" (pour Cowork / CLI)
plugins/pastille-ia/
  .claude-plugin/plugin.json                                           # manifeste du plugin
  shared/regles-pastille.md                                            # LA source unique des normes (les 3 skills la lisent)
  shared/template-pastille.html                                        # gabarit HTML de diffusion, PRODUIT par build.py --gabarit
  skills/generate/
    SKILL.md                                                           # processus de création
    references -> ../../shared                                         # symlink -> ${CLAUDE_SKILL_DIR}/references/regles-pastille.md
  skills/refine/
    SKILL.md                                                           # processus de raffinement
    references -> ../../shared                                         # symlink -> ${CLAUDE_SKILL_DIR}/references/regles-pastille.md
  skills/email/
    SKILL.md                                                           # processus de mise en courriel
    references -> ../../shared                                         # symlink -> ${CLAUDE_SKILL_DIR}/references/regles-pastille.md
    exemple/pastille-13.json                                           # fiche réelle, point de départ a copier
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
/refine        # raffiner une pastille existante (recollez son texte)
/email         # fabriquer le courriel .msg (collez les deux visuels générés)
```

Le parcours complet d'une pastille: `/generate` produit le texte et le prompt d'images, vous générez les deux visuels dans Gemini et vous les collez dans la conversation, `/email` fabrique le `.msg`. `/refine` s'intercale à tout moment pour retoucher le texte, et `/email` se rejoue ensuite sans rien régénérer.

Fonctionne à l'identique en local et en session Claude Code sur le web (les skills sont lus depuis `.claude/skills/` du clone). Aucune marketplace, aucun `/plugin install`, aucun rafraîchissement de cache.

### 2. Cowork / claude.ai

Customize > Plugins > **Add from a repository**, puis l'URL du dépôt (`https://github.com/lemaitre-aneo/pastilles-ia`). Les skills apparaissent via `/` ou le bouton `+`, sous `/pastille-ia:generate` et `/pastille-ia:refine`.

### 3. Autres postes / autres dépôts (Claude Code CLI)

```
/plugin marketplace add lemaitre-aneo/pastilles-ia
/plugin install pastille-ia@alliance-ia
/reload-plugins
```

Puis `/pastille-ia:generate`, `/pastille-ia:refine` ou `/pastille-ia:email`.

## Développement

Les normes de la série sont centralisées dans `plugins/pastille-ia/shared/regles-pastille.md`: modifiez-les là, et les deux skills en héritent (pas de duplication à synchroniser). Les processus propres à chaque skill vivent dans leur `SKILL.md`. En ouvrant le dépôt, `/generate` et `/refine` pointent (via les symlinks) directement sur ces fichiers: vos modifications sont prises en compte tout de suite, `/reload-plugins` recharge après édition. Pour publier vers Cowork et les autres postes, poussez sur GitHub (ils rafraîchissent ensuite la marketplace).

## Notes

- **Sous-agents parallèles:** `generate` lance systématiquement des sous-agents; `refine` n'en lance que pour sa revue critique optionnelle; `email` n'en lance aucun. Le processus tourne dans Claude Code et dans Cowork. Dans le chat simple de claude.ai (hors Cowork), les sous-agents ne s'exécutent pas; `generate` bascule sur son repli séquentiel documenté et `refine` propose une relecture globale unique.
- **Symlinks:** valables sous Linux/WSL et dans le cloud Linux d'Anthropic, aussi bien pour les skills projet (`.claude/skills/*`) que pour les `references -> ../../shared` internes. Un clone Windows sans support des symlinks git verrait des liens cassés; remplacer alors le lien concerné par une copie réelle du fichier cible. Même solution de repli si une session cloud ne suivait pas un symlink.
- **Courriel et Outlook:** le rendu du `.msg` est contraint par le moteur de rendu de Word, qui affiche les messages ouverts dans Outlook pour Windows. Les contournements (couleur jamais portée par un `<td>`, `color` avant `font-family`, aucun nom de police entre apostrophes, mise en forme doublée en balises `<font>`, plafond de largeur en commentaire conditionnel) sont documentés dans la spec partagée et appliqués par `render.py`. `verify.py` échoue si l'un d'eux est défait. Aucun Outlook n'existe dans l'environnement de génération: la validation finale du rendu appartient toujours à l'humain.
- **Dépendances du skill `email`:** `olefile` (vérification) et `pillow` (conversion webp et aplatissement de la transparence). Le conteneur `.msg` lui-même est écrit sans aucune dépendance.
- **Nom de marketplace vs dépôt:** la marketplace s'appelle `alliance-ia`, le dépôt GitHub `pastilles-ia`; les installations lisent `pastille-ia@alliance-ia`.
```
