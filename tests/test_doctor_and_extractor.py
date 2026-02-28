import json

import plumbing_takeoff.extractor as extractor
from plumbing_takeoff.doctor import main as doctor_main
from plumbing_takeoff.doctor import run_doctor


class _Msg:
    def __init__(self, content):
        self.content = content


class _Choice:
    def __init__(self, content):
        self.message = _Msg(content)


class _Resp:
    def __init__(self, content):
        self.choices = [_Choice(content)]


class _Completions:
    def __init__(self):
        self.calls = 0

    def create(self, **kwargs):
        self.calls += 1
        if self.calls == 1:
            return _Resp("not-json")
        payload = {
            "source_file": "a.pdf",
            "extraction_mode": "vector",
            "items": [],
        }
        return _Resp(json.dumps(payload))


class _Chat:
    def __init__(self):
        self.completions = _Completions()


class _Client:
    def __init__(self):
        self.chat = _Chat()


def test_extractor_retries(monkeypatch):
    monkeypatch.setattr(extractor, "_openai_client", lambda _: _Client())
    report = extractor.extract_bom_with_llm({1: "text"}, "a.pdf", api_key="k")
    assert report.source_file == "a.pdf"


def test_doctor_returns_map():
    result = run_doctor()
    assert "pydantic" in result


def test_doctor_main_runs(capsys):
    assert doctor_main() == 0
    assert "{" in capsys.readouterr().out
