from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
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
            # Convert the skills list to a set to remove duplicates
            skills = set(data.get('skills', []))  # Extract unique skills
            # Normalize skills to lowercase
            skills = {skill.lower() for skill in skills}
            return skills
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return set()


# Load data from the JSON file
SKILLS = load_data_from_json('languages.json')  # Corrected file name

# Check if data was loaded successfully
# if SKILLS:
#     print("Data loaded from JSON:")
#     print(SKILLS)


# Function to clean text and include skills as tokens
def clean_text(text):
    text = re.sub(r'[/\-]', ' ', text.lower())  # Clean text by replacing / and - with spaces
    tokens = word_tokenize(text)  # Tokenize the cleaned text
    tokens = [word for word in tokens if word.isalpha() or word in SKILLS]  # Keep only words and skills
    cleaned = ' '.join(tokens)  # Join tokens back into a single string

    # Add skills explicitly if they exist in the text (ensuring that skills are included)
    for skill in SKILLS:
        if skill in text.lower():
            cleaned += f" {skill}"

    return cleaned


# Function to compute matching similarity using CountVectorizer and cosine similarity
def matching_similarity(resume_text, description):
    resume = clean_text(resume_text)  # Clean resume text
    desc = clean_text(description)    # Clean job description text
    vectorizer = CountVectorizer(ngram_range=(1, 3), vocabulary=SKILLS)  # Initialize CountVectorizer with skill-based vocabulary
    vect = vectorizer.fit_transform([resume, desc])  # Transform texts into word count vectors
    similarity = cosine_similarity(vect[0:1], vect[1:2])[0][0]  # Calculate cosine similarity between the vectors
    return round(similarity * 100, 2) 