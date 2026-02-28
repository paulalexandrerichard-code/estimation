# Workflows (ATLAS)

## Runtime data flow
1. Ingest PDF and detect page mode (vector/scanned/mixed).
2. Extract page text with evidence snippets.
3. Send structured prompt to OpenRouter model.
4. Validate response with Pydantic BoM contracts.
5. Retry once on invalid JSON.
6. Export final BoM to CSV/XLSX/JSON/Markdown.
7. CLI execution path available via `python -m plumbing_takeoff.cli <pdf> --output-dir <dir>`.

## Delivery flow
1. PRs to `develop`/`main` run commitlint + quality checks (ruff, black, pytest+coverage).
2. Merges to `main` trigger semantic-release for versioning/tagging/changelog.
3. New `v*.*.*` tags trigger cross-platform binary build and GitHub release publication.
