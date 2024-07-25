import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
import subprocess

from pass_prot_pdf.settings import settings,server_settings
from pass_prot_pdf.utils import read_file, add_password, check_password


def main():
    """
    Main entry point for the application.

    This function sets up the Streamlit app, handles file uploads and password input,
    and provides a download button for the password-protected PDF.
    """
    st.title(settings.title)
    uploaded_file: UploadedFile | None = st.file_uploader(settings.upload_msg, type=settings.allowed)

    if uploaded_file is not None:
        temp_file_name = uploaded_file.name
        st.write("Filename:", temp_file_name)
        st.write("File type:", uploaded_file.type)
        st.write("File size:", uploaded_file.size, "bytes")

        with st.spinner('Processing your file...'):
            try:
                pdf_reader = read_file(uploaded_file)
                st.write(settings.password_suggestion_msg+" "+"**"+settings.default_password+"**")
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

if __name__ == "__main__":
    main()
