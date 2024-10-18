import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import google.generativeai as genai
import PyPDF2 as pdf
import json
from dotenv import load_dotenv

# Load environment variables (Optional: if you still want to support external keys)
load_dotenv()

# Manually set the API key directly in the code
GOOGLE_API_KEY = 'AIzaSyCmVo3f173T0_arc-fN7QMUg7xoc2oQCX0'

# Configure Generative AI with internal API key
genai.configure(api_key=GOOGLE_API_KEY)

# Function to get response from Gemini Pro
def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

# Function to extract text from uploaded PDF file
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += str(page.extract_text())
    return text

# Prompt Template
input_prompt = """
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science, 
data analyst and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving the resumes. Assign the percentage Matching based 
on JD and the missing keywords with high accuracy.
resume:{text}
description:{jd}

I want the response as per below structure:
{{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}
"""

# Adding custom CSS for background image
def set_background(image_file_path):
    page_bg_img = f"""
    <style>
    .stApp {{
    background-image: url("file://{image_file_path}");
    background-size: cover;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Streamlit app layout
with st.sidebar:
    st.title("Smart ATS for Resumes")
    st.subheader("About")
    st.write("This sophisticated ATS project, developed with Gemini Pro and Streamlit, seamlessly incorporates advanced features including resume match percentage, keyword analysis to identify missing criteria, and the generation of comprehensive profile summaries, enhancing the efficiency and precision of the candidate evaluation process for discerning talent acquisition professionals.")
    
    st.markdown("""
    - [Streamlit](https://streamlit.io/)
    - [Gemini Pro](https://deepmind.google/technologies/gemini/#introduction)
    - [makersuit API Key](https://makersuite.google.com/)
    - [Github](https://github.com/praj2408/End-To-End-Resume-ATS-Tracking-LLM-Project-With-Google-Gemini-Pro) Repository
    """)
    
    add_vertical_space(5)
    st.write("Made ❤ by Yukti Kumari CSE 7th Semester.")

# Set a background image (replace 'path_to_image' with the actual path to the image)
set_background('path_to_your_image/background.jpg')

# Main app content
st.title("Smart Application Tracking System")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        resume_text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt.format(text=resume_text, jd=jd))
        st.subheader(response)
