# ARCHITECT (ATLAS)

Plumbing Takeoff MVP architecture:
- **UI layer**: `plumbing_takeoff.app` (PySide6).
- **Pipeline layer**: `pdf_pipeline.py` (vector/scanned detection + text extraction).
- **LLM layer**: `extractor.py` (OpenRouter via OpenAI client, strict JSON + retry once).
- **Domain layer**: `models.py` (strict Pydantic-first BoM contracts) + JSON schema.
- **Export layer**: `exports.py` (CSV, XLSX, JSON, Markdown).
- **Ops layer**: GitHub Actions CI/build/release + semantic release.
