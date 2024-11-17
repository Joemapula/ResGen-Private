# ResGen - AI-Powered Resume Generator

## Why ResGen?
Job searching is hard, and existing resume tools often fall short. ResGen aims to make this process easier by focusing on two key advantages:

1. **Niche Resume Best Practices**: Instead of using generic templates, ResGen focuses on tech industry standards and role-specific emphasis.
2. **Comprehensive Background Processing**: Unlike other tools, ResGen leverages LLMs' ability to process extensive background information, creating more personalized and relevant outputs.

## Project Vision & Status

### Current Shape: One-Shot PDFs
The current version focuses on quickly generating tailored resumes by combining:
- Job descriptions
- Detailed professional background
- Industry-specific best practices

Current features include:
- Web interface for file uploads and resume generation
- Command-line interface for local use
- Support for both OpenAI (GPT) and Anthropic (Claude) models
- Markdown output format
- Structured resume sections (Contact, Experience, Education, Skills)
- Logging system for debugging

### Known Limitations
- Limited file format support
- Basic PDF styling
- Single-use resume generation

### Future Direction & Evolution
The project is intentionally flexible in its direction. We're exploring evolution into a broader job search tool, focusing on:

#### Knowledge Base Creation
Many people struggle with various aspects of job hunting:
- Resume creation
- Cover letter writing
- Interview preparation
- The "Tell me about yourself" pitch

At the heart of all these is how we perceive and present our experiences. We're exploring ways to:
1. **Gather** - Help people provide the right information about their experiences
2. **Compile** - Organize this information for multiple uses
3. **Leverage** - Use AI to transform this information for different purposes

## Getting Started

### Prerequisites
- Python 3.8+
- OpenAI API key
- Anthropic API key

### Installation
1. Clone the repository
```bash
git clone https://github.com/yourusername/resgen.git
cd resgen
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your API keys
```

### Usage

#### Web Interface
```bash
python app.py
```
Then visit `http://localhost:5000` in your browser.

#### Command Line
```bash
python generate_resume.py job_description.txt background_info.txt best_practices.txt
```

## Input Files
The system needs three text files:
1. **Job Description**: The position you're applying for
2. **Background Information**: Your professional experience and achievements
3. **Best Practices**: Resume guidelines (we provide defaults for tech roles)

## Development

### Project Structure
```
resgen/
├── app.py              # Flask web application
├── generate_resume.py  # Core resume generation logic
├── templates/         # Web interface templates
└── uploads/          # Temporary file storage
```

### Development Philosophy

- Experimental: Try things out, see what works
- Collaborative: Open to new ideas and approaches
- Iterative: Start simple, improve based on feedback
- Learning-focused: Great opportunity to work with AI, web development, and document processing

### Local Development
1. Create a new branch for your feature
2. Make changes and test locally
3. Create a pull request for review

### Looking for Help With
- UI/UX improvements
- Additional output formats
- Template design
- Testing and feedback
- New ideas and approaches

## Collaboration Philosophy
This project is meant to be collaborative and experimental. If you're interested in contributing:
- Have an idea? Share it!
- Want to try a new tool or approach? Go for it!
- See a different direction? Let's discuss it!

The goal is to create something useful while learning and experimenting together.

## Contributors
- Joseph Mapula (Creator)
- Chris Morris 
- Stephen Roberts 

## License
Copyright (c) 2024 Joseph Mapula. All rights reserved.
See LICENSE file for details.