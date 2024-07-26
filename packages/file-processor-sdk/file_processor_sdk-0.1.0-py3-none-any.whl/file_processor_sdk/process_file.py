# file_processor_sdk/process_file.py
from .process_pdf import process_pdf
from .process_docx import process_docx
from .process_doc import process_doc
from .process_txt import process_txt
from .save_to_txt import save_to_txt
import os

def process_file(file_path: str, save_dir: str) -> str:
    _, file_extension = os.path.splitext(file_path)
    save_path = os.path.join(save_dir, os.path.basename(file_path) + '.txt')

    if file_extension.lower() == '.pdf':
        content = '\n'.join(process_pdf(file_path))
    elif file_extension.lower() == '.docx':
        content = process_docx(file_path)
    elif file_extension.lower() == '.doc':
        content = process_doc(file_path)
    elif file_extension.lower() == '.txt':
        content = process_txt(file_path)
    else:
        raise ValueError(f"不支持的文件类型: {file_extension}")

    save_to_txt(content, save_path)
    return save_path