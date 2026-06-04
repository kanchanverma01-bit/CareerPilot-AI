import streamlit as st

st.set_page_config(page_title="CareerPilot AI", page_icon="🚀")

st.title("🚀 CareerPilot AI")
st.subheader("AI Interview Preparation Platform")

st.write("Upload your resume and prepare for interviews with AI.")

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

if uploaded_file:
    st.success("Resume uploaded successfully!")