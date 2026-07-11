# Pastilles IA

Générateur multi-agents de **pastilles** pédagogiques internes sur les LLM: un texte court en français plus un prompt unique de génération d'images à coller dans Gemini. Le skill lance de vrais sous-agents en parallèle (rédaction sous cinq angles, fusion, puis revue critique par trois relecteurs et correction).

Ce dépôt est à la fois:
- une **marketplace de plugin privée** installable dans Claude Code (CLI/web) et dans Cowork,
- un dépôt qui **s'auto-configure** quand on l'ouvre dans Claude Code (le plugin s'installe via `.claude/settings.json`).

Invocation partout: **`/pastille-ia:generate`**. Source unique de vérité: `plugins/pastille-ia/skills/generate/SKILL.md`.

## Structure

```
.claude/settings.json                             # déclare la marketplace + active le plugin (local + cloud)
.claude-plugin/marketplace.json                   # catalogue de la marketplace "alliance-ia"
plugins/pastille-ia/
  .claude-plugin/plugin.json                       # manifeste du plugin
  skills/generate/SKILL.md                         # le skill (source unique)
```

## Utilisation

### 1. Ce dépôt, dans Claude Code (local ou web)

`.claude/settings.json` déclare la marketplace `alliance-ia` (source GitHub) et active `pastille-ia@alliance-ia`. C'est le mécanisme documenté qui fonctionne **aussi en session cloud**.

- **Claude Code sur le web (session cloud sur ce dépôt):** le plugin est installé automatiquement au démarrage de la session depuis la marketplace déclarée. Rien à faire, puis `/pastille-ia:generate`.
- **Claude Code local:** à la première ouverture, après avoir accordé la confiance du dossier (workspace trust), Claude Code propose d'installer la marketplace et le plugin; acceptez (ou lancez `/plugin install pastille-ia@alliance-ia`). Ensuite `/pastille-ia:generate`. Le plugin est mis en cache, donc disponible hors-ligne aux ouvertures suivantes.

La première installation (locale et cloud) nécessite un accès réseau au dépôt GitHub (marketplace privée).

### 2. Autres machines / autres dépôts (Claude Code CLI)

```
/plugin marketplace add lemaitre-aneo/pastilles-ia
/plugin install pastille-ia@alliance-ia
/reload-plugins
```

Puis `/pastille-ia:generate`.

### 3. Cowork / claude.ai

Customize > Plugins > **Add from a repository**, puis indiquez l'URL du dépôt GitHub (`https://github.com/lemaitre-aneo/pastilles-ia`). Le skill apparaît ensuite via `/` ou le bouton `+`.

## Notes

- **Sous-agents parallèles:** le processus multi-agents tourne dans Claude Code et dans Cowork. Dans le chat simple de claude.ai (hors Cowork), les sous-agents ne s'exécutent pas; le skill bascule alors sur son repli séquentiel documenté.
- **Accès:** dépôt privé; seules les personnes ayant accès peuvent installer le plugin. En session cloud, l'installation réutilise l'accès GitHub de la session.
- **Nom de marketplace vs dépôt:** la marketplace s'appelle `alliance-ia` (dans `marketplace.json` et `settings.json`), le dépôt GitHub `pastilles-ia`. Les installations lisent donc `pastille-ia@alliance-ia`.
