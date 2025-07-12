import fitz  

def load_pdf(filepath: str) -> str:
    text = ""
    with fitz.open(filepath) as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

def load_pdf_by_paragraph(filepath: str) -> list[str]:
    full_text = load_pdf(filepath)
    # 연속 줄바꿈을 기준으로 분리
    import re
    paragraphs = re.split(r'\n\s*\n', full_text)
    return [p.strip() for p in paragraphs if p.strip()]