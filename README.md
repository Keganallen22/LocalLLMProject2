
# Document AI Assistant

A Python-based web application built with Streamlit that uses an open-source Large Language Model (LLM) to analyze documents, answer questions, and generate abbreviation indexes for scientific articles.

The application uses [Ollama](https://ollama.com/) to run the Qwen language model locally, so users do not need an OpenAI API key or a paid AI API subscription.

## Features

### 1. Ask Questions About Documents

- Enter questions using a simple web interface.
- Upload an optional document for additional context.
- Receive AI-generated answers based on the uploaded document.
- Supported document formats:
  - PDF (.pdf)
  - Word (.docx)
  - Plain Text (.txt)
  - HTML (.html, .htm)

### 2. Generate Abbreviation Index

- Upload multiple scientific articles in PDF format.
- Automatically identify abbreviations and their corresponding full terms.
- Use the LLM to organize abbreviation definitions.
- Remove duplicate entries.
- Generate a separate abbreviation index for each article.

Example output:

- WDC: weighted degree centrality
- SH: structural holes
- SNA: social network analysis

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application programming language |
| Streamlit | Web application interface |
| Ollama | Local LLM hosting |
| Qwen 3.5 4B | Open-source language model |
| Requests | Communication with Ollama API |
| PyPDF | PDF text extraction |
| python-docx | Word document extraction |
| BeautifulSoup4 | HTML text extraction |

## Requirements

Before installing the application, make sure you have:

- Python 3.9 or newer
- pip (Python package installer)
- Ollama installed
- An internet connection for downloading the model and dependencies

## Installation

### Step 1: Download the Project

Clone the GitHub repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Alternatively, select **Code → Download ZIP** on GitHub and extract the project.

Navigate into the project directory:

```bash
cd document-ai-assistant
```

### Step 2: Install Python Dependencies

Install the required packages:

```bash
pip install streamlit requests pypdf python-docx beautifulsoup4
```

Alternatively, install them using the included requirements.txt file:

```bash
pip install -r requirements.txt
```

### Step 3: Install Ollama

Download and install Ollama:

https://ollama.com/download

Ollama allows users to run open-source language models locally on their computers.

### Step 4: Download the Qwen Model

Open a terminal and run:

```bash
ollama pull qwen3.5:4b
```

This downloads the Qwen 3.5 4B model.

The model only needs to be downloaded once.

### Step 5: Start Ollama

Make sure Ollama is running.

On most desktop installations, Ollama runs in the background after installation.

You can verify that the model is available by running:

```bash
ollama list
```

### Step 6: Launch the Application

Navigate to the project directory and run:

```bash
streamlit run app.py
```

Streamlit will start the application and provide a local URL.

Open the URL in your browser:

```text
http://localhost:8501
```

The application is now ready to use!

## How to Use the Application

### Ask Questions

1. Open the **Ask Questions** tab.
2. Enter a question into the text box.
3. Optionally upload a document.
4. Select **Submit Question**.
5. Wait for the LLM to process the request.
6. Review the generated response.

If no document is uploaded, the LLM will answer using its general knowledge.

### Generate an Abbreviation Index

1. Open the **Abbreviation Index** tab.
2. Upload one or more scientific articles in PDF format.
3. Select **Generate Abbreviation Index**.
4. The application extracts the text from each article.
5. Potential abbreviation definitions are identified.
6. The LLM organizes the definitions into an abbreviation index.
7. Review the results for each uploaded article.

Example:

```text
Article1.pdf

• WDC: weighted degree centrality
• SH: structural holes
• SNA: social network analysis
```

## Project Structure

```text
document-ai-assistant/
│
├── app.py
├── requirements.txt
└── README.md
```

| File | Description |
|---|---|
| app.py | Main Streamlit application |
| requirements.txt | Required Python packages |
| README.md | Installation and usage instructions |

## Troubleshooting

### Ollama Connection Error

If you receive an error connecting to Ollama, verify that Ollama is running.

You can test the local API by opening:

```text
http://localhost:11434
```

You should receive a response indicating that Ollama is running.

### Model Not Found

If the application reports that the model cannot be found, run:

```bash
ollama pull qwen3.5:4b
```

Make sure the model name in app.py matches the installed model.

### Missing Python Packages

If you receive a ModuleNotFoundError, install the dependencies again:

```bash
pip install -r requirements.txt
```

### PDF Text Extraction Issues

The application extracts selectable text from PDFs. Scanned documents containing only images may require OCR before they can be analyzed.

## Limitations

- The LLM runs locally, so response speed depends on the user's hardware.
- The Q&A feature currently limits document context to 15,000 characters.
- PDF extraction works with text-based PDFs, not scanned images without OCR.
- Word document support is for .docx files, not older .doc files.
- The abbreviation index currently looks for conventional definitions formatted as Full Term (ABBR).
- Abbreviation extraction may not identify every abbreviation in an article.
- Results should be reviewed for accuracy.

## Deployment and Distribution

This project is distributed through GitHub.

GitHub provides access to the application source code, but does not host the local AI model.

Each user must install Python, Streamlit, and Ollama, download the Qwen model, and run the application on their own computer.

No external AI API subscription is required.

## License

This project is intended for educational and demonstration purposes.
