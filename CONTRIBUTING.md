# Contributing

## Branching
- Branch from `develop` using `feature/*` names.
- Merge with `--no-ff` through PR.
- Never commit directly to `main`.

## Conventional Commits
Use `type(scope): subject` and allowed types: `feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert`.

## Developer setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
bash scripts/dev_setup.sh
```

Windows:
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements-dev.txt
powershell -ExecutionPolicy Bypass -File scripts/dev_setup.ps1
```

## Quality gates
- `ruff check .`
- `black --check .`
- `pytest --cov`
- Coverage must stay >= 70%.
