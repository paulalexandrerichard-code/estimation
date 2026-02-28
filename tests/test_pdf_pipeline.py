import plumbing_takeoff.pdf_pipeline as pipeline


class FakePage:
    def __init__(self, text):
        self._text = text

    def get_text(self, _mode):
        return self._text


class FakeDoc(list):
    pass


def test_pdf_mode_detection_and_text(monkeypatch):
    class FakeFitz:
        @staticmethod
        def open(_path):
            return FakeDoc([FakePage("1x sink")])

    monkeypatch.setattr(pipeline, "_fitz", lambda: FakeFitz)
    assert pipeline.detect_page_mode("a.pdf") == "vector"
    text_map = pipeline.extract_text_by_page("a.pdf")
    assert "sink" in text_map[1]
