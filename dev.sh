#!/usr/bin/env bash
# Développement du skill pastille-ia.
#
# Lance Claude Code avec le plugin chargé depuis les fichiers LOCAUX de ce dépôt.
# `--plugin-dir` est prioritaire, pour la session, sur la version publiée via la
# marketplace GitHub. Vos modifications dans plugins/pastille-ia/ sont donc prises
# en compte immédiatement, sans push ni `/plugin marketplace update`.
#
# Usage: ./dev.sh [arguments claude...]
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec claude --plugin-dir "$here/plugins/pastille-ia" "$@"
