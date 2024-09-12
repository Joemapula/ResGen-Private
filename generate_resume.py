# Copyright (c) 2024 Joseph Mapula. All rights reserved. See LICENSE file for details.
import os
from dotenv import load_dotenv
import openai
import anthropic

# Load environment variables from the .env file
# This allows us to securely store and access API keys without hardcoding them
load_dotenv()

# Set up API keys for both OpenAI and Anthropic
# We retrieve these from environment variables to keep them secure
openai.api_key = os.getenv("OPENAI_API_KEY")
anthropic.api_key = os.getenv("ANTHROPIC_API_KEY")

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
        response = anthropic.Completion.create(
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

def main():
    """
    The main function to demonstrate the use of the generate_resume function.

    This function sets up sample inputs and generates resumes using different
    providers and models. In a real-world scenario, these inputs would come
    from user input or file reads.
    """

    # Sample job description (in a real scenario, this could be read from a file or user input)
    job_description = """
    We are seeking a Product Manager to lead the development of innovative software products. 
    The ideal candidate will have experience in agile methodologies, user-centered design, 
    and data-driven decision making. Strong communication and leadership skills are essential.
    """

    # Sample background information (in a real scenario, this could be read from a file or user input)
    background_info = """
    I have 5 years of experience in software development, including 2 years as a junior product manager. 
    I've led cross-functional teams, conducted user research, and launched several successful products. 
    I have a BS in Computer Science and an MBA.
    """

    # Sample best practices (in a real scenario, this could be read from a file or user input)
    best_practices = """
    1. Tailor the resume to the specific job description
    2. Use action verbs and quantify achievements
    3. Keep the resume concise and focused
    4. Highlight relevant skills and experiences
    5. Use a clean, professional format
    """

    # Generate a resume using OpenAI's GPT-3.5-turbo model
    openai_resume = generate_resume(job_description, background_info, best_practices, provider="openai", model="gpt-3.5-turbo")
    print("OpenAI Generated Resume:")
    print(openai_resume)
    print("\n" + "="*50 + "\n")  # Separator for readability

    # Generate a resume using Anthropic's Claude model
    claude_resume = generate_resume(job_description, background_info, best_practices, provider="anthropic", model="claude-3.5-sonnet")
    print("Anthropic Generated Resume:")
    print(claude_resume)

    # TODO: Add logic to save the generated resumes to files
    # TODO: Implement a way to read job descriptions, background info, and best practices from files
    # TODO: Create a user interface for inputting information and selecting options
    # TODO: Implement error handling and logging
    # TODO: Add a feedback mechanism for iterating on the generated resumes

if __name__ == "__main__":
    # This block ensures that the main() function is only called if this script is run directly,
    # not if it's imported as a module in another script.
    main()