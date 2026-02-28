from __future__ import annotations


def _fitz():
    import fitz

    return fitz


def detect_page_mode(pdf_path: str) -> str:
    fitz = _fitz()
    doc = fitz.open(pdf_path)
    vector_pages = 0
    scanned_pages = 0
    for page in doc:
        text = page.get_text("text").strip()
        if text:
            vector_pages += 1
        else:
            scanned_pages += 1
    if vector_pages and scanned_pages:
        return "mixed"
    return "vector" if vector_pages else "scanned"


def extract_text_by_page(pdf_path: str) -> dict[int, str]:
    fitz = _fitz()
    doc = fitz.open(pdf_path)
    return {idx + 1: page.get_text("text") for idx, page in enumerate(doc)}
