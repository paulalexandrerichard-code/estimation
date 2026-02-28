import json
from pathlib import Path

import plumbing_takeoff.cli as cli
from plumbing_takeoff.takeoff import export_bundle, extract_bom_from_text


def test_extract_bom_from_text_aggregates_items():
    report = extract_bom_from_text(
        {
            1: "2x wc\n3 x 50 mm pipe",
            2: "1x sink\n4x floor drain\n2 x 50 mm pipe",
        },
        source_file="sample.pdf",
        extraction_mode="vector",
    )
    payload = report.model_dump()
    names = {item["item_name"]: item for item in payload["items"]}
    assert names["WC"]["quantity"] == 2
    assert names["Sink"]["quantity"] == 1
    assert names["Floor Drain"]["quantity"] == 4
    assert names["Pipe"]["quantity"] == 5


def test_export_bundle_outputs_files(tmp_path: Path):
    report = extract_bom_from_text({1: "2x wc"}, "sample.pdf", "vector")
    bundle = export_bundle(report, tmp_path)
    assert set(bundle.keys()) == {"csv", "xlsx", "json", "markdown"}
    assert all(path.exists() for path in bundle.values())


def test_cli_main_with_monkeypatched_pdf(monkeypatch, tmp_path: Path, capsys):
    pdf_path = tmp_path / "plan.pdf"
    pdf_path.write_text("placeholder", encoding="utf-8")

    monkeypatch.setattr(cli, "run_takeoff", lambda _pdf, _out: {"json": str(tmp_path / "out.json")})
    (tmp_path / "out.json").write_text("{}", encoding="utf-8")

    exit_code = cli.main([str(pdf_path), "--output-dir", str(tmp_path / "out")])
    assert exit_code == 0
    output = capsys.readouterr().out
    payload = json.loads(output)
    assert Path(payload["json"]).exists()


def test_cli_main_missing_pdf(capsys):
    exit_code = cli.main(["missing.pdf"])
    assert exit_code == 2
    assert "PDF not found" in capsys.readouterr().out


def test_cli_main_missing_dependency(monkeypatch, tmp_path: Path, capsys):
    pdf_path = tmp_path / "plan.pdf"
    pdf_path.write_text("placeholder", encoding="utf-8")

    def _raise(_pdf, _out):
        raise ImportError("fitz")

    monkeypatch.setattr(cli, "run_takeoff", _raise)
    exit_code = cli.main([str(pdf_path)])
    assert exit_code == 3
    assert "Missing runtime dependency" in capsys.readouterr().out
