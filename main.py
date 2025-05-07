from flask import Flask, request, jsonify, render_template
from similarity import matching_similarity
from suggestions import suggestions
from docx import Document

app = Flask(__name__)

def extract_text_from_docx(file):
    try:
        document = Document(file)
        full_text = [para.text for para in document.paragraphs if para.text.strip()]
        return '\n'.join(full_text) or "No text found in the document."
    except Exception as e:
        raise ValueError(f"Error reading .docx file: {str(e)}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    try:
        if "resume" not in request.files or "job_description" not in request.form:
            return jsonify({"error": "Missing resume file or job description"}), 400

        file = request.files["resume"]
        description = request.form["job_description"]
        # resume_text = "I have experience with Python, Django, Flask, Docker, and RESTful APIs"
        # description = "This job requires skills in Python, Flask, Docker, RESTful APIs, and Kubernetes"

        if not file or not description.strip():
            return jsonify({"error": "Empty resume file or job description"}), 400

        resume_text = extract_text_from_docx(file)
        similar = matching_similarity(resume_text, description)
        suggest = suggestions(resume_text, description)
        # print("Missing Skills:", suggest) 
        # 

        return jsonify({
            "score": similar,
            "feedback": suggest
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)