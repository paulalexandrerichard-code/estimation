from __future__ import annotations

import re
from pathlib import Path

from plumbing_takeoff.exports import (
    export_csv,
    export_json_report,
    export_markdown_summary,
    export_xlsx,
)
from plumbing_takeoff.models import BoMItem, BoMReport

_FIXTURE_KEYWORDS = {
    "wc": "WC",
    "water closet": "Water Closet",
    "sink": "Sink",
    "lav": "Lavatory",
    "urinal": "Urinal",
    "floor drain": "Floor Drain",
}

_PIPE_PATTERN = re.compile(
    r"(?P<qty>\d+(?:\.\d+)?)\s*(?:x|×)?\s*(?P<size>\d+(?:\.\d+)?)\s*(?:mm|in|\")\s*pipe",
    re.IGNORECASE,
)
_GENERIC_COUNT_PATTERN = re.compile(
    r"(?P<qty>\d+(?:\.\d+)?)\s*(?:x|×)\s*(?P<name>[a-z][a-z\s\-]+)", re.IGNORECASE
)


def _normalize(name: str) -> str:
    cleaned = re.sub(r"\s+", " ", name.strip())
    return cleaned.title()


def extract_bom_from_text(
    text_by_page: dict[int, str], source_file: str, extraction_mode: str
) -> BoMReport:
    grouped: dict[tuple[str, str, str], BoMItem] = {}

    for page, text in text_by_page.items():
        lower_text = text.lower()

        for match in _PIPE_PATTERN.finditer(text):
            qty = float(match.group("qty"))
            size = match.group("size")
            key = ("Pipe", "pipe", size)
            if key not in grouped:
                grouped[key] = BoMItem(
                    item_name="Pipe",
                    category="pipe",
                    size=size,
                    quantity=0,
                    page_numbers=[],
                    evidence_snippets=[],
                    confidence_score=0.8,
                )
            item = grouped[key]
            item.quantity += qty
            item.page_numbers.append(page)
            item.evidence_snippets.append(match.group(0))

        for keyword, canonical_name in _FIXTURE_KEYWORDS.items():
            fixture_hits = re.findall(
                rf"(\d+(?:\.\d+)?)\s*(?:x|×)\s*{re.escape(keyword)}", lower_text
            )
            for raw_qty in fixture_hits:
                qty = float(raw_qty)
                key = (canonical_name, "fixture", "N/A")
                if key not in grouped:
                    grouped[key] = BoMItem(
                        item_name=canonical_name,
                        category="fixture",
                        size="N/A",
                        quantity=0,
                        page_numbers=[],
                        evidence_snippets=[],
                        confidence_score=0.9,
                    )
                item = grouped[key]
                item.quantity += qty
                item.page_numbers.append(page)
                item.evidence_snippets.append(f"{raw_qty}x {keyword}")

        for match in _GENERIC_COUNT_PATTERN.finditer(text):
            name = _normalize(match.group("name"))
            if any(name.lower().startswith(k) for k in _FIXTURE_KEYWORDS):
                continue
            qty = float(match.group("qty"))
            key = (name, "other", "N/A")
            if key not in grouped:
                grouped[key] = BoMItem(
                    item_name=name,
                    category="other",
                    size="N/A",
                    quantity=0,
                    page_numbers=[],
                    evidence_snippets=[],
                    confidence_score=0.6,
                )
            item = grouped[key]
            item.quantity += qty
            item.page_numbers.append(page)
            item.evidence_snippets.append(match.group(0))

    items = list(grouped.values())
    for item in items:
        item.page_numbers = sorted(set(item.page_numbers))

    return BoMReport(source_file=source_file, extraction_mode=extraction_mode, items=items)


def export_bundle(report: BoMReport, output_dir: str | Path) -> dict[str, Path]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    stem = Path(report.source_file).stem
    return {
        "csv": export_csv(report, out / f"{stem}_bom.csv"),
        "xlsx": export_xlsx(report, out / f"{stem}_bom.xlsx"),
        "json": export_json_report(report, out / f"{stem}_bom.json"),
        "markdown": export_markdown_summary(report, out / f"{stem}_summary.md"),
    }
