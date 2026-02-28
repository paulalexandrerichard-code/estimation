python -m pip install --upgrade pip
pip install -r requirements-dev.txt
npm install --no-save @commitlint/cli @commitlint/config-conventional husky
npx husky install

@(
'#!/usr/bin/env sh',
'. "$(dirname -- "$0")/_/husky.sh"',
'npx --no -- commitlint --edit "$1"'
) | Set-Content .husky/commit-msg

@(
'#!/usr/bin/env sh',
'. "$(dirname -- "$0")/_/husky.sh"',
'ruff check .',
'black --check .',
'pytest -q'
) | Set-Content .husky/pre-commit
