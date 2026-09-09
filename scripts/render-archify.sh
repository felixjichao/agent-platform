#!/usr/bin/env bash
set -uo pipefail

ARCHIFY_BIN="${ARCHIFY_BIN:-/tmp/archify/archify/bin/archify.mjs}"
ARCHIFY_QUALITY="${ARCHIFY_QUALITY:-showcase}"
DIAGRAM_ROOT="${DIAGRAM_ROOT:-diagrams}"
PUBLIC_DIAGRAM_ROOT="${PUBLIC_DIAGRAM_ROOT:-public/diagrams}"

mapfile -t sources < <(find "$DIAGRAM_ROOT" -type f -name '*.architecture.json' | sort)
if [ "${#sources[@]}" -eq 0 ]; then
  echo "No Archify architecture sources found."
  exit 0
fi

status=0
for source in "${sources[@]}"; do
  relative="${source#${DIAGRAM_ROOT}/}"
  output="${PUBLIC_DIAGRAM_ROOT}/${relative%.json}.html"
  mkdir -p "$(dirname "$output")"

  echo "::group::Archify $source"
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
