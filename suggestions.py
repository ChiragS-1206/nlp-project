import nltk
from nltk.tokenize import word_tokenize
import re
import json

# Download NLTK resources
nltk.download('punkt_tab', quiet=True)
nltk.download('punkt', quiet=True)

# Function to load data from a JSON file
def load_data_from_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)  # Load JSON data from the file
            return data.get('skills', [])  # Access the 'skills' key and return the skills list
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return []

# Load data from the JSON file
SKILLS = load_data_from_json('languages.json')  # Provide the correct file path

# Check if data was loaded successfully
# if SKILLS:
    # print("Data loaded from JSON:")
    # print(SKILLS)

def extract_skills(text):
    text = re.sub(r'[/\-]', ' ', text.lower())  # Clean the text
    found = set()
    for skill in SKILLS:
        if skill.lower() in text:  # Case insensitive comparison
            found.add(skill.lower())
    return found

def suggestions(resume_text, description):
    resume_skills = extract_skills(resume_text)
    desc_skills = extract_skills(description)
    missing = list(desc_skills - resume_skills)[:5]  # Get the first 5 missing skills
    return missing if missing else ["No specific skill gaps identified."]
