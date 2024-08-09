import os
from typing import BinaryIO
from fastapi import UploadFile
from io import BytesIO
from docx import Document
import fitz  # PyMuPDF

def read_file(upload_file: UploadFile) -> str:
    """
    Read content from a file stream based on its extension.

    Args:
        upload_file (UploadFile): The uploaded file object.

    Returns:
        str: The text content of the file.

    Raises:
        ValueError: If the file type is unsupported.
    """
    # Get the file extension from the UploadFile object
    _, file_extension = os.path.splitext(upload_file.filename)

    # Convert the SpooledTemporaryFile to BytesIO if needed
    file_content = BytesIO(upload_file.file.read())
    upload_file.file.seek(0)  # Reset file pointer after reading

    if file_extension.lower() == '.txt':
        return read_txt(file_content)

    elif file_extension.lower() == '.docx':
        return read_docx(file_content)

    elif file_extension.lower() == '.pdf':
        return read_pdf(file_content)

    else:
        raise ValueError(f"Unsupported file extension: {file_extension}")

def read_txt(file: BinaryIO) -> str:
    file.seek(0)
    return file.read().decode('utf-8')

def read_docx(file: BinaryIO) -> str:
    file.seek(0)
    document = Document(file)
    full_text = [paragraph.text for paragraph in document.paragraphs]
    return '\n'.join(full_text)

def read_pdf(file: BinaryIO) -> str:
    file.seek(0)
    document = fitz.open(stream=file.read(), filetype='pdf')
    all_text = [page.get_text() for page in document]
    document.close()  # Ensure the document is closed after processing
    return '\n'.join(all_text)


# from typing import BinaryIO
# from fastapi import UploadFile
# from docx import Document
# import fitz
# import os

# def read_file(file: UploadFile) -> str:
#     """
#     Read content from a file stream based on its extension.

#     Args:
#         file (UploadFile): The uploaded file object.

#     Returns:
#         str: The text content of the file.

#     Raises:
#         ValueError: If the file type is unsupported.
#     """
#     # Get the file extension
#     _, file_extension = os.path.splitext(file.filename)

#     if file_extension.lower() == '.txt':
#         return read_txt(file.file)

#     elif file_extension.lower() == '.docx':
#         return read_docx(file.file)

#     elif file_extension.lower() == '.pdf':
#         return read_pdf(file.file)

#     else:
#         raise ValueError(f"Unsupported file extension: {file_extension}")

# def read_txt(file: BinaryIO) -> str:
#     file.seek(0)
#     return file.read().decode('utf-8')

# def read_docx(file: BinaryIO) -> str:
#     file.seek(0)
#     document = Document(file)
#     full_text = [paragraph.text for paragraph in document.paragraphs]
#     return '\n'.join(full_text)

# def read_pdf(file: BinaryIO) -> str:
#     file.seek(0)
#     document = fitz.open(stream=file.read(), filetype='pdf')
#     all_text = [page.get_text() for page in document]
#     return '\n'.join(all_text)



# import os
# import fitz  # PyMuPDF
# from docx import Document

# def read_file(file_path: str) -> str:
#     """
#     Read content from a file based on its extension.

#     Args:
#         file_path (str): The path to the file to be read.

#     Returns:
#         str: The text content of the file.

#     Raises:
#         FileNotFoundError: If the file does not exist.
#         ValueError: If the file type is unsupported.
#     """
#     # Check if file exists
#     if not os.path.isfile(file_path):
#         raise FileNotFoundError(f"The file {file_path} does not exist.")

#     # Get the file extension
#     _, file_extension = os.path.splitext(file_path)

#     if file_extension.lower() == '.txt':
#         return read_txt(file_path)

#     elif file_extension.lower() == '.docx':
#         return read_docx(file_path)

#     elif file_extension.lower() == '.pdf':
#         return read_pdf(file_path)

#     else:
#         raise ValueError(f"Unsupported file extension: {file_extension}")

# def read_txt(file_path: str) -> str:
#     with open(file_path, 'r', encoding='utf-8') as file:
#         return file.read()

# def read_docx(file_path: str) -> str:
#     document = Document(file_path)
#     full_text = [paragraph.text for paragraph in document.paragraphs]
#     return '\n'.join(full_text)

# def read_pdf(file_path: str) -> str:
#     document = fitz.open(file_path)
#     all_text = [page.get_text() for page in document]
#     return '\n'.join(all_text)

# if __name__ == "__main__":
#     file_path = 'sample.txt'
#     text = read_file(file_path)
#     print(text[:10])
