#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
pip install -r requirements-dev.txt
npm install --no-save @commitlint/cli @commitlint/config-conventional husky
npx husky install
npx husky set .husky/commit-msg 'npx --no -- commitlint --edit "$1"'
cat > .husky/pre-commit <<'HOOK'
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"
ruff check .
black --check .
pytest -q
HOOK
chmod +x .husky/pre-commit
