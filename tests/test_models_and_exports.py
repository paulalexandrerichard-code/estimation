from pathlib import Path

from plumbing_takeoff.exports import (
    export_csv,
    export_json_report,
    export_markdown_summary,
    export_xlsx,
)
from plumbing_takeoff.models import BoMItem, BoMReport


def sample_report() -> BoMReport:
    return BoMReport(
        source_file="plan.pdf",
        extraction_mode="vector",
        items=[
            BoMItem(
                item_name="WC",
                category="fixture",
                size="N/A",
                quantity=2,
                page_numbers=[1],
                evidence_snippets=["2x WC"],
                confidence_score=0.9,
            )
        ],
    )


def test_exports(tmp_path: Path):
    report = sample_report()
    assert export_csv(report, tmp_path / "out.csv").exists()
    assert export_xlsx(report, tmp_path / "out.xlsx").exists()
    assert export_json_report(report, tmp_path / "out.json").exists()
    md = export_markdown_summary(report, tmp_path / "out.md")
    assert "WC" in md.read_text(encoding="utf-8")


def test_model_dump_contains_items():
    payload = sample_report().model_dump()
    assert payload["items"][0]["item_name"] == "WC"
