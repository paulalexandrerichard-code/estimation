from __future__ import annotations

import json
from typing import Any

from plumbing_takeoff.models import BoMReport

try:
    from pydantic import ValidationError
except ImportError:  # pragma: no cover
    ValidationError = ValueError  # type: ignore[assignment]

DEFAULT_MODEL = "arcee-ai/trinity-large-preview:free"


def _prompt_schema() -> str:
    return (
        "Return JSON with keys: source_file, extraction_mode, items. "
        "Each item has item_name, category, size, quantity, page_numbers, "
        "evidence_snippets, confidence_score. Never invent unknown quantities."
    )


def _openai_client(api_key: str):
    from openai import OpenAI

    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)


def extract_bom_with_llm(
    text_by_page: dict[int, str],
    source_file: str,
    api_key: str,
    model: str = DEFAULT_MODEL,
) -> BoMReport:
    client = _openai_client(api_key)
    payload = {"source_file": source_file, "pages": text_by_page}
    attempts = 0
    last_error: Exception | None = None

    while attempts < 2:
        attempts += 1
        try:
            response = client.chat.completions.create(
                model=model,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": _prompt_schema()},
                    {"role": "user", "content": json.dumps(payload)},
                ],
            )
            content = response.choices[0].message.content or "{}"
            parsed: Any = json.loads(content)
            return BoMReport.model_validate(parsed)
        except (json.JSONDecodeError, ValidationError, KeyError, IndexError, TypeError) as exc:
            last_error = exc
    raise ValueError(f"Could not validate model JSON output after retry: {last_error}")
