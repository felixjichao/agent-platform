#!/usr/bin/env bash
set -uo pipefail

ARCHIFY_BIN="${ARCHIFY_BIN:-/tmp/archify/archify/bin/archify.mjs}"
ARCHIFY_QUALITY="${ARCHIFY_QUALITY:-showcase}"
ARCHIFY_READABILITY_PATCH="${ARCHIFY_READABILITY_PATCH:-scripts/patch-archify-readability.mjs}"
DIAGRAM_ROOT="${DIAGRAM_ROOT:-diagrams}"
PUBLIC_DIAGRAM_ROOT="${PUBLIC_DIAGRAM_ROOT:-public/diagrams}"

mapfile -t sources < <(find "$DIAGRAM_ROOT" -type f -name '*.architecture.json' | sort)
if [ "${#sources[@]}" -eq 0 ]; then
  echo "No Archify architecture sources found."
  exit 0
fi

if ! node "$ARCHIFY_READABILITY_PATCH" "$ARCHIFY_BIN"; then
  echo "::error::Unable to apply the Agent Platform Archify readability profile."
  exit 1
fi

fetch_repository_evidence_revision() {
  local source="$1"
  local revision

  revision="$(node - "$source" <<'NODE'
const fs = require('node:fs')
const source = process.argv[2]
const diagram = JSON.parse(fs.readFileSync(source, 'utf8'))
process.stdout.write(diagram.meta?.repository?.revision ?? '')
NODE
)"

  if [ -z "$revision" ]; then
    return 0
  fi

  if git cat-file -e "${revision}^{commit}" 2>/dev/null; then
    return 0
  fi

  echo "Fetching pinned repository evidence revision $revision"
  if ! git fetch --no-tags --depth=1 origin "$revision"; then
    echo "::error file=$source::Unable to fetch pinned repository evidence revision $revision."
    return 1
  fi

  if ! git cat-file -e "${revision}^{commit}" 2>/dev/null; then
    echo "::error file=$source::Pinned repository evidence revision $revision is still unavailable after fetch."
    return 1
  fi
}

status=0
for source in "${sources[@]}"; do
  relative="${source#${DIAGRAM_ROOT}/}"
  output="${PUBLIC_DIAGRAM_ROOT}/${relative%.json}.html"
  mkdir -p "$(dirname "$output")"

  echo "::group::Archify $source"
  if ! fetch_repository_evidence_revision "$source"; then
    status=1
    echo "::endgroup::"
    continue
  fi
  if ! node "$ARCHIFY_BIN" validate architecture "$source" --quality "$ARCHIFY_QUALITY" --repo-root . --json; then
    status=1
    echo "::endgroup::"
    continue
  fi
  if ! node "$ARCHIFY_BIN" deliver architecture "$source" "$output" --quality "$ARCHIFY_QUALITY" --repo-root . --json; then
    status=1
  fi
  echo "::endgroup::"
done

exit "$status"
