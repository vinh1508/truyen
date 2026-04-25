#!/bin/sh
set -eu

repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root"

before=$(mktemp)
after=$(mktemp)
trap 'rm -f "$before" "$after"' EXIT

python3 - <<'PY' > "$before"
from hashlib import sha256
from pathlib import Path

for path in sorted(Path("truyen").glob("*/chapters.json")):
    print(f"{sha256(path.read_bytes()).hexdigest()}  {path}")
PY

echo "Generating chapters.json..."
python3 scripts/generate_chapters.py

python3 - <<'PY' > "$after"
from hashlib import sha256
from pathlib import Path

for path in sorted(Path("truyen").glob("*/chapters.json")):
    print(f"{sha256(path.read_bytes()).hexdigest()}  {path}")
PY

if ! cmp -s "$before" "$after"; then
  echo "Committing story files and generated manifests..."
  git add truyen
  git commit -m "chore: update story chapters"
fi

git push "$@"
