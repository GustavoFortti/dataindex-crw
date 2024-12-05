from bs4 import BeautifulSoup
from typing import List, Optional


def get_items(soup: BeautifulSoup) -> List[BeautifulSoup]:
    """
    Extracts all product items from the given BeautifulSoup object.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object containing the parsed HTML.

    Returns:
        List[BeautifulSoup]: A list of BeautifulSoup objects for each product item.
    """
    return soup.find_all('li', class_='grid__item')


def get_product_url(soup: BeautifulSoup, base_url: str) -> Optional[str]:
    """
    Extracts the product URL from the given BeautifulSoup object and appends it to the base URL.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object containing the parsed HTML for a product.
        base_url (str): The base URL to prepend to the extracted product link.

    Returns:
        Optional[str]: The full product URL or None if not found.
    """
    product_link_element = soup.find('a')
    if product_link_element and 'href' in product_link_element.attrs:
        return f"{base_url}{product_link_element['href']}"
    return None


def get_title(soup: BeautifulSoup) -> Optional[str]:
    """
    Extracts the product title from the given BeautifulSoup object.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object containing the parsed HTML for a product.

    Returns:
        Optional[str]: The product title or None if not found.
    """
    title_element = soup.find('h2')
    return title_element.get_text().strip() if title_element else None


def get_price(soup: BeautifulSoup) -> Optional[str]:
    """
    Extracts the product price from the given BeautifulSoup object.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object containing the parsed HTML for a product.

    Returns:
        Optional[str]: The product price or None if not found.
    """
    price_container = soup.find(class_="price__container")
    if price_container:
        price_element = price_container.find('span', class_="price-item price-item--regular")
        if price_element:
            price = price_element.get_text().strip()
            if price.lower().startswith("from"):
                return price.replace("From", "").strip()
            return price
    return None


def get_image_url(soup: BeautifulSoup) -> Optional[str]:
    """
    Extracts the product image URL from the given BeautifulSoup object.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object containing the parsed HTML for a product.

    Returns:
        Optional[str]: The product image URL or None if not found.
    """
    image_element = soup.find('img')
    if image_element and 'src' in image_element.attrs:
        return f"https:{image_element['src']}"
    return None
