# Copyright (c) 2024 Joseph Mapula. All rights reserved. See LICENSE file for details.
import os
from dotenv import load_dotenv
import openai
import anthropic
import PyPDF2
from docx import Document
import tempfile
import shutil


# Import the logging module, which provides a flexible framework for generating log messages in Python
import logging
# Configure the basic settings for the logging system
logging.basicConfig(
    level=logging.INFO,  # Set the root logger's level to INFO
    # This means it will capture all logs of severity INFO and above (INFO, WARNING, ERROR, CRITICAL)
    # Logs below this level (like DEBUG) will be ignored unless explicitly set for specific loggers
    
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    # Define the format of log messages:
    # %(asctime)s: Timestamp when the log was created
    # %(name)s: Name of the logger (in this case, it will be '__main__' unless specified otherwise)
    # %(levelname)s: Severity level of the log (e.g., INFO, WARNING, ERROR)
    # %(message)s: The actual log message
    
    datefmt='%Y-%m-%d %H:%M:%S'
    # Specify the date/time format in the log messages
)

# Create a logger instance for this module
logger = logging.getLogger(__name__)
# __name__ is a special variable in Python that holds the name of the current module
# In the main script, __name__ is set to '__main__'
# This allows you to have separate loggers for different modules in larger applications

# Now you can use logger to create log messages, for example:
# logger.debug("This is a debug message")
# logger.info("This is an info message")
# logger.warning("This is a warning message")
# logger.error("This is an error message")
# logger.critical("This is a critical message")

# The logging setup above ensures that:
# 1. All log messages are consistently formatted
# 2. Each log includes a timestamp, logger name, log level, and the message
# 3. Only logs of INFO level and above will be displayed/saved (due to level=logging.INFO)
# 4. You can easily adjust the logging level and format globally by modifying the basicConfig

# Load environment variables from the .env file
# This allows us to securely store and access API keys without hardcoding them
load_dotenv()

# Set up API keys for both OpenAI and Anthropic
# We retrieve these from environment variables to keep them secure
openai.api_key = os.getenv("OPENAI_API_KEY")
anthropic.api_key = os.getenv("ANTHROPIC_API_KEY")


def read_file(file_path):
    """
    Read content from various file types (PDF, DOCX, TXT, MD).
    
    Args:
        file_path (str): Path to the file to be read.
    
    Returns:
        str: Content of the file.
    
    Raises:
        ValueError: If the file type is not supported.
    """
    _, file_extension = os.path.splitext(file_path)
    
    if file_extension.lower() == '.pdf':
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            return ' '.join(page.extract_text() for page in pdf_reader.pages)
    
    elif file_extension.lower() == '.docx':
        doc = Document(file_path)
        return ' '.join(paragraph.text for paragraph in doc.paragraphs)
    
    elif file_extension.lower() in ['.txt', '.md']:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")


def generate_resume(job_description, background_info, best_practices, provider="openai", model="gpt-3.5-turbo", custom_prompt=None, max_tokens=1000):
    """
    Generate a tailored resume based on the provided information.

    This function takes various inputs and uses an AI model to generate a resume.
    It supports multiple AI providers and models, and allows for a custom prompt.

    Args:
        job_description (str): The description of the job being applied for.
        background_info (str): The applicant's professional background.
        best_practices (str): Best practices for resume writing.
        provider (str): The AI provider to use ('openai' or 'anthropic').
        model (str): The specific model to use (e.g., 'gpt-3.5-turbo' for OpenAI).
        custom_prompt (str, optional): A custom prompt to override the default.
        max_tokens (int): The maximum number of tokens in the generated resume.
                          Default is 1000, which is about 750 words or 1.5 pages.
                          Adjust this value based on desired resume length.

    Returns:
        str: The generated resume content.

    Raises:
        ValueError: If an unsupported provider is specified.
    """

    # Define the default prompt structure
    default_prompt = f"""
    Job Description:
    {job_description}

    My Professional Background:
    {background_info}

    Best Practices for Job Applications:
    {best_practices}

    Based on the job description, my professional background, and the best practices for job applications, 
    generate a tailored resume in markdown format. The resume should highlight relevant skills and experiences 
    that match the job requirements. Please structure the resume with the following sections:

    1. Contact Information
    2. Work Experience
    3. Education
    4. Skills (if relevant)
    5. Additional Sections (if relevant)

    Ensure that the content is concise, impactful, and directly relevant to the product manager position described.
    """

    # Use the custom prompt if provided, otherwise use the default
    prompt = custom_prompt if custom_prompt else default_prompt

    # Use the appropriate AI provider based on the 'provider' parameter
    if provider == "openai":
        # Create a chat completion using OpenAI's API
        response = openai.ChatCompletion.create(
            model=model,  # The specific model to use (e.g., 'gpt-3.5-turbo')
            messages=[
                {"role": "system", "content": "You are an expert resume writer specializing in product management positions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,  # Limit the response length. Adjust this for longer or shorter resumes.
            n=1,  # Generate only one completion
            stop=None,  # No custom stop sequence
            temperature=0.7,  # Control randomness (0.7 is moderately creative)
        )
        # Extract and return the generated content from the API response
        return response.choices[0].message['content'].strip()
    elif provider == "anthropic":
        # Create a completion using Anthropic's API
        client = anthropic.Client(api_key=anthropic.api_key)
        response = client.complete(
            model=model,  # The specific Claude model to use
            prompt=f"Human: {prompt}\n\nAssistant:",  # Format the prompt for Claude
            max_tokens_to_sample=max_tokens,  # Limit the response length. Adjust this for longer or shorter resumes.
            temperature=0.7,  # Control randomness (0.7 is moderately creative)
        )
        # Extract and return the generated content from the API response
        return response.completion.strip()
    else:
        # Raise an error if an unsupported provider is specified
        raise ValueError("Unsupported provider. Please use 'openai' or 'anthropic'.")

# Temperature spectrum:
# 0.0: Deterministic/repetitive. Always generates the most probable completion.
# 0.3: Conservative/focused. Generates more predictable and coherent text.
# 0.7: Moderately creative. Balances coherence with novelty. (Our current setting)
# 1.0: Very creative. More diverse outputs, but may occasionally be less coherent.
# 2.0: Highly unpredictable. Can generate more unusual or creative outputs, but with higher risk of incoherence.


def process_uploaded_files(job_description_file, background_info_file, best_practices_file):
    """
    Process uploaded files and extract their contents.
    
    Args:
        job_description_file (file object): Uploaded job description file.
        background_info_file (file object): Uploaded background information file.
        best_practices_file (file object): Uploaded best practices file.
    
    Returns:
        tuple: Extracted contents of job description, background info, and best practices.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_job_path = os.path.join(temp_dir, job_description_file.name)
        temp_background_path = os.path.join(temp_dir, background_info_file.name)
        temp_practices_path = os.path.join(temp_dir, best_practices_file.name)
        
        try:
            # Save uploaded files to temporary directory
            with open(temp_job_path, 'wb') as f:
                shutil.copyfileobj(job_description_file, f)
            with open(temp_background_path, 'wb') as f:
                shutil.copyfileobj(background_info_file, f)
            with open(temp_practices_path, 'wb') as f:
                shutil.copyfileobj(best_practices_file, f)
            
            # Read contents from temporary files
            job_description = read_file(temp_job_path)
            background_info = read_file(temp_background_path)
            best_practices = read_file(temp_practices_path)
            
            return job_description, background_info, best_practices
        
        finally:
            # Temporary directory and its contents are automatically removed
            pass

def save_resume(resume_content, output_path):
    """
    Save the generated resume to a file.
    
    Args:
        resume_content (str): The content of the generated resume.
        output_path (str): Path where the resume should be saved.
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(resume_content)

def main():
    """
    The main function to demonstrate the use of the generate_resume function.

    This function sets up sample inputs and generates resumes using different
    providers and models. In a real-world scenario, these inputs would come
    from user input or file reads.
    """
    # Example file paths (in a real scenario, these would come from user uploads)
    job_description_path = 'path/to/job_description.pdf'
    background_info_path = 'path/to/background_info.docx'
    best_practices_path = 'path/to/best_practices.txt'
    
    try:
        # Open files and process them
        with open(job_description_path, 'rb') as job_file, \
             open(background_info_path, 'rb') as background_file, \
             open(best_practices_path, 'rb') as practices_file:
            
            job_description, background_info, best_practices = process_uploaded_files(
                job_file, background_file, practices_file
            )
        
        # Generate resumes using both providers
        openai_resume = generate_resume(job_description, background_info, best_practices, provider="openai", model="gpt-3.5-turbo")
        claude_resume = generate_resume(job_description, background_info, best_practices, provider="anthropic", model="claude-3.5-sonnet")
        
        # Save generated resumes
        save_resume(openai_resume, 'openai_generated_resume.md')
        save_resume(claude_resume, 'claude_generated_resume.md')
        
        logger.info("Resumes generated and saved successfully!")
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {str(e)}")
    except ValueError as e:
        logger.error(f"Invalid input: {str(e)}")
    except IOError as e:
        logger.error(f"I/O error occurred: {str(e)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")


    # TODO: Create a user interface for inputting information and selecting options
    # TODO: Add a feedback mechanism for iterating on the generated resumes

if __name__ == "__main__":
    # This block ensures that the main() function is only called if this script is run directly,
    # not if it's imported as a module in another script.
    main()