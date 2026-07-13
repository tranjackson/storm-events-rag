from pypdf import PdfReader

def load_pdf_text(path: str) -> str:

    return "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)

def chunk_fixed(text: str, size: int = 1600, overlap: int = 100) -> list[str]:

    out, i = [], 0

    while i < len(text):

        out.append(text[i:i+size]); i += size - overlap

    return out

def chunk_by_heading(text: str) -> list[str]:

    import re

    # split on lines that look like numbered headings ("2.1.1 ...")

    parts = re.split(r"\n(?=\d+(\.\d+)*\s)", text)

    return [p.strip() for p in parts if p and len(p.strip()) > 50]
