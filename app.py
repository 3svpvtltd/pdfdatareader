from flask import Flask, request, jsonify, render_template
import PyPDF2
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="AIzaSyDjFgQ09blcxDsn3hCp0jffR4ZLExuODkg")

@app.route("/")
def home_page():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    # Extract text from PDF
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"

    # Summarize with Gemini
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"Read the following PDF text carefully and generate a clear, concise summary:\n\n{text}"
    response = model.generate_content(prompt)

    summary = response.text.strip() if response and response.text else "Summary could not be generated."

    return jsonify({"summary": summary})

if __name__ == '__main__':
    app.run(debug=True)
