# file_processor_sdk/process_docx.py
from docx import Document
def process_docx(file_path: str) -> str:
    doc = Document(file_path)
    return '\n'.join([paragraph.text for paragraph in doc.paragraphs])