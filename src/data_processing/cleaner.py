import re

def clean_text(text):

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # Remove weird characters
    text = re.sub(r'[^a-zA-Z0-9., ]', '', text)

    # Fix broken sentences
    text = text.replace("  ", " ")

    return text.strip()