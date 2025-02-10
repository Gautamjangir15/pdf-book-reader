from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import fitz  # PyMuPDF for extracting text from PDFs
from gtts import gTTS
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    text = extract_text_from_pdf(file_path)
    audio_file = convert_text_to_speech(text, file.filename)
    
    return jsonify({"message": "File processed successfully", "audio_file": audio_file, "text": text})

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def convert_text_to_speech(text, filename):
    tts = gTTS(text, lang="en")
    audio_path = os.path.join(OUTPUT_FOLDER, filename.replace(".pdf", ".mp3"))
    tts.save(audio_path)
    return filename.replace(".pdf", ".mp3")

@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get Render's port or default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)
