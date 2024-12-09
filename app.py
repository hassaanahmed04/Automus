import streamlit as st
from config import LANGUAGES
from generate_content import generate_content_from_prompt, generate_content_from_pdf
from ppt_creator import create_dynamic_ppt
from io import BytesIO
import tempfile

def main():
    st.set_page_config(page_title="PowerPoint Automation Tool", page_icon=":guardsman:", layout="wide")
    
    st.markdown(
        "<h1 style='text-align: center; color: #4CAF50;'>PowerPoint Automation Tool</h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p style='text-align: center; color: #888888;'>Automate the creation of PowerPoint presentations from prompts or PDF files</p>",
        unsafe_allow_html=True,
    )

    st.write("---")

    input_method = st.radio(
        "Choose input method:",
        options=["From Prompt", "From PDF"],
        index=0,
        label_visibility="collapsed",
        help="Choose whether to generate content from a prompt or a PDF",
    )

    if input_method == "From Prompt":
        prompt = st.text_area(
            "Enter a prompt to generate content for your PowerPoint:",
            placeholder="Describe the topic for your presentation...",
            max_chars=500,
            height=150,
        )
        language = st.selectbox(
            "Select Language",
            options=list(LANGUAGES.keys()),
            index=0,
            help="Choose the language for the content",
        )
        if not prompt:
            st.warning("Please enter a prompt to generate content.")

    elif input_method == "From PDF":
        pdf_file = st.file_uploader(
            "Upload a PDF file",
            type="pdf",
            label_visibility="collapsed",
            help="Upload a PDF file from which content will be extracted",
        )
        if not pdf_file:
            st.warning("Please upload a PDF file.")

    st.write("---")
    heading_font_size = st.slider(
    "Heading Font Size",
    min_value=10,
    max_value=50,
    value=16,
    step=2,
    help="Adjust the font size of the heading in the generated PowerPoint",
    format="%d",  # Use integer format
)

    text_font_size = st.slider(
        "Text Font Size",
        min_value=8,
        max_value=40,
        value=12,
        step=2,
        help="Adjust the font size of the text in the generated PowerPoint",
        format="%d",  # Use integer format
    )

    animation = st.selectbox(
        "Choose Animation",
        options=["None", "Fade", "Slide", "Zoom"],
        index=0,
        help="Select an animation for the PowerPoint slides",
    )
    media_url = st.text_input(
        "Enter a video URL (Optional)",
        placeholder="Paste a video URL if you'd like to embed media",
    )

    st.write("---")
    generate_button = st.button(
        "Generate PowerPoint",
        help="Click to generate your PowerPoint presentation",
        use_container_width=True,
        key="generate_button",
    )

    if generate_button:
        if input_method == "From Prompt" and prompt:
            st.write("Generating content from prompt...")
            generated_content = generate_content_from_prompt(prompt, LANGUAGES[language])
            st.success("Content generated successfully!")

        elif input_method == "From PDF" and pdf_file:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_pdf:
                tmp_pdf.write(pdf_file.getbuffer())
                tmp_pdf_path = tmp_pdf.name

            st.write("Generating content from PDF...")
            generated_content = generate_content_from_pdf(tmp_pdf_path)
            st.success("Content generated successfully!")

        prs = create_dynamic_ppt(generated_content, heading_font_size, text_font_size, animation, media_url)
        pptx_filename = "generated_presentation.pptx"
        prs.save(pptx_filename)

        st.success("PowerPoint presentation created successfully!")

        with open(pptx_filename, "rb") as file:
            st.download_button(
                label="Download PowerPoint",
                data=file,
                file_name=pptx_filename,
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width=True,
                key="download_button",
            )

if __name__ == "__main__":
    main()
