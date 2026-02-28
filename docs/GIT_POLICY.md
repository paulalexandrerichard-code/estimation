# Git Policy

## Branch rules
- Protected branches: `main`, `develop`.
- Feature branches: `feature/atlas-architect`, `feature/atlas-trace`, `feature/atlas-link`, `feature/atlas-assemble`, `feature/atlas-stress`, `feature/ci-cd`, `feature/release-automation`, `feature/packaging-linux`, `feature/packaging-windows`.
- Start work from `develop`, keep `main` stable.
- Rebase before push: `git pull --rebase origin develop`.
- Merge using `--no-ff`.

## PR requirements
- Green CI.
- Review approval.
- Conventional commit history.
- No secrets or credentials.

## CI requirements
- Lint (ruff, black --check), tests with coverage, release checks, and secret scanning.
- Workflow triggers on push/PR per `.github/workflows`.

## Coverage requirements
- Minimum line coverage: 70%.
- CI fails under threshold.
