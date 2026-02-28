from __future__ import annotations

import argparse
import json
from pathlib import Path

from plumbing_takeoff.pdf_pipeline import detect_page_mode, extract_text_by_page
from plumbing_takeoff.takeoff import export_bundle, extract_bom_from_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Plumbing Takeoff MVP CLI")
    parser.add_argument("pdf", type=Path, help="Path to source PDF")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"), help="Output directory")
    return parser


def run_takeoff(pdf_path: Path, output_dir: Path) -> dict[str, str]:
    mode = detect_page_mode(str(pdf_path))
    text_by_page = extract_text_by_page(str(pdf_path))
    report = extract_bom_from_text(text_by_page, source_file=pdf_path.name, extraction_mode=mode)
    artifacts = export_bundle(report, output_dir)
    return {k: str(v) for k, v in artifacts.items()}


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.pdf.exists():
        print(json.dumps({"error": f"PDF not found: {args.pdf}"}, indent=2))
        return 2

    try:
        artifacts = run_takeoff(args.pdf, args.output_dir)
    except ImportError as exc:
        print(json.dumps({"error": f"Missing runtime dependency: {exc}"}, indent=2))
        return 3

    print(json.dumps(artifacts, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
