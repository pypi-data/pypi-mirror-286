from setuptools import setup, find_packages

setup(
    name='file_processor_sdk',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'python-docx',
        'PyPDF2',  # 假设你使用PyPDF2来处理PDF，而不是langchain
        'pywin32',  # 用于处理.doc文件
    ],
    entry_points={
        'console_scripts': [
            'process_files=file_processor_sdk.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
