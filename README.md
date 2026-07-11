# Pastilles IA

Générateur multi-agents de **pastilles** pédagogiques internes sur les LLM: un texte court en français plus un prompt unique de génération d'images à coller dans Gemini. Le skill lance de vrais sous-agents en parallèle (rédaction sous cinq angles, fusion, puis revue critique par trois relecteurs et correction).

Ce dépôt est à la fois:
- un **skill utilisable directement** quand on ouvre le dépôt dans Claude Code (aucune installation),
- une **marketplace de plugin privée** installable dans Claude Code (CLI/web) et dans Cowork.

Une seule source de vérité: `plugins/pastille-ia/skills/pastille-ia/SKILL.md`. Le fichier `.claude/skills/pastille-ia` est un lien symbolique qui pointe vers ce skill pour l'auto-chargement local.

## Structure

```
.claude-plugin/marketplace.json                  # catalogue de la marketplace "alliance-ia"
plugins/pastille-ia/
  .claude-plugin/plugin.json                      # manifeste du plugin
  skills/pastille-ia/SKILL.md                     # le skill (source unique)
.claude/skills/pastille-ia -> ../../plugins/...   # symlink pour l'usage direct
```

## Utilisation

### 1. Directement dans ce dépôt (aucune installation)

Ouvrez Claude Code **à la racine du dépôt** et lancez:

```
/pastille-ia:pastille-ia
```

`.claude/skills/pastille-ia` est un symlink vers la racine du plugin (`plugins/pastille-ia/`, qui contient `.claude-plugin/plugin.json`). Claude Code le charge donc en place comme plugin `pastille-ia@skills-dir`, ce qui donne une invocation **namespacée identique à l'installation via marketplace**. Aucune installation, hors-ligne, source unique.

Contraintes: lancez Claude Code depuis la racine du dépôt (les plugins `@skills-dir` de portée projet ne remontent pas depuis un sous-dossier), et acceptez la fenêtre de confiance du dossier (workspace trust). Après un changement, `/reload-plugins` recharge sans redémarrer.

Note session web (Claude Code on the web): le `.claude/` du dépôt cloné est lu, mais le chargement d'un plugin `@skills-dir` en session cloud n'est pas garanti par la doc (seuls les skills simples et les plugins déclarés dans `.claude/settings.json` le sont). Si l'auto-chargement web direct devient nécessaire, basculer sur `.claude/settings.json` (`extraKnownMarketplaces` + `enabledPlugins`), documenté pour le cloud.

### 2. Comme plugin dans Claude Code (autres machines / autres dépôts)

```
/plugin marketplace add lemaitre-aneo/pastilles-ia
/plugin install pastille-ia@alliance-ia
/reload-plugins
```

Puis invoquez le skill (namespacé par le plugin):

```
/pastille-ia:pastille-ia
```

Pour tester localement avant publication, on peut aussi ajouter la marketplace depuis le chemin local: `/plugin marketplace add .`

### 3. Dans Cowork / claude.ai

Customize > Plugins > **Add from a repository**, puis indiquez l'URL du dépôt GitHub (`https://github.com/lemaitre-aneo/pastilles-ia`). Le skill `pastille-ia` apparaît ensuite via `/` ou le bouton `+`.

## Notes

- **Sous-agents parallèles:** le processus multi-agents tourne dans Claude Code et dans Cowork. Dans le chat simple de claude.ai (hors Cowork), les sous-agents ne s'exécutent pas; le skill bascule alors sur son repli séquentiel documenté.
- **Symlink:** fonctionne sous Linux/WSL et dans l'infra cloud d'Anthropic. Un collaborateur qui clone sous Windows sans support des symlinks git (`core.symlinks`) verra un lien cassé; remplacer alors `.claude/skills/pastille-ia` par une copie réelle du dossier.
- **Accès:** dépôt privé, seules les personnes ayant accès peuvent ajouter la marketplace et installer le plugin.
