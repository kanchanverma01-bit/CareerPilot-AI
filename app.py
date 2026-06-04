import streamlit as st
from pypdf import PdfReader

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
        height=300
    )