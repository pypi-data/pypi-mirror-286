# file_processor_sdk/process_txt.py
def process_txt(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()