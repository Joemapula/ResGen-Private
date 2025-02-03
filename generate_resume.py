# Copyright (c) 2024 Joseph Mapula. All rights reserved. See LICENSE file for details.
import os
from typing import Optional
from dotenv import load_dotenv
import openai
from openai import OpenAI
import anthropic
from mistralai import Mistral
import PyPDF2
from docx import Document
import argparse
import tempfile
import shutil
# Import the logging module, which provides a flexible framework for generating log messages in Python
import logging
# Configure the basic settings for the logging system
logging.basicConfig(
    level=logging.DEBUG,  # Set the root logger's level 
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

# Set up API keys for OpenAIm, Anthropic, and Mistral (missing will return none)
openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
mistral_api_key = os.getenv("MISTRAL_API_KEY")

def validate_api_keys():
    if not openai_api_key:
        logger.error("OpenAI API key is missing. Please check your .env file.")
        raise ValueError("OpenAI API key is required")
    if not anthropic_api_key:
        logger.error("Anthropic API key is missing. Please check your .env file.")
        raise ValueError("Anthropic API key is required")
    if not mistral_api_key: 
        logger.error("Mistral API key is missing. Please check your .env file.")
        raise ValueError("Mistral API key is required")
    logger.info("API keys validated successfully.")
# Validate API keys before proceeding
validate_api_keys()

# Create clients for each provider
try:
    anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
    openai_client = OpenAI(api_key=openai_api_key)
    mistral_client = Mistral(api_key=mistral_api_key)
    logger.info("Clients created successfully.")
except Exception as e:
    logger.error(f"Error creating API clients: {e}")
    raise

def read_file(file_path):
    """
    Read content from various file types.
    
    Args:
        file_path (str): Path to the file.
    
    Returns:
        str: Content of the file.
    """
    _, file_extension = os.path.splitext(file_path)
    
    try:
        if file_extension.lower() == '.pdf':
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfFileReader(file)
                content = ""
                for page_num in range(reader.numPages):
                    content += reader.getPage(page_num).extract_text()
            logger.info(f"Successfully read PDF file: {file_path}")
            return content
        elif file_extension.lower() in ['.docx', '.doc']:
            doc = Document(file_path)
            content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            logger.info(f"Successfully read Word document: {file_path}")
            return content
        elif file_extension.lower() in ['.txt', '.md']:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            logger.info(f"Successfully read file: {file_path}")
            return content
        else:
            logger.error(f"Unsupported file type: {file_extension}")
            return ""
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {str(e)}")
        return ""

def generate_resume(
    job_description: str,
    background_info: str,
    best_practices: str,
    provider: str = "mistral",
    model: str = "mistral-large-latest",
    custom_prompt: Optional[str] = None,
    max_tokens: int = 4000
) -> str:    
    """
    Generate a tailored resume based on the provided information.

    This function takes various inputs and uses an AI model to generate a resume.
    It supports multiple AI providers and models, and allows for a custom prompt.

    Args:
        job_description (str): The description of the job being applied for.
        background_info (str): The applicant's professional background.
        best_practices (str): Best practices for resume writing.
        provider (str): The AI provider to use ('openai', 'anthropic', or 'mistral').
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

    logger.info(f"Generating resume using {provider} ({model})")
    logger.debug(f"Prompt preview: {prompt[:200]}...")
    # Use the appropriate AI provider based on the 'provider' parameter
    if provider == "openai":
        # Create a chat completion using OpenAI's API
        response = openai_client.chat.completions.create(
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
        return response.choices[0].message.content.strip()
    elif provider == "anthropic":
        # Create a completion using Anthropic's API
        message = anthropic_client.messages.create(
            model=model,  # The specific Claude model to use
            max_tokens=max_tokens,  # Limit the response length. Adjust this for longer or shorter resumes.
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,  # Control randomness (0.7 is moderately creative)
        )
        # Extract and return the generated content from the API response
        return message.content[0].text.strip()
    elif provider == "mistral":
        # Create a chat completion using Mistral's API
        response = mistral_client.chat.complete(
            model=model,
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=0.7,  # Control randomness (0.7 is moderately creative)
            max_tokens=max_tokens
        )

        # Extract and return the generated content from the API response
        return response.choices[0].message.content.strip()
    else:
        # Raise an error if an unsupported provider is specified
        raise ValueError("Unsupported provider. Please use 'openai', 'anthropic', or 'mistral'.")
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
        job_description_file: Flask FileStorage object for job description
        background_info_file: Flask FileStorage object for background info
        best_practices_file: Flask FileStorage object for best practices
    
    Returns:
        tuple: Contains the contents of job description, background info, and best practices.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_job_path = os.path.join(temp_dir, job_description_file.filename)
        temp_background_path = os.path.join(temp_dir, background_info_file.filename)
        temp_practices_path = os.path.join(temp_dir, best_practices_file.filename)
        
        try:
            # Save uploaded files to temporary directory
            job_description_file.save(temp_job_path)
            background_info_file.save(temp_background_path)
            best_practices_file.save(temp_practices_path)
            
            # Read contents from temporary files
            job_content = read_file(temp_job_path)
            background_content = read_file(temp_background_path)
            practices_content = read_file(temp_practices_path)
            
            # Log the lengths of the contents
            logger.info(f"Job description length: {len(job_content)} characters")
            logger.info(f"Background info length: {len(background_content)} characters")
            logger.info(f"Best practices length: {len(practices_content)} characters")
            
            return job_content, background_content, practices_content
        
        except Exception as e:
            logger.error(f"Error processing uploaded files: {str(e)}")
            return "", "", ""

def save_resume(resume_content, output_path):
    """
    Save the generated resume to a file.
    
    Args:
        resume_content (str): The content of the generated resume.
        output_path (str): Path where the resume should be saved.
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(resume_content)

def main(job_description_path, background_info_path, best_practices_path, log_level=logging.INFO):
    # Set the log level
    logging.getLogger().setLevel(log_level)
    try:
        # Open files and process them
        with open(job_description_path, 'rb') as job_file, \
             open(background_info_path, 'rb') as background_file, \
             open(best_practices_path, 'rb') as practices_file:
            
            job_description, background_info, best_practices = process_uploaded_files(
                args.job_description, args.background_info, args.best_practices
            )
        
        # Generate resumes using both providers
        openai_resume = generate_resume(job_description, background_info, best_practices, provider="openai", model="gpt-4o-mini-2024-07-18")
        claude_resume = generate_resume(job_description, background_info, best_practices, provider="anthropic", model="claude-3-5-sonnet-20240620")
        
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
    except anthropic.APIError as e:
        logger.error(f"Anthropic API error: {str(e)}")
    except openai.APIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
    except openai.APIConnectionError as e:
        #Handle connection error here
        logger.error(f"Failed to connect to OpenAI API: {e}")
        pass
    except openai.RateLimitError as e:
        #Handle rate limit error (we recommend using exponential backoff)
        logger.error(f"OpenAI API request exceeded rate limit: {e}")
        pass
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate resumes using AI")
    parser.add_argument("job_description", help="Path to the job description file")
    parser.add_argument("background_info", help="Path to the background information file")
    parser.add_argument("best_practices", help="Path to the best practices file")
    parser.add_argument("--log-level", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        default='INFO', help="Set the logging level")
    
    args = parser.parse_args()
    
    log_level = getattr(logging, args.log_level)
    main(args.job_description, args.background_info, args.best_practices, log_level)

    # TODO: Create a user interface for inputting information and selecting options
    # TODO: Add a feedback mechanism for iterating on the generated resumes

