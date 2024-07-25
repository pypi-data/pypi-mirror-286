"""
Utility functions for password-protecting PDFs.

This module provides functions for reading PDF files, adding password protection,
and checking password validity.
"""

from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from secure_pdf.settings import settings

def read_file(file) -> PdfReader:
    """
    Reads a PDF file and returns a PyPDF2 PdfReader object.

    Args:
        file: The PDF file to read.

    Returns:
        PdfReader: A PyPDF2 PdfReader object representing the PDF file.
    """
    pdf_reader = PdfReader(file)
    return pdf_reader

def check_password(password: str, max_len: int = 5) -> tuple[bool, str]:
    """
    Checks the validity of a password.

    Args:
        password (str): The password to check.
        max_len (int, optional): The minimum length of the password. Defaults to 5.

    Returns:
        tuple[bool, str]: A tuple containing a boolean indicating password validity
            and a string with an error message or the password itself.
    """
    decline_msg = f"Password should be Equal or Greater than {max_len}"
    if len(password.strip()) >= max_len:
        return True, password
    elif password.strip() is None or password.strip()=="":
        return True, settings.default_password
    else:
        return False, decline_msg

def add_password(pdf_reader: PdfReader, password: str = settings.default_password) -> BytesIO | str:
    """
    Adds password protection to a PDF file.

    Args:
        pdf_reader (PdfReader): The PyPDF2 PdfReader object representing the PDF file.
        password (str, optional): The password to add to the PDF file. Defaults to "IQA".

    Returns:
        BytesIO | str: The password-protected PDF file as a BytesIO object, or an error message as a string.
    """
    try:
        pdf_writer = PdfWriter()
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])
        pdf_writer.encrypt(password)
        pdf_bytes = BytesIO()
        pdf_writer.write(pdf_bytes)
        pdf_bytes.seek(0)
    except Exception as e:
        pdf_bytes = f"Unable to process, error occur due to {e}"
    return pdf_bytes