from flask import Flask, render_template, request, send_file
import os
from werkzeug.utils import secure_filename
from your_resume_generator import generate_resume, process_uploaded_files

app = Flask(__name__)

# Ensure the upload folder exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file parts
        if 'job_description' not in request.files or 'background_info' not in request.files or 'best_practices' not in request.files:
            return 'Missing file parts', 400
        
        job_description = request.files['job_description']
        background_info = request.files['background_info']
        best_practices = request.files['best_practices']
        
        # If user does not select a file, browser also submits an empty file without filename
        if job_description.filename == '' or background_info.filename == '' or best_practices.filename == '':
            return 'No selected file', 400
        
        # Save uploaded files
        job_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(job_description.filename))
        background_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(background_info.filename))
        practices_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(best_practices.filename))
        
        job_description.save(job_path)
        background_info.save(background_path)
        best_practices.save(practices_path)
        
        # Process files and generate resume
        job_content, background_content, practices_content = process_uploaded_files(job_description, background_info, best_practices)
        resume = generate_resume(job_content, background_content, practices_content)
        
        # Save generated resume
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], 'generated_resume.md')
        with open(resume_path, 'w') as f:
            f.write(resume)
        
        # Return the generated resume file
        return send_file(resume_path, as_attachment=True)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)