# Releasing

## Automatic release flow
1. Merge Conventional Commit history into `main`.
2. `release.yml` runs `semantic-release version` and `semantic-release publish`.
3. Semantic-release updates `CHANGELOG.md` and creates git tag `vX.Y.Z`.
4. Tag triggers `build.yml` to produce Linux/Windows binaries.
5. `build.yml` creates GitHub Release and attaches generated artifacts.

## Manual override
- Inspect prospective version with `semantic-release version --print`.
- For emergency patching, merge a `fix:` commit into `main` and rerun release workflow.
