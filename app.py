from flask import Flask, render_template, request, send_file, jsonify
import os
import shutil
from werkzeug.utils import secure_filename
from generate_resume import extract_job_title_and_company_regex, save_resume, cleanup_temp_folder

app = Flask(__name__)

# Define folder locations
UPLOAD_FOLDER = 'uploads'  # Stores user-uploaded files
TEMP_FOLDER = 'temp'       # Temporary folder for processing

# Ensure folders exist
for folder in [UPLOAD_FOLDER, TEMP_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMP_FOLDER'] = TEMP_FOLDER

# Extract job title & company from job description
job_title, company_name = extract_job_title_and_company_regex(job_content)

# Use defaults if extraction fails
if not job_title:
    job_title = "Unknown Job Title"
if not company_name:
    company_name = "Unknown Company"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Validate file uploads
        if 'job_description' not in request.files or \
           'background_info' not in request.files or \
           'best_practices' not in request.files:
            return jsonify({"error": "Missing file(s)"}), 400

        job_description = request.files['job_description']
        background_info = request.files['background_info']
        best_practices = request.files['best_practices']

        # Ensure files were actually selected
        if job_description.filename == '' or background_info.filename == '' or best_practices.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Save uploaded files securely
        job_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(job_description.filename))
        background_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(background_info.filename))
        practices_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(best_practices.filename))

        job_description.save(job_path)
        background_info.save(background_path)
        best_practices.save(practices_path)

        # Use a temp folder for processing (avoids modifying original uploads)
        temp_dir = os.path.join(app.config['TEMP_FOLDER'], secure_filename(job_description.filename) + "_temp")
        os.makedirs(temp_dir, exist_ok=True)

        temp_job_path = os.path.join(temp_dir, os.path.basename(job_path))
        temp_background_path = os.path.join(temp_dir, os.path.basename(background_path))
        temp_practices_path = os.path.join(temp_dir, os.path.basename(practices_path))

        shutil.copy(job_path, temp_job_path)
        shutil.copy(background_path, temp_background_path)
        shutil.copy(practices_path, temp_practices_path)

        # Process the copied files
        job_content, background_content, practices_content = process_uploaded_files(temp_job_path, temp_background_path, temp_practices_path)

        try:
            resume = generate_resume(job_content, background_content, practices_content)
        except Exception as e:
            return jsonify({"error": f"Resume generation failed: {str(e)}"}), 500

        # Save the generated resume
        resume_path = save_resume(resume, job_title, company_name, "mistral-large", format="md")
        with open(resume_path, 'w', encoding='utf-8') as f:
            f.write(resume)

        # Clean up temp files after processing
        cleanup_temp_folder()


        return send_file(resume_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
