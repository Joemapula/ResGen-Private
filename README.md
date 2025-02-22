Here's an updated version of your **README** based on both the current content and the recent status update. It refines the structure, reflects completed work, highlights known issues, and aligns with your portfolio goals.

---

# 📝 **ResGen – AI-Powered Resume Generator**

## 💡 **Why ResGen?**
Job searching is hard, and existing resume tools often fall short. **ResGen** simplifies the process by focusing on two key advantages:

1. **🎯 Niche Resume Best Practices**  
   ResGen emphasizes **tech industry standards** and **role-specific formatting** rather than generic templates.

2. **🤖 Comprehensive Background Processing**  
   Unlike many tools, ResGen leverages **LLMs** (OpenAI & Anthropic) to process **extensive professional backgrounds**, creating **personalized** and **relevant** resumes.

---

## 🚀 **Project Vision & Status**

### ✅ **Current Core Features**
- **AI Model Integration:**  
  Supports **OpenAI (GPT)** and **Anthropic (Claude)** with model selection flexibility.

- **Dual Interface:**  
  - 🖥️ **Web Interface** (Flask-based) for file uploads and resume downloads.  
  - 🛠️ **Command-Line Interface (CLI)** for local usage.

- **File Handling:**  
  - Supports `.txt` and `.md` files for inputs.  
  - Temporary file handling with cleanup processes.

- **Resume Output:**  
  - Structured Markdown format with sections (Contact, Experience, Education, Skills).  
  - Conversion options to **DOCX** and **PDF** using **Pandoc** (supports `pdflatex`, `xelatex`, and `lualatex` engines).

- **Robust Logging & Error Handling:**  
  - Detailed logs for file processing, API interactions, and conversion outcomes.  
  - Structured error handling with multiple log levels.

---

### ⚠️ **Known Limitations**
- **🚫 Limited File Format Support:**  
  PDF and Word document reading not fully implemented.

- **🎨 Basic PDF Styling:**  
  LaTeX engine inconsistencies affect formatting.

- **💾 Single-Use Resume Generation:**  
  No current iteration/feedback mechanism for refining resumes.

- **❗ Incomplete Error Handling:**  
  Some cases lack user-facing error messages or graceful failures.

---

### 🔮 **Future Direction**
The long-term vision is to evolve ResGen into a **full-fledged job search tool**, expanding beyond resumes into:

1. 🗃️ **Knowledge Base Creation**  
   - Centralized user data for resume, cover letter, and interview prep.
   - Structured experience data for multiple job application materials.

2. 💌 **Cover Letter Generation**  
   - Leverage user data to auto-generate tailored cover letters.

3. 🎤 **Interview Preparation Tools**  
   - Create personalized "Tell me about yourself" pitches.
   - AI-generated interview questions based on job descriptions.

4. 📊 **Job Search Dashboard**  
   - Track applications, interview stages, and recruiter feedback.

---

## 📂 **Project Structure**

```
resgen/
├── app.py               # Flask web application (Web Interface)
├── generate_resume.py   # Core resume generation logic (CLI)
├── templates/           # Web interface templates
├── uploads/             # Temporary file storage
├── outputs/             # Generated resumes (Markdown, DOCX, PDF)
├── logs/                # Log files
├── .env                 # API Keys for OpenAI & Anthropic
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## ⚙️ **Getting Started**

### 🛠️ **Prerequisites**
- Python **3.8+**
- **OpenAI API key** and **Anthropic API key**
- **Pandoc** & **LaTeX distribution** (MiKTeX/TeXLive) for DOCX/PDF conversions

---

### 📥 **Installation**

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/resgen.git
cd resgen
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up API keys**
```bash
cp .env.example .env
# Add your OpenAI and Anthropic API keys in the .env file
```

---

## ⚡ **Usage Guide**

### ✅ **Web Interface**
```bash
python app.py
```
- Visit `http://localhost:5000` to upload files and generate resumes.

---

### ✅ **Command Line (CLI)**
```bash
python generate_resume.py job_description.txt background_info.txt best_practices.txt --generate-docx --generate-pdf
```

**Flags:**
- `--generate-docx` → Create a DOCX file  
- `--generate-pdf` → Create a PDF file  
- `--test-conversions` → Run conversion tests on existing Markdown  
- `--md-file` → Specify Markdown file for testing  
- `--docx-template` → Specify DOCX template for styling  

---

## 📁 **Input Files**
1. **`job_description.txt`** → The specific role you’re applying for  
2. **`background_info.txt`** → Your professional experience, achievements, and skills  
3. **`best_practices.txt`** → Resume writing guidelines (tech industry defaults provided)

---

## 🐞 **Known Issues**
- **DOCX File Corruption**: Some DOCX files experience corruption when using certain templates.  
- **PDF Formatting Inconsistencies**: Varies based on the LaTeX engine used.  
- **API Error Handling**: Some edge cases lack robust handling or informative feedback.

---

## 📊 **Roadmap**

### 🔥 **High Priority**
- [ ] Complete PDF and Word document reading functionality  
- [ ] Implement feedback mechanism for resume iteration  
- [ ] Add robust error messages for unsupported file types  
- [ ] Update AI model versions to current releases  

### 🌟 **Medium Priority**
- [ ] Resume template selection  
- [ ] Export options: DOCX, PDF, and HTML  
- [ ] Cover letter generation  

### 🌐 **Future Plans**
- [ ] Interview preparation tools  
- [ ] Resume comparison feature  
- [ ] Centralized knowledge base for job search assets  

---

## ✅ **Contributing**
1. Fork the repo  
2. Create a new branch (`git checkout -b feature/your-feature`)  
3. Commit your changes (`git commit -m 'Add new feature'`)  
4. Push to the branch (`git push origin feature/your-feature`)  
5. Open a Pull Request  

💡 **Looking for help with:**
- UI/UX design  
- Additional file format support  
- Resume styling and templates  
- API integration improvements  
- Testing & QA

---

## 🤝 **Contributors**
- **Joseph Mapula** (Creator)  
- **Chris Morris**  
- **Stephen Roberts**  

## License
Copyright (c) 2024 Joseph Mapula. All rights reserved.
See LICENSE file for details.