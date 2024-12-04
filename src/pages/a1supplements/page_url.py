from typing import Optional

def get_url(url: str, index: Optional[int], seed: object) -> str:
    """
    Generates an incremented URL based on the provided index.

    Args:
        url (str): The base URL.
        index (Optional[int]): The current index, or None if not yet initialized.
        seed (object): An object containing the `url` attribute.

    Returns:
        str: The complete URL with the index.
    """

    seed_url = seed["url"]

    if index is None:
        index = 1
        return f"{seed_url}{index}", index

    index += 1
    return f"{seed_url}{index}", index