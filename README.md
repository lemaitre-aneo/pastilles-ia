# Pastilles IA

Générateur multi-agents de **pastilles** pédagogiques internes sur les LLM: un texte court en français plus un prompt unique de génération d'images à coller dans Gemini. Le skill lance de vrais sous-agents en parallèle (rédaction sous cinq angles, fusion, puis revue critique par trois relecteurs et correction).

Le dépôt sert deux entrées, avec **une seule source de vérité** (`plugins/pastille-ia/skills/generate/SKILL.md`):

| Entrée | Invocation | Installation |
| --- | --- | --- |
| Ouvrir le dépôt dans Claude Code (local **ou** cloud web) | `/generate` | aucune, chargé automatiquement |
| Installer le plugin (Cowork, autres postes) | `/pastille-ia:generate` | via la marketplace GitHub |

Le fichier `.claude/skills/generate` est un lien symbolique vers la source; c'est un **skill de projet simple**, donc Claude Code le charge sans aucune action quand on ouvre le dépôt, en local comme en session cloud (le dossier `.claude/` fait partie du clone).

## Structure

```
.claude/skills/generate -> ../../plugins/pastille-ia/skills/generate   # skill projet (symlink) -> /generate, zéro action
.claude-plugin/marketplace.json                                        # catalogue "alliance-ia" (pour Cowork / CLI)
plugins/pastille-ia/
  .claude-plugin/plugin.json                                            # manifeste du plugin
  skills/generate/SKILL.md                                              # LA source unique
```

## Utilisation

### 1. Ce dépôt, dans Claude Code (local ou cloud web)

Rien à installer. Ouvrez le dépôt, accordez la confiance du dossier, puis:

```
/generate
```

Fonctionne à l'identique en local et en session Claude Code sur le web (le skill est lu depuis `.claude/skills/` du clone). Aucune marketplace, aucun `/plugin install`, aucun rafraîchissement de cache.

### 2. Cowork / claude.ai

Customize > Plugins > **Add from a repository**, puis l'URL du dépôt (`https://github.com/lemaitre-aneo/pastilles-ia`). Le skill apparaît via `/` ou le bouton `+`, sous `/pastille-ia:generate`.

### 3. Autres postes / autres dépôts (Claude Code CLI)

```
/plugin marketplace add lemaitre-aneo/pastilles-ia
/plugin install pastille-ia@alliance-ia
/reload-plugins
```

Puis `/pastille-ia:generate`.

## Développement

La source unique est `plugins/pastille-ia/skills/generate/SKILL.md`. En ouvrant le dépôt, `/generate` pointe (via le symlink) directement sur ce fichier: vos modifications sont prises en compte tout de suite, `/reload-plugins` recharge après édition. Pour publier vers Cowork et les autres postes, poussez sur GitHub (ils rafraîchissent ensuite la marketplace).

## Notes

- **Sous-agents parallèles:** le processus multi-agents tourne dans Claude Code et dans Cowork. Dans le chat simple de claude.ai (hors Cowork), les sous-agents ne s'exécutent pas; le skill bascule sur son repli séquentiel documenté.
- **Symlink:** valable sous Linux/WSL et dans le cloud Linux d'Anthropic. Un clone Windows sans support des symlinks git verrait un lien cassé; remplacer alors `.claude/skills/generate` par une copie réelle du `SKILL.md`. Même solution de repli si une session cloud ne suivait pas le symlink.
- **Nom de marketplace vs dépôt:** la marketplace s'appelle `alliance-ia`, le dépôt GitHub `pastilles-ia`; les installations lisent `pastille-ia@alliance-ia`.
