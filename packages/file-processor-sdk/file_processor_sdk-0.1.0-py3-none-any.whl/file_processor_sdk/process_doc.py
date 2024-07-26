# file_processor_sdk/process_doc.py
import win32com.client as win32
def process_doc(file_path: str) -> str:
    # 启动Word应用程序
    word = win32.gencache.EnsureDispatch('Word.Application')
    # 打开.doc文件
    doc = word.Documents.Open(file_path)
    # 读取文件内容
    content = doc.Range().Text
    # 关闭Word文档
    doc.Close()
    # 退出Word应用程序
    word.Quit()
    return content