from PyPDF2 import PdfReader
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
from io import BytesIO

from secure_pdf.settings import settings, server_settings
from secure_pdf.utils import read_file, add_password, check_password, remove_password

def provide_file_info():
    """
    Provides information about the uploaded file.

    Returns:
        tuple: A tuple containing the uploaded file and its temporary file name.
    """
    uploaded_file: UploadedFile | None = st.file_uploader(settings.upload_msg, type=settings.allowed)
    temp_file_name = ""
    if uploaded_file is not None:
        temp_file_name = uploaded_file.name
        st.write("Filename:", temp_file_name)
        st.write("File type:", uploaded_file.type)
        st.write("File size:", uploaded_file.size, "bytes")
    return uploaded_file, temp_file_name

def main():
    """
    Main entry point for the application.

    This function sets up the Streamlit app, handles file uploads and password input,
    and provides a download button for the password-protected PDF.

    Returns:
        None
    """
    st.title(settings.title)
    option = st.radio("Please select", ["Add a Password", "Remove a Password"])
    if option == "Add a Password":
        """
        Adds a password to the uploaded PDF file.

        This section of the app allows users to upload a PDF file, enter a password,
        and download the password-protected PDF file.
        """
        uploaded_file, temp_file_name = provide_file_info()
        if temp_file_name:
            with st.spinner('Processing your file...'):
                try:
                    pdf_reader = read_file(uploaded_file)
                    st.write(settings.password_suggestion_msg + " " + "**" + settings.default_password + "**")
                    password: str | None = st.text_input(settings.password_input_msg, type="password")
                    pass_status, password = check_password(password=password)

                    if password and pass_status:
                        new_file = add_password(pdf_reader=pdf_reader, password=password)
                        if isinstance(new_file, str):
                            st.text_area(label="Error", value=new_file, height=150, disabled=True)
                        else:
                            st.download_button(label=settings.download_file_msg,
                                               data=new_file,
                                               file_name=temp_file_name,
                                               mime=settings.application_type)
                    elif pass_status is False:
                        st.write(password)
                    else:
                        st.write(settings.password_suggestion_msg)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.write(settings.no_file_msg)
    elif option == "Remove a Password":
        """
        Removes the password from the uploaded PDF file.

        This section of the app allows users to upload a PDF file, enter the password,
        and download the PDF file without the password.
        """
        uploaded_file, temp_file_name = provide_file_info()
        if temp_file_name:
            with st.spinner('Processing your file...'):
                try:
                    pdf_reader: PdfReader = read_file(uploaded_file)
                    st.write(settings.password_decrypt_suggestion_msg)
                    password: str | None = st.text_input(settings.password_input_msg, type="password")
                    pass_status, password = check_password(password=password, decrypt=True)
                    if password and pass_status:
                        new_file, password_check = remove_password(pdf_reader=pdf_reader, password=password)
                        if isinstance(new_file, str):
                            st.text_area(label="Error", value=new_file, height=150, disabled=True)
                        elif password_check:
                            st.text_area(label="No password available for PDF", value=new_file, height=150, disabled=True)
                        else:
                            st.download_button(label=settings.download_file_msg,
                                               data=new_file,
                                               file_name=temp_file_name,
                                               mime=settings.application_type)
                    elif pass_status is False:
                        st.write(password)
                    else:
                        st.write(settings.password_decrypt_suggestion_msg)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        st.write("Welcome")

if __name__ == "__main__":
    main()