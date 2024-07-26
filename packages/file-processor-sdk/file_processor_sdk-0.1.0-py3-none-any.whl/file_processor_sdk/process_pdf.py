# file_processor_sdk/process_pdf.py
from langchain.document_loaders import PyPDFLoader
from typing import List
def process_pdf(file_path: str) -> List[str]:
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    return [page.page_content for page in pages]
