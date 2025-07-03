from flask import Flask, request, jsonify, render_template
import os
#import mysql.connector

from resume_parser_own_model import resume_parser # 👈 your new function

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/')
def index():
    return render_template('main.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
     # Save uploaded file first
    file = request.files.get('resume')
    if not file:
        return "No file uploaded", 400
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    # Parse all PDFs in the folder (including this newly uploaded file)
    resumes = []
    folder_path = app.config['UPLOAD_FOLDER']
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.pdf','.doc', '.docx')):
        
            try:
                filepath = os.path.join(folder_path, filename)
                parsed = resume_parser(filepath)
                parsed["Filename"] = filename  # Add filename to result
                resumes.append(parsed)
            except Exception as e:
                resumes.append({
                    "Filename": filename,
                    "Error": str(e),
                     "Name": "", "Email": "", "Phone": "", "Location": "", "Skills": ""    
                })
    print("Result data:", resumes)  
    return render_template('results.html', resumes=resumes)

  
if __name__ == "__main__":
    app.run(debug=True)
