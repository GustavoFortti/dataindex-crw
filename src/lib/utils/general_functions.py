from typing import Any, List, Optional

import requests
from fake_useragent import UserAgent


def flatten_list(list_of_lists: Optional[List[Any]]) -> List[Any]:
    """
    Flattens a nested list into a single list.

    Args:
        list_of_lists (Optional[List[Any]]): A list that may contain nested lists.

    Returns:
        List[Any]: A flattened list containing all elements from the input.

    Example:
        Input: [[1, 2], [3, [4, 5]], 6]
        Output: [1, 2, 3, [4, 5], 6]
    """
    if list_of_lists is None:
        return []

    flattened_list: List[Any] = []
    for element in list_of_lists:
        if isinstance(element, list):
            flattened_list.extend(element)
        else:
            flattened_list.append(element)

    return flattened_list


def check_url_existence(url: str, timeout: int = 5) -> bool:
    """
    Checks if a URL is accessible.

    This function first tries to send a HEAD request to the URL.
    If the server does not allow HEAD requests (HTTP 405), it falls back to a GET request.

    Args:
        url (str): The URL to check.
        timeout (int, optional): The timeout for the request in seconds. Defaults to 5.

    Returns:
        bool: True if the URL is accessible (HTTP status code between 200 and 399), False otherwise.
    """
    ua = UserAgent()
    headers = {'User-Agent': ua.random}

    try:
        # Attempt with HEAD method first
        response = requests.head(url, headers=headers, timeout=timeout)
        if response.status_code == 405:  # Method not allowed
            # Fall back to GET method
            response = requests.get(url, headers=headers, timeout=timeout)
        # Return True if status code is between 200 and 399
        return 200 <= response.status_code < 400
    except requests.RequestException as e:
        # Log the error and return False
        print(f"Error checking URL '{url}': {e}")
        return False