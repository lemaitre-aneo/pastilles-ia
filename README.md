# Pastilles IA

Outils multi-agents pour les **pastilles** pédagogiques internes sur les LLM: un texte court en français plus un prompt unique de génération d'images à coller dans Gemini. Deux skills:

- **`generate`**: crée une pastille à partir d'un titre. Lance de vrais sous-agents en parallèle (rédaction sous cinq angles, fusion, puis revue critique par trois relecteurs et correction).
- **`refine`**: raffine une pastille déjà rédigée dont la conversation d'origine est perdue. On recolle le texte (et selon le cas le titre, le prompt image, les sources) plus la retouche voulue; le skill réhydrate le contexte et applique un diff minimal, sans relancer la génération complète.

Les deux skills partagent **une seule source de vérité pour les normes de la série** (`plugins/pastille-ia/shared/regles-pastille.md`): liste des 45 pastilles et périmètre, Règles du texte et du titre, spec du prompt image, charte graphique, gabarit de diffusion, boite à outils de revue. Le gabarit HTML de diffusion vit à côté, dans `plugins/pastille-ia/shared/template-pastille.html`. Chaque skill n'y ajoute que son propre processus.

| Entrée | Invocation | Installation |
| --- | --- | --- |
| Ouvrir le dépôt dans Claude Code (local **ou** cloud web) | `/generate`, `/refine` | aucune, chargé automatiquement |
| Installer le plugin (Cowork, autres postes) | `/pastille-ia:generate`, `/pastille-ia:refine` | via la marketplace GitHub |

Les dossiers `.claude/skills/generate` et `.claude/skills/refine` sont des liens symboliques vers les sources; ce sont des **skills de projet simples**, donc Claude Code les charge sans aucune action quand on ouvre le dépôt, en local comme en session cloud (le dossier `.claude/` fait partie du clone).

## Structure

```
.claude/skills/generate -> ../../plugins/pastille-ia/skills/generate   # skill projet (symlink) -> /generate
.claude/skills/refine   -> ../../plugins/pastille-ia/skills/refine     # skill projet (symlink) -> /refine
.claude-plugin/marketplace.json                                        # catalogue "alliance-ia" (pour Cowork / CLI)
plugins/pastille-ia/
  .claude-plugin/plugin.json                                           # manifeste du plugin
  shared/regles-pastille.md                                            # LA source unique des normes (les 2 skills la lisent)
  shared/template-pastille.html                                        # gabarit HTML de diffusion (a coller dans le client mail)
  skills/generate/
    SKILL.md                                                           # processus de création
    references -> ../../shared                                         # symlink -> ${CLAUDE_SKILL_DIR}/references/regles-pastille.md
  skills/refine/
    SKILL.md                                                           # processus de raffinement
    references -> ../../shared                                         # symlink -> ${CLAUDE_SKILL_DIR}/references/regles-pastille.md
```

Le symlink interne `references -> ../../shared` reste dans le dossier du plugin: c'est le contournement officiel documenté pour partager un fichier entre skills, préservé à l'installation du plugin comme à l'ouverture du dépôt. Chaque SKILL.md lit la spec via `${CLAUDE_SKILL_DIR}/references/regles-pastille.md`.

## Utilisation

### 1. Ce dépôt, dans Claude Code (local ou cloud web)

Rien à installer. Ouvrez le dépôt, accordez la confiance du dossier, puis:

```
/generate      # créer une pastille à partir d'un titre
/refine        # raffiner une pastille existante (recollez son texte)
```

Fonctionne à l'identique en local et en session Claude Code sur le web (les skills sont lus depuis `.claude/skills/` du clone). Aucune marketplace, aucun `/plugin install`, aucun rafraîchissement de cache.

### 2. Cowork / claude.ai

Customize > Plugins > **Add from a repository**, puis l'URL du dépôt (`https://github.com/lemaitre-aneo/pastilles-ia`). Les skills apparaissent via `/` ou le bouton `+`, sous `/pastille-ia:generate` et `/pastille-ia:refine`.

### 3. Autres postes / autres dépôts (Claude Code CLI)

```
/plugin marketplace add lemaitre-aneo/pastilles-ia
/plugin install pastille-ia@alliance-ia
/reload-plugins
```

Puis `/pastille-ia:generate` ou `/pastille-ia:refine`.

## Reprise des pastilles déjà diffusées

Les pastilles envoyées avant la mise en place du gabarit actuel vivent dans `emails/` (les `.eml` d'origine) et sont reprises dans `pastilles/`, un dossier par pastille. Le corps du texte y est **inchangé**: la reprise ajoute seulement ce que le gabarit impose (bandeau de série, encadré "L'essentiel", légende du schéma, bloc annexe), les textes alternatifs rédigés d'après les visuels, les sources qui corroborent le message et un prompt image régénéré. Voir `pastilles/README.md` pour l'index et les points de vigilance relevés.

Trois outils, dans `tools/`:

| Outil | Rôle |
| --- | --- |
| `import_emails.py` | éclate chaque `.eml` vers `work/<slug>/`: texte brut, HTML porteur des emphases d'origine, images liées dans leur ordre d'apparition |
| `build_eml.py` | reconstruit un `.eml` diffusable à partir du gabarit HTML rempli et des deux visuels, en résolvant `cid:IMAGE_TITRE` et `cid:IMAGE_SCHEMA` |
| `check_pastille.py` | compare le corps réexporté au courriel d'origine caractère par caractère, et vérifie les contraintes du gabarit (crochets résiduels, tiret cadratin, textes alternatifs, jetons `cid`, blocs, temps de lecture) |

```
python3 tools/import_emails.py emails work     # importer les .eml
python3 tools/check_pastille.py --all          # verifier les 13 reprises
python3 tools/normalize_meta.py                # normaliser les meta.json et regenerer l'index
```

Le corps gelé fait que certains défauts hérités (paragraphes de plus de 60 mots, emphases surabondantes, artefacts de mise en forme Outlook) subsistent volontairement: ils sont remontés dans les points de vigilance plutôt que corrigés. Une dérogation assumée au gel se déclare dans `pastilles/<slug>/gel-exceptions.json`, que le vérificateur applique avant comparaison puis rappelle en avertissement, pour qu'elle ne passe ni pour une modification silencieuse ni pour un échec.

Le dossier `work/` est un intermédiaire, hors dépôt.

## Développement

Les normes de la série sont centralisées dans `plugins/pastille-ia/shared/regles-pastille.md`: modifiez-les là, et les deux skills en héritent (pas de duplication à synchroniser). Les processus propres à chaque skill vivent dans leur `SKILL.md`. En ouvrant le dépôt, `/generate` et `/refine` pointent (via les symlinks) directement sur ces fichiers: vos modifications sont prises en compte tout de suite, `/reload-plugins` recharge après édition. Pour publier vers Cowork et les autres postes, poussez sur GitHub (ils rafraîchissent ensuite la marketplace).

## Notes

- **Sous-agents parallèles:** `generate` lance systématiquement des sous-agents; `refine` n'en lance que pour sa revue critique optionnelle. Le processus tourne dans Claude Code et dans Cowork. Dans le chat simple de claude.ai (hors Cowork), les sous-agents ne s'exécutent pas; `generate` bascule sur son repli séquentiel documenté et `refine` propose une relecture globale unique.
- **Symlinks:** valables sous Linux/WSL et dans le cloud Linux d'Anthropic, aussi bien pour les skills projet (`.claude/skills/*`) que pour les `references -> ../../shared` internes. Un clone Windows sans support des symlinks git verrait des liens cassés; remplacer alors le lien concerné par une copie réelle du fichier cible. Même solution de repli si une session cloud ne suivait pas un symlink.
- **Nom de marketplace vs dépôt:** la marketplace s'appelle `alliance-ia`, le dépôt GitHub `pastilles-ia`; les installations lisent `pastille-ia@alliance-ia`.
```
