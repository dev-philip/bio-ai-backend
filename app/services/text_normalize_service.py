import re
import nltk
from typing import Optional

# Download stopwords only once
nltk.download('stopwords')
from nltk.corpus import stopwords

EN_STOPWORDS = set(stopwords.words('english'))
SCIENTIFIC_SYMBOLS = set("+-αβ")  # Add more symbols as needed

def normalize_text(text: str, remove_stopwords: Optional[bool] = False) -> str:
    if not text:
        return ""

    # Step 1: Trim leading/trailing whitespace
    text = text.strip()

    # Step 2: Remove unwanted symbols (keep alphanumeric + scientific symbols)
    def clean_char(char):
        return char.isalnum() or char.isspace() or char in SCIENTIFIC_SYMBOLS

    cleaned = ''.join(c if clean_char(c) else ' ' for c in text)

    # Step 3: Convert to lowercase
    cleaned = cleaned.lower()

    # Step 4: Remove extra internal whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned)

    # Step 5: Optional stop word removal
    if remove_stopwords:
        cleaned = ' '.join(word for word in cleaned.split() if word not in EN_STOPWORDS)

    return cleaned.strip()
