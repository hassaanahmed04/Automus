import os

def save_uploaded_file(uploaded_file, save_path):
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

def get_ppt_filename():
    return "generated_presentation.pptx"
