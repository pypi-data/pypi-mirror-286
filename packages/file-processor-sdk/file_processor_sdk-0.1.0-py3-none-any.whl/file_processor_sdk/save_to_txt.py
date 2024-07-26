# file_processor_sdk/save_to_txt.py
def save_to_txt(content: str, save_path: str):
    with open(save_path, 'w', encoding='utf-8') as file:
        file.write(content)