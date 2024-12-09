import google.generativeai as genai
from config import API_KEY
import PyPDF2

def generate_content_from_input(input_data, input_type="prompt", language='en'):
    
    if input_type == "prompt":
        return generate_content_from_prompt(input_data, language)
    elif input_type == "pdf":
        return generate_content_from_pdf(input_data)
    else:
        raise ValueError("Invalid input_type. Choose 'prompt' or 'pdf'.")


def generate_content_from_prompt(prompt, language='en'):
    genai.configure(api_key=API_KEY)
    if language != 'en':
        prompt = prompt + f" in {language}"
    
    structured_prompt = f"""
    Please generate a PowerPoint presentation based on the following topic: {prompt}
    The presentation should contain no more than 5 slides.
    For each slide, provide a title, text, and optional image in the following format:

    slide_X:
        title: [Title of slide X]
        text: [Text content for slide X]
        image: [Optional image URL or "None" if no image]
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(structured_prompt)

    print("Response from Gemini AI:", response)

    if isinstance(response.candidates[0].content, str):
        generated_text = response.candidates[0].content.parts[0].text
    else:
        generated_text = str(response.candidates[0].content.parts[0].text)

    return parse_generated_content(generated_text)


def generate_content_from_pdf(pdf_path):
  
    pdf_text = extract_text_from_pdf(pdf_path)
    
    structured_prompt = f"""
    Please generate a PowerPoint presentation based on the following content extracted from a PDF:
    {pdf_text}
    The presentation should contain no more than 5 slides.
    For each slide, provide a title, text, and optional image in the following format:

    slide_X:
        title: [Title of slide X]
        text: [Text content for slide X]
        image: [Optional image URL or "None" if no image]
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(structured_prompt)

    print("Response from Gemini AI:", response)

    if isinstance(response.candidates[0].content, str):
        generated_text = response.candidates[0].content.parts[0].text
    else:
        generated_text = str(response.candidates[0].content.parts[0].text)

    return parse_generated_content(generated_text)


def extract_text_from_pdf(pdf_path):
    
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text


def parse_generated_content(generated_text):
   
    slides_dict = {}
    slides_lines = generated_text.strip().split('\n')
    current_slide = None
    slide_data = {}

    for line in slides_lines:
        line = line.strip()
        if line.startswith('slide_'):
            if current_slide:
                slides_dict[current_slide] = slide_data
            current_slide = line.split(':')[0]
            slide_data = {}
        elif ':' in line:
            try:
                key, value = line.split(':', 1)
                slide_data[key.strip()] = value.strip()
            except ValueError:
                print(f"Skipping invalid line: {line}")
        else:
            print(f"Skipping line without ':' separator: {line}")

    if current_slide:
        slides_dict[current_slide] = slide_data

    print(slides_dict)
    return slides_dict
