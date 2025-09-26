import streamlit as st
import PyPDF2
import io
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Resume Analyzer", layout="centered")
st.title("Resume Analyzer")
st.markdown("Upload your resume and get insights!")
Gemini_API_KEY = os.getenv("Gemini_API_KEY")
uploaded_file = st.file_uploader("Upload your resume (PDF or TXT )", type=["pdf","txt"])
job_role = st.text_input("Enter the job role you are targeting for (Optional):")
analyze = st.button("Analyze Resume")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    
    return uploaded_file.read().decode("utf-8")
genai.configure(api_key=Gemini_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")
if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)
        if not file_content.strip():
            st.error("The uploaded file is empty or could not be read. Please upload a valid PDF or TXT file.")
            st.stop()
        prompt = f"""Please analyze this resume and provide constructive feedback.
        Focus on Followig aspects:
        1. Content Clarity and impact
        2.Skills presentation
        3.Experience descriptions
        4.Specfic improvements for {job_role if job_role else 'general job applications'}

        Resume content:
        {file_content}

        Please provide your analysis in aclear, structures format with specific recommenations for improvement."""
        
        response = model.generate_content(prompt)
        st.markdown("### Analysis Results")
        st.write(response.text)
    except Exception as e:
        st.error(f"An error occurred: {e}")


