import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

# -----------------------------
# LOAD API KEY
# -----------------------------
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(
    page_title="AI Student Material",
    page_icon="📚",
    layout="wide"
)

# -----------------------------
# HEADER
# -----------------------------
st.title("📚 AI Student Material")
st.write("Upload your study material and let AI help you learn.")

st.markdown("---")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("🎓 Learning Options")

material_type = st.sidebar.selectbox(
    "Choose Material",
    [
        "Study Notes",
        "Important Questions",
        "MCQs",
        "Question & Answers",
        "Exam Preparation"
    ]
)

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Medium", "Hard"]
)

# -----------------------------
# PDF UPLOAD
# -----------------------------
st.header("📄 Upload Study Material")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

# -----------------------------
# TOPIC
# -----------------------------
topic = st.text_input(
    "🎯 Enter your topic",
    placeholder="Example: DBMS, Java, Operating System..."
)

# -----------------------------
# GENERATE BUTTON
# -----------------------------
if st.button("🤖 Generate Material", use_container_width=True):

    if not api_key:
        st.error("API key not found. Check your .env file.")

    elif not topic and not uploaded_file:
        st.warning("Please enter a topic or upload a PDF.")

    else:

        # -----------------------------
        # GET PDF TEXT
        # -----------------------------
        pdf_text = ""

        if uploaded_file:

            reader = PdfReader(uploaded_file)

            for page in reader.pages:
                text = page.extract_text()

                if text:
                    pdf_text += text + "\n"

            # Limit text sent to AI
            pdf_text = pdf_text[:20000]

        # -----------------------------
        # CREATE PROMPT
        # -----------------------------
        if uploaded_file:

            prompt = f"""
You are an AI educational assistant.

The student uploaded study material.

Topic:
{topic if topic else "Not specified"}

Requested material:
{material_type}

Difficulty:
{difficulty}

Study material:
{pdf_text}

Create useful learning material based mainly on the uploaded material.

Use simple English.
Use headings, bullet points and clear explanations.
"""

        else:

            prompt = f"""
You are an AI educational assistant.

Topic:
{topic}

Requested material:
{material_type}

Difficulty:
{difficulty}

Create clear and accurate learning material for a college student.

Use simple English.
Use headings and bullet points.
Include useful examples where appropriate.
"""

        # -----------------------------
        # CALL AI
        # -----------------------------
        with st.spinner("🤖 AI is preparing your material..."):

            try:

                client = OpenAI(api_key=api_key)

                response = client.responses.create(
                    model="gpt-5-mini",
                    input=prompt
                )

                result = response.output_text

                st.success("Material generated successfully! 🎉")

                st.markdown("---")
                st.header("📚 Generated Material")

                st.markdown(result)

            except Exception as e:

                st.error("Something went wrong.")
                st.write(str(e))

# -----------------------------
# FEATURES
# -----------------------------
st.markdown("---")

st.header("✨ Features")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.write("📄")
    st.write("PDF Upload")

with col2:
    st.write("📝")
    st.write("Study Notes")

with col3:
    st.write("🎯")
    st.write("MCQs")

with col4:
    st.write("❓")
    st.write("Questions")

with col5:
    st.write("📖")
    st.write("Exam Preparation")

st.markdown("---")

st.caption("AI Student Material | Hackathon Project")