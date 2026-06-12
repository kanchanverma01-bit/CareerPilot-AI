import streamlit as st
from pypdf import PdfReader
from dotenv import load_dotenv
from ai_service import get_ai_response

import pytesseract
from pdf2image import convert_from_bytes
from streamlit_mic_recorder import mic_recorder
from docx import Document

load_dotenv()

# ---------------- TESSERACT PATH ----------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide"
)

# ---------------- UI ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

h1 { color: #38bdf8; text-align: center; }

.stButton > button {
    background: linear-gradient(90deg, #2563eb, #38bdf8);
    color: white;
    border-radius: 10px;
    width: 100%;
}

.box {
    background-color: #1e293b;
    padding: 15px;
    border-radius: 10px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "resume" not in st.session_state:
    st.session_state.resume = ""

if "question" not in st.session_state:
    st.session_state.question = ""

if "step" not in st.session_state:
    st.session_state.step = 0

if "answer" not in st.session_state:
    st.session_state.answer = ""

# ---------------- DOCX READER ----------------
def extract_docx(file):
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

# ---------------- TITLE ----------------
st.title("🚀 CareerPilot AI")
st.subheader("AI Mock Interview Platform")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload Resume (PDF / DOCX / TXT)",
    type=["pdf", "docx", "txt"]
)

text = ""

if uploaded_file:

    file_type = uploaded_file.name.split(".")[-1].lower()

    # ---------------- TXT ----------------
    if file_type == "txt":
        text = uploaded_file.read().decode("utf-8")

    # ---------------- DOCX ----------------
    elif file_type == "docx":
        text = extract_docx(uploaded_file)

    # ---------------- PDF ----------------
    elif file_type == "pdf":

        uploaded_file.seek(0)

        try:
            pdf = PdfReader(uploaded_file)

            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

        except Exception as e:
            st.warning(f"PDF read error: {e}")

        # 🔥 FORCE OCR IF TEXT IS WEAK (FIXED LOGIC)
        if len(text.strip()) < 100:

            st.info("🔄 Scanned PDF detected → Using OCR...")

            try:
                uploaded_file.seek(0)
                images = convert_from_bytes(uploaded_file.read())

                for img in images:
                    text += pytesseract.image_to_string(img)

            except Exception as e:
                st.error(f"OCR Error: {e}")

    # ---------------- RESULT ----------------
    if len(text.strip()) == 0:
        st.error("❌ Could not extract text from resume")
    else:
        st.session_state.resume = text

        st.success("✅ Resume Loaded Successfully")

        st.text_area("Extracted Resume Text", text, height=250)

# ---------------- START INTERVIEW ----------------
if st.session_state.resume:

    level = st.selectbox("Select Difficulty Level", ["Easy", "Medium", "Hard"])

    if st.button("🚀 Start Interview") and st.session_state.step == 0:

        with st.spinner("Generating Question..."):

            prompt = f"""
You are a FAANG interviewer.

Based on this resume, ask ONE {level} level technical interview question.

Resume:
{st.session_state.resume}
"""

            try:
                st.session_state.question = get_ai_response(prompt)
                st.session_state.step = 1
            except Exception as e:
                st.error(f"AI Error: {e}")

# ---------------- QUESTION ----------------
if st.session_state.step >= 1:

    st.markdown(f"""
    <div class="box">
        <h3>🧠 Interview Question</h3>
        <p>{st.session_state.question}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ✍️ Answer Mode")

    mode = st.radio("Choose Mode:", ["Type", "Voice", "Both"])

    answer = ""

    # -------- TYPE --------
    if mode == "Type":
        answer = st.text_area("Write your answer")

    # -------- VOICE --------
    elif mode == "Voice":
        audio = mic_recorder(
            start_prompt="🎤 Start Recording",
            stop_prompt="⏹ Stop Recording",
            key="mic1"
        )

        if audio:
            st.audio(audio["bytes"])
            answer = "VOICE ANSWER (speech-to-text upgrade pending)"

    # -------- BOTH --------
    elif mode == "Both":
        text_ans = st.text_area("Write your answer")

        audio = mic_recorder(
            start_prompt="🎤 Start Recording",
            stop_prompt="⏹ Stop Recording",
            key="mic2"
        )

        answer = text_ans if text_ans else "VOICE ANSWER"

# ---------------- SUBMIT ----------------
if st.session_state.step == 1:

    if st.button("📊 Submit Answer"):

        if not answer:
            st.warning("Please provide an answer")
        else:

            with st.spinner("Evaluating..."):

                prompt = f"""
Question:
{st.session_state.question}

Answer:
{answer}

Give:
1. Score out of 10
2. Mistakes
3. Improved Answer
"""

                try:
                    result = get_ai_response(prompt)

                    st.markdown(f"""
                    <div class="box">
                        <h3>📊 Result</h3>
                        <p>{result}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    st.session_state.step = 2

                except Exception as e:
                    st.error(f"Evaluation Error: {e}")