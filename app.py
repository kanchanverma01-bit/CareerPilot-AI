import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")

st.set_page_config(page_title="CareerPilot AI", page_icon="🚀")

st.title("🚀 CareerPilot AI")
st.subheader("AI Interview Preparation Platform")

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

if uploaded_file:
    pdf = PdfReader(uploaded_file)

    resume_text = ""

    for page in pdf.pages:
        text = page.extract_text()
        if text:
            resume_text += text

    st.success("Resume uploaded successfully!")

    st.subheader("Resume Content")

    st.text_area(
        "Extracted Resume Text",
        resume_text,
        height=250
    )

    if st.button("Generate Interview Questions"):
        with st.spinner("Generating Questions..."):

            prompt = f"""
            Analyze the following resume and generate
            10 technical interview questions.

            Resume:
            {resume_text}
            """

            response = model.generate_content(prompt)

            st.subheader("AI Generated Interview Questions")

            st.write(response.text)