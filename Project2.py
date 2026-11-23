
import streamlit as st
import requests
import re
from pypdf import PdfReader
from docx import Document
from bs4 import BeautifulSoup
import io

st.title("Document AI Assistant")

st.markdown("""
Upload documents, ask questions, or generate an abbreviation index
using an open-source language model.
""")

# Ollama model settings
MODEL = "qwen3:8b"
OLLAMA_URL = "http://localhost:11434/api/chat"


# Function to communicate with Ollama
def ask_llm(prompt):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        },
        timeout=300
    )

    response.raise_for_status()

    return response.json()["message"]["content"]


# Function to extract document text
def extract_text(file):

    extension = file.name.split(".")[-1].lower()

    if extension == "txt":
        return file.getvalue().decode("utf-8", errors="replace")

    elif extension == "pdf":
        pdf = PdfReader(io.BytesIO(file.getvalue()))
        text = ""

        for page in pdf.pages:
            text += (page.extract_text() or "") + "\n"

        return text

    elif extension == "docx":
        document = Document(io.BytesIO(file.getvalue()))
        text = ""

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        return text

    elif extension in ["html", "htm"]:
        soup = BeautifulSoup(
            file.getvalue(),
            "html.parser"
        )

        return soup.get_text(separator="\n")

    return ""


# Function to find abbreviation definitions
def find_abbreviation_candidates(text):

    pattern = r'\b([A-Za-z][A-Za-z-]*(?:\s+[A-Za-z][A-Za-z-]*){1,9})\s*\(([A-Z][A-Z0-9-]{1,9})\)'

    matches = re.finditer(pattern, text)

    candidates = []

    for match in matches:

        full_term = match.group(1).strip()
        abbreviation = match.group(2).strip()

        candidates.append(
            f"{abbreviation}: {full_term}"
        )

    return list(dict.fromkeys(candidates))


# Create application tabs
tab1, tab2 = st.tabs([
    "Ask Questions",
    "Abbreviation Index"
])


# ----------------------------------
# TAB 1: DOCUMENT QUESTION ANSWERING
# ----------------------------------

with tab1:

    st.subheader("Ask Questions About Documents")

    question = st.text_area("Enter your question:")

    uploaded_file = st.file_uploader(
        "Upload a document (optional)",
        type=["txt", "pdf", "docx", "html", "htm"],
        key="question_file"
    )

    if st.button("Submit Question"):

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            document_text = ""

            if uploaded_file is not None:
                document_text = extract_text(uploaded_file)

            prompt = f"""
            Answer the following question using the uploaded
            document as context.

            If the answer is not found in the document,
            explain that it is not provided.

            Document:
            {document_text[:15000]}

            Question:
            {question}
            """

            try:

                with st.spinner("Generating answer..."):

                    answer = ask_llm(prompt)

                st.subheader("AI Response")
                st.markdown(answer)

            except Exception as e:

                st.error(f"Error communicating with Ollama: {e}")


# ----------------------------------
# TAB 2: ABBREVIATION INDEX
# ----------------------------------

with tab2:

    st.subheader("Generate Abbreviation Index")

    st.markdown("""
    Upload one or more scientific articles in PDF format.
    The application will identify abbreviations and their
    corresponding full terms.
    """)

    articles = st.file_uploader(
        "Upload scientific articles",
        type=["pdf"],
        accept_multiple_files=True,
        key="article_files"
    )

    if st.button("Generate Abbreviation Index"):

        if not articles:

            st.warning("Please upload at least one PDF article.")

        else:

            for article in articles:

                st.divider()

                st.subheader(article.name)

                try:

                    # Extract article text
                    article_text = extract_text(article)

                    if not article_text.strip():

                        st.warning("No readable text found in this PDF.")
                        continue

                    # Find possible abbreviation definitions
                    candidates = find_abbreviation_candidates(
                        article_text
                    )

                    if not candidates:

                        st.info(
                            "No abbreviation definitions were identified."
                        )
                        continue

                    # Ask the LLM to organize and verify candidates
                    prompt = f"""
                    You are analyzing a scientific research article.

                    Create an abbreviation index using the
                    abbreviation definitions identified below.

                    Only include abbreviations that have an explicitly
                    provided full term in the source material.

                    Do not invent definitions or guess meanings.

                    Remove duplicate entries.

                    Format the output exactly like this:

                    • WDC: weighted degree centrality
                    • SH: structural holes

                    Abbreviation definitions found in the article:

                    {chr(10).join(candidates)}

                    Return only the abbreviation index.
                    """

                    with st.spinner(
                        f"Analyzing {article.name}..."
                    ):

                        result = ask_llm(prompt)

                    st.markdown(result)

                except Exception as e:

                    st.error(
                        f"Could not process {article.name}: {e}"
                    )
