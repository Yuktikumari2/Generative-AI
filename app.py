import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import base64

# Set the page title and icon in the browser tab
st.set_page_config(page_title="Enhance Your Resume Screening 🎯📈", page_icon="📈")

load_dotenv()  # Load environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(input)
    return response.text

# Prompt Template
input_prompt = """
Hey, act like a skilled and highly experienced ATS (Applicant Tracking System)
with a strong understanding of different industries and job roles. Your task is to evaluate the resume based on the provided job description.
Considering the competitive job market, provide the best assistance for enhancing resumes by identifying essential skills, experiences, 
and keywords that align with the job description.
Assign a percentage match based on the job description and highlight any missing keywords or skills with high accuracy.
Resume content: {text}
Job description: {jd}

Please structure the response as follows:
{{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}
"""

# Streamlit app
with st.sidebar:
    st.title("Smart ATS for CV/Resume")
    st.subheader("About")
    st.write("This Smart ATS, powered by Gemini Pro and Streamlit, brings a new level of precision to resume screening. It intelligently analyzes resumes to calculate match percentages, pinpoints missing keywords, and crafts tailored profile summaries—streamlining candidate assessment and empowering recruiters to identify top talent with speed and accuracy.")
    st.markdown("""
    - [Streamlit](https://streamlit.io/)
    - [Gemini Pro](https://deepmind.google/technologies/gemini/#introduction)
    - [Makersuite API Key](https://makersuite.google.com/)
    - [Github Repository](https://github.com/Yuktikumari2/Generative-AI)
    - [LinkedIn Profile](https://www.linkedin.com/in/yukti-kumari-146bb821b?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)
    """)
                
    add_vertical_space(5)
    st.write("Made ❤ by Yukti Kumari 7th Sem. CSE")

st.title("Smart Application Tracking System")
st.text("Enhance your resume screening with ATS 🎯📈")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume Image", type=["jpg", "jpeg", "png"], help="Please upload an image of your resume")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        # Convert the image to text using Gemini
        resume_text = get_gemini_response(image)  # Extract text from the image using Gemini model
        prompt = input_prompt.format(text=resume_text, jd=jd)
        response = get_gemini_response(prompt)
        st.subheader("ATS Analysis Result")
        st.write(response)
    else:
        st.warning("Please upload an image of your resume.")

# Setting the default background image
background_image_path = "Background.png"

with open(background_image_path, "rb") as file:
    background_image = file.read()

encoded_background_image = base64.b64encode(background_image).decode()

st.markdown(
    f"""
    <style>
    .stApp {{
        background: url(data:image/png;base64,{encoded_background_image}) no-repeat center center fixed;
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
