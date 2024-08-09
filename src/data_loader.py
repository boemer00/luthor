import os
import fitz  # PyMuPDF
from docx import Document

def read_file(file_path: str) -> str:
    """
    Read content from a file based on its extension.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        str: The text content of the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file type is unsupported.
    """
    # Check if file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    # Get the file extension
    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() == '.txt':
        return read_txt(file_path)

    elif file_extension.lower() == '.docx':
        return read_docx(file_path)

    elif file_extension.lower() == '.pdf':
        return read_pdf(file_path)

    else:
        raise ValueError(f"Unsupported file extension: {file_extension}")

def read_txt(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_docx(file_path: str) -> str:
    document = Document(file_path)
    full_text = [paragraph.text for paragraph in document.paragraphs]
    return '\n'.join(full_text)

def read_pdf(file_path: str) -> str:
    document = fitz.open(file_path)
    all_text = [page.get_text() for page in document]
    return '\n'.join(all_text)

if __name__ == "__main__":
    file_path = 'sample.txt'
    text = read_file(file_path)
    print(text[:10])
