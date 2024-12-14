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
    return soup.find_all('div', class_='product-cell-container')


def get_product_url(soup: BeautifulSoup) -> Optional[str]:
    """
    Extracts the product URL from the given BeautifulSoup object.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object containing the parsed HTML for a product.

    Returns:
        Optional[str]: The product URL or None if not found.
    """
    product_link_element = soup.find('a', class_='absolute-link product-link')
    return product_link_element['href'] if product_link_element and 'href' in product_link_element.attrs else None


def get_title(soup: BeautifulSoup) -> Optional[str]:
    """
    Extracts the product title from the given BeautifulSoup object.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object containing the parsed HTML for a product.

    Returns:
        Optional[str]: The product title or None if not found.
    """
    title_element = soup.find('div', class_='product-title')
    return title_element.get_text().strip() if title_element else None


def get_price(soup: BeautifulSoup) -> Optional[str]:
    """
    Extracts the product price from the given BeautifulSoup object.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object containing the parsed HTML for a product.

    Returns:
        Optional[str]: The product price or None if not found.
    """
    price_element = soup.find('span', class_='price')
    return price_element.get_text().strip() if price_element else None


def get_image_url(soup: BeautifulSoup) -> Optional[str]:
    """
    Extracts the product image URL from the given BeautifulSoup object.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object containing the parsed HTML for a product.

    Returns:
        Optional[str]: The product image URL or None if not found.
    """
    image_element = soup.find('img', itemprop='image')
    return image_element['src'] if image_element and 'src' in image_element.attrs else None


def get_rating(soup: BeautifulSoup) -> Optional[str]:
    """
    Extracts the product rating from the given BeautifulSoup object.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object containing the parsed HTML for a product.

    Returns:
        Optional[str]: The product rating or None if not found.
    """
    rating_element = soup.find('meta', itemprop='ratingValue')
    return rating_element['content'] if rating_element and 'content' in rating_element.attrs else None


def get_review_count(soup: BeautifulSoup) -> Optional[int]:
    """
    Extracts the product review count from the given BeautifulSoup object.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object containing the parsed HTML for a product.

    Returns:
        Optional[int]: The product review count or None if not found.
    """
    review_element = soup.find('meta', itemprop='reviewCount')
    return int(review_element['content']) if review_element and 'content' in review_element.attrs else None
