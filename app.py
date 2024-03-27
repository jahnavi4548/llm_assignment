from flask import Flask, request, render_template, redirect, url_for, jsonify, session
from docx import Document
import pandas as pd
import tempfile
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
import fitz  # PyMuPDF
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)   # Set a secret key for session management

# Set OpenAI API key from environment variable
os.environ["OPENAI_API_KEY"] = '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'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload_pdf():
    if request.method == "POST":
        # Handle file upload here
        uploaded_file = request.files.get("file")
        if uploaded_file:
            # Create a temporary directory to store the uploaded files
            temp_dir = tempfile.mkdtemp()
            file_path = os.path.join(temp_dir, uploaded_file.filename)
            # Save the uploaded file to the temporary directory
            uploaded_file.save(file_path)
            # Store the file path in the session
            session["file_path"] = file_path
            return redirect(url_for("ask_question"))
        else:
            return jsonify({"error": "No file uploaded"}), 400

    return render_template("upload.html")

@app.route("/ask_question", methods=["GET", "POST"])
def ask_question():
    if request.method == "POST":
        # Get the path of the uploaded file from the session
        file_path = session.get("file_path")
        if not file_path:
            return jsonify({"error": "No file uploaded"}), 400
        
        # Read file and extract text
        try:
            text = extract_text_from_file(file_path)
            if len(text)<=0:
                raise Exception("Text extraction returned an empty string")
        except Exception as e:
            return jsonify({"error": f"Error reading file: {e}"}), 500
        
        
        
               

        # Split text into chunks
        text_chunks = split_text_into_chunks(text)

        # Use the embeddings from OpenAI
        embeddings = OpenAIEmbeddings()
        pdf_embeddings = FAISS.from_texts(text_chunks, embeddings)

        input_text = request.form.get("question")

        # Use the summarization chain to generate a summary
        try:
            chain = load_qa_chain(OpenAI(model="gpt-3.5-turbo-instruct",top_p=0.7,temperature=0.7, max_tokens=1000 ), chain_type="stuff")
            query = input_text
            docs = pdf_embeddings.similarity_search(query)
            summary = chain.run(input_documents=docs, question=query)
            return jsonify({query: summary})
        except Exception as e:
            return jsonify({"error": f"Error during summarization: {e}"}), 500

    return render_template("ask_question.html")

def extract_text_from_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    # Extract text based on file extension
    if file_extension.lower() == ".pdf":
        return extract_text_from_pdf(file_path)
    elif file_extension.lower() in [".doc", ".docx"]:
        return extract_text_from_docx(file_path)
    elif file_extension.lower() == ".csv":
        return extract_text_from_csv(file_path)
    elif file_extension.lower() in [".xls", ".xlsx"]:
        return extract_text_from_excel(file_path)
    else:
        return "Unsupported file format"

def extract_text_from_pdf(pdf_file_path):
    with fitz.open(pdf_file_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        return f"Error reading DOCX file: {e}"
    
def extract_text_from_csv(file_path):
    try:
        # Try reading the CSV file with different encodings
        for encoding in ['utf-8', 'latin1', 'utf-16']:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                text = df.to_string(index=False)
                return text
            except Exception as e:
                continue
        # If none of the encodings work, raise an error
        raise Exception("Unable to read CSV file with any encoding")
    except Exception as e:
        return f"Error reading CSV file: {e}"


def extract_text_from_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        text = df.to_string(index=False)
        return text
    except Exception as e:
        return f"Error reading Excel file: {e}"

def split_text_into_chunks(text):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len)
    return text_splitter.split_text(text)

if __name__ == "__main__":
    pass
