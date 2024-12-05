import base64
import hashlib
import re
import unicodedata
from typing import List, Optional


def find_in_text_with_wordlist(text: str, wordlist: List[str]) -> bool:
    """
    Searches for the presence of any word from the wordlist within the provided text.

    Args:
        text (str): The text to search within.
        wordlist (List[str]): A list of words to search for in the text.

    Returns:
        bool: True if any word from the wordlist is found in the text, False otherwise.
    """
    cleaned_text: str = clean_text(text)
    for word in wordlist:
        clean_word: str = clean_text(word)
        match = re.search(clean_word, cleaned_text)
        if match:
            return True
    return False


def levenshtein(s1: str, s2: str) -> int:
    """
    Calculates the Levenshtein distance between two strings.

    The Levenshtein distance is a measure of the difference between two sequences.
    It is the minimum number of single-character edits (insertions, deletions, or substitutions)
    required to change one word into the other.

    Args:
        s1 (str): The first string.
        s2 (str): The second string.

    Returns:
        int: The Levenshtein distance between the two strings.
    """
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row: List[int] = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row: List[int] = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1      # Insertion
            deletions = current_row[j] + 1           # Deletion
            substitutions = previous_row[j] + (c1 != c2)  # Substitution
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def encode_to_base64(value: str) -> str:
    """
    Encodes a given string to Base64.

    Args:
        value (str): The string to encode.

    Returns:
        str: The Base64 encoded string.
    """
    encoded_bytes: bytes = base64.b64encode(value.encode('utf-8'))
    encoded_str: str = encoded_bytes.decode('utf-8')
    return encoded_str


def generate_numeric_hash(data: str) -> int:
    """
    Generates a numeric hash value for the given data using Python's built-in hash function.

    Args:
        data (str): The data to hash.

    Returns:
        int: The absolute numeric hash value.
    """
    hash_value: int = hash(data)
    return abs(hash_value)


def generate_hash(value: str) -> str:
    """
    Generates a SHA-256 hash for the given string and returns the first 9 characters.

    Args:
        value (str): The string to hash.

    Returns:
        str: The first 9 characters of the SHA-256 hash.
    """
    sha256_hash: str = hashlib.sha256(value.encode('utf-8')).hexdigest()
    return sha256_hash[:9]


def remove_spaces(text: str) -> str:
    """
    Removes extra spaces from the text, replacing multiple whitespace characters with a single space.

    Args:
        text (str): The text to clean.

    Returns:
        str: The cleaned text with single spaces.
    """
    return re.sub(r'\s+', ' ', text).strip()


def clean_string_break_line(value: str) -> str:
    """
    Cleans a string by removing line breaks and non-breaking spaces, then removing extra spaces.

    Args:
        value (str): The string to clean.

    Returns:
        str: The cleaned string.
    """
    cleaned_value: str = value.replace('\n', '').replace('\xa0', ' ')
    return remove_spaces(cleaned_value)


def clean_text(
    text: str,
    clean_spaces: bool = False,
    remove_final_s: bool = False,
    remove_break_line: bool = True,
    remove_accents: bool = True,
    add_space_first: bool = False
) -> Optional[str]:
    """
    Cleans and formats text based on the provided parameters.

    This function can:
    - Remove accents from characters.
    - Remove punctuation and replace them with spaces.
    - Remove line breaks.
    - Remove trailing 's' characters.
    - Add a space at the beginning of the string.
    - Normalize whitespace.

    Args:
        text (str): The text to clean.
        clean_spaces (bool, optional): If True, collapse multiple spaces into one. Defaults to False.
        remove_final_s (bool, optional): If True, removes trailing 's' characters. Defaults to False.
        remove_break_line (bool, optional): If True, removes line breaks. Defaults to True.
        remove_accents (bool, optional): If True, removes accents from characters. Defaults to True.
        add_space_first (bool, optional): If True, adds a space at the beginning of the text. Defaults to False.

    Returns:
        Optional[str]: The cleaned and formatted text, or None if the input is not a string.
    """
    if not isinstance(text, str):
        return None

    if remove_accents:
        text = ''.join(
            c for c in unicodedata.normalize('NFKD', text)
            if not unicodedata.combining(c)
        )

    text = re.sub(r'[^\w\s]', ' ', text)  # Replace punctuation with space

    if remove_break_line:
        text = text.replace('\n', ' ')

    if remove_final_s:
        text = re.sub(r's\b', ' ', text)

    if add_space_first:
        text = f' {text}'

    if clean_spaces:
        text = re.sub(r'\s+', ' ', text).strip()
    else:
        # Replace each whitespace character with a single space
        text = re.sub(r'\s+', lambda match: ' ' * len(match.group(0)), text)

    text = text.lower()

    return text