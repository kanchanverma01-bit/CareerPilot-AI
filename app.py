pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import streamlit as st
from pypdf import PdfReader
from dotenv import load_dotenv
from ai_service import get_ai_response
import pytesseract
from pdf2image import convert_from_bytes
from streamlit_mic_recorder import mic_recorder
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

load_dotenv()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide"
)

# ---------------- CUSTOM UI ----------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

h1 {
    color: #38bdf8;
    text-align: center;
}

h2, h3 {
    color: #60a5fa;
}

.stButton > button {
    background: linear-gradient(90deg, #2563eb, #38bdf8);
    color: white;
    border-radius: 10px;
    border: none;
    width: 100%;
}

.question-box {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    border-left: 5px solid #38bdf8;
}

.result-box {
    background-color: #111827;
    padding: 20px;
    border-radius: 15px;
    border-left: 5px solid #22c55e;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🚀 CareerPilot AI")
st.subheader("AI Interview Platform")

# ---------------- SESSION STATE ----------------
if "resume" not in st.session_state:
    st.session_state.resume = ""

if "question" not in st.session_state:
    st.session_state.question = ""

if "step" not in st.session_state:
    st.session_state.step = 0

# ---------------- UPLOAD RESUME ----------------
uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

if uploaded_file:

    text = ""

    # Normal PDF extraction
    try:
        pdf = PdfReader(uploaded_file)

        for page in pdf.pages:
            text += page.extract_text() or ""

    except:
        pass

    # OCR fallback for scanned PDFs
    if len(text.strip()) < 50:

        uploaded_file.seek(0)

        try:
            images = convert_from_bytes(
                uploaded_file.read()
            )

            for image in images:
                text += pytesseract.image_to_string(image)

        except:
            pass

    st.write("Characters:", len(text))

    if len(text.strip()) == 0:
        st.error("Could not extract text from PDF.")
    else:

        st.session_state.resume = text

        st.success("✅ Resume Loaded Successfully")

        st.text_area(
            "Resume Text",
            text,
            height=250
        )

# ---------------- START INTERVIEW ----------------
if st.session_state.resume:

    if st.button("Start Interview 🚀"):

        with st.spinner("Generating Interview Question..."):

            prompt = f"""
            You are a FAANG interviewer.

            Based on this resume,
            ask ONLY ONE technical interview question.

            Resume:
            {st.session_state.resume}
            """

            st.session_state.question = get_ai_response(prompt)
            st.session_state.step = 1

# ---------------- SHOW QUESTION ----------------
if st.session_state.step == 1:

    st.markdown(f"""
    <div class="question-box">
    <h3>🧠 Interview Question</h3>
    <p>{st.session_state.question}</p>
    </div>
    """, unsafe_allow_html=True)

    answer = st.text_area(
        "Your Answer",
        height=200
    )
# ---------------- VOICE INPUT ----------------
st.markdown("### 🎤 Voice Answer")

audio = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹ Stop Recording",
    key="recorder"
)

if audio:
    st.success("Voice Recorded Successfully!")
    st.audio(audio["bytes"])
    if st.button("Submit Answer"):

        with st.spinner("Evaluating Answer..."):

            prompt = f"""
            Question:
            {st.session_state.question}

            Candidate Answer:
            {answer}

            Evaluate the answer.

            Give:
            1. Score out of 10
            2. Detailed Feedback
            3. Improved Answer
            """

            result = get_ai_response(prompt)

            st.markdown(f"""
            <div class="result-box">
            <h3>📊 Evaluation Result</h3>
            <p>{result}</p>
            </div>
            """, unsafe_allow_html=True)