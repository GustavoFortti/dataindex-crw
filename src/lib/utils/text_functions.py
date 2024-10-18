import base64
import hashlib
import re
import unicodedata
from typing import Optional

from src.lib.utils.log import message

DATE_FORMAT = "%Y-%m-%d"

def find_in_text_with_wordlist(text, wordlist):
    match = None
    for word in wordlist:
        clean_word = clean_text(word)
        text = clean_text(text)
        
        match = re.search(clean_word, clean_text(text))  # Expressão regular para encontrar dígitos
        if match:
            break
            
    if match:
        return True
    return False

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def encode_to_base64(value: str) -> str:
    """Encodes a string to Base64."""
    return base64.b64encode(value.encode('utf-8')).decode('utf-8')

def generate_numeric_hash(data: str) -> int:
    """Generates a numeric hash value for the given data."""
    hash_value = hash(data)
    return abs(hash_value)

def generate_hash(value):
    return hashlib.sha256(value.encode()).hexdigest()[:8]

def remove_spaces(text):
    return re.sub(r'\s+', ' ', text).strip()

def clean_string_break_line(value):
    return remove_spaces(str(value).replace('\n', '').replace('\xa0', ' '))

def clean_text(text: str, clean_spaces: bool = False, remove_final_s: bool = False, 
               remove_break_line: bool = True, remove_accents: bool = True, 
               add_space_first: bool = False) -> Optional[str]:
    """Cleans and formats text based on the provided parameters."""
    
    if not isinstance(text, str):
        return None

    if remove_accents:
        text = ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))

    text = re.sub(r'[^\w\s]', ' ', text)
    
    if remove_break_line:
        text = text.replace('\n', ' ')
    
    if remove_final_s:
        text = re.sub(r's\b', ' ', text)
    
    if add_space_first:
        text = ' ' + text

    if clean_spaces:
        text = re.sub(r'\s+', ' ', text).strip()
    else:
        text = re.sub(r'\s+', lambda match: ' ' * len(match.group(0)), text)

    text = text.lower()

    return text