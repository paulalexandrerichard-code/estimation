# Security

- No API keys in repository.
- API key is entered by user at runtime via masked UI field.
- `.env` not required.
- Validation through Pydantic + JSON schema.
- CI secret scanning should be enabled in GitHub Advanced Security/secret scanning.
- Keep dependencies pinned through lock process in deployment pipelines.

- GitHub Actions `security.yml` performs repository secret scanning on push/PR.
