from __future__ import annotations

import csv
from pathlib import Path

from plumbing_takeoff.models import BoMReport


def _rows(report: BoMReport) -> list[dict]:
    return [item.model_dump() for item in report.items]


def export_csv(report: BoMReport, path: str | Path) -> Path:
    p = Path(path)
    rows = _rows(report)
    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["item_name"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return p


def export_xlsx(report: BoMReport, path: str | Path) -> Path:
    p = Path(path)
    try:
        from openpyxl import Workbook
    except ImportError:  # pragma: no cover
        # constrained fallback for local smoke environments
        return export_csv(report, p)

    rows = _rows(report)
    wb = Workbook()
    ws = wb.active
    ws.title = "BoM"

    if rows:
        headers = list(rows[0].keys())
        ws.append(headers)
        for row in rows:
            ws.append([row[h] for h in headers])
    else:
        ws.append(["item_name"])

    wb.save(p)
    return p


def export_json_report(report: BoMReport, path: str | Path) -> Path:
    p = Path(path)
    p.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    return p


def export_markdown_summary(report: BoMReport, path: str | Path) -> Path:
    p = Path(path)
    lines = ["# Plumbing BoM Summary", "", f"Source: `{report.source_file}`", ""]
    for item in report.items:
        lines.append(
            f"- **{item.item_name}** ({item.category}, {item.size}) x {item.quantity} "
            f"[confidence={item.confidence_score}]"
        )
    p.write_text("\n".join(lines), encoding="utf-8")
    return p
