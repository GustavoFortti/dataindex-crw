import os
from typing import Any, Callable, Dict, List, Optional

import html2text
import pandas as pd
from bs4 import BeautifulSoup

from src.jobs.pipeline import JobBase
from src.lib.extract.crawler import crawler
from src.lib.transform.product_definition import create_product_cols
from src.lib.utils.file_system import (file_modified_within_x_hours, read_file,
                                       save_file, save_json)
from src.lib.utils.log import message
from src.lib.utils.general_functions import flatten_list


def create_product_info_columns(df: pd.DataFrame, job_base: JobBase) -> pd.DataFrame:
    """
    Creates additional product information columns in the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing product information.
        job_base (JobBase): An instance of JobBase containing job configurations.

    Returns:
        pd.DataFrame: Updated DataFrame with additional product columns.
    """
    message("loading product data")
    if job_base.mode == "prd":
        extract_metadata_from_page(df, job_base)

    message("CREATING columns [product_definition, product_collection]")
    return create_product_cols(job_base, df)


def extract_metadata_from_page(df: pd.DataFrame, job_base: JobBase) -> None:
    """
    Iterates over each row in the DataFrame and extracts product metadata.

    Args:
        df (pd.DataFrame): DataFrame containing product information.
        job_base (JobBase): An instance of JobBase containing job configurations.
    """
    for idx, row in df.iterrows():
        ref: str = str(row['ref'])
        product_url: str = row['product_url']

        # Define file paths
        products_path: str = job_base.products_path
        description_path: str = f"{products_path}/{ref}_description.txt"
        images_path: str = f"{products_path}/{ref}_images.json"
        page_path: str = f"{products_path}/{ref}.txt"

        # Try to load the product page HTML; update if it doesn't exist
        html_text: Optional[str] = fetch_product_page_html(job_base, page_path, product_url)

        if "text" in job_base.page.html_metadata_type:
            # Extract description based on configured tags
            description: Optional[List[str]] = extract_element_from_html(
                html_text, job_base.page.html_description_path, get_product_description
            )

            if not description:
                html_text = fetch_product_page_html(job_base, page_path, product_url, force=True)
                description = extract_element_from_html(
                    html_text, job_base.page.html_description_path, get_product_description
                )

            # If description was extracted, format and save the file
            if description:
                description_text = " ".join(description)
                formatted_description: str = format_product_description(row, description_text)
                message(f"Saving description for ref {ref}")
                save_file(formatted_description, description_path)

        if "image" in job_base.page.html_metadata_type:
            url_images: Optional[List[str]] = extract_element_from_html(
                html_text, job_base.page.html_images_list, get_product_url_images
            )
            if url_images:
                url_images = flatten_list(url_images)
                if job_base.page.html_remove_first_image_from_list:
                    url_images = url_images[1:]

                save_json(images_path, {"url_images": url_images})


def fetch_product_page_html(
    job_base: JobBase, page_path: str, product_url: str, force: bool = False
) -> Optional[str]:
    """
    Attempts to read the HTML of the product page; updates the page if the file is not found.

    Args:
        job_base (JobBase): An instance of JobBase containing job configurations.
        page_path (str): Path to the product's HTML file.
        product_url (str): URL of the product.
        force (bool, optional): Whether to force update the HTML. Defaults to False.

    Returns:
        Optional[str]: HTML text of the product page, or None if not found.
    """
    html_text: Optional[str] = read_file(page_path)

    is_page_updated: bool = file_modified_within_x_hours(page_path, 6)
    if (not html_text or force) and not is_page_updated:
        # Update metadata and try again
        update_old_products_metadata_by_url(job_base, product_url)
        html_text = read_file(page_path)

    return html_text


def extract_element_from_html(
    html_text: Optional[str],
    tags_map: List[Dict[str, str]],
    get_function: Callable[[str, Dict[str, str]], Optional[Any]],
) -> Optional[List[Any]]:
    """
    Extracts elements from the HTML using the configured tags.

    Args:
        html_text (Optional[str]): HTML text of the product page.
        tags_map (List[Dict[str, str]]): List of tag mappings containing selector paths.
        get_function (Callable): Function to extract elements from HTML given a tag map.

    Returns:
        Optional[List[Any]]: List of extracted elements, or None if none found.
    """
    elements: List[Any] = []

    if html_text:
        for tag_map in tags_map:
            element: Optional[Any] = get_function(html_text, tag_map)
            if element:
                elements.append(element)

    return elements if elements else None


def format_product_description(row: pd.Series, description: str) -> str:
    """
    Formats the product description by including the title and brand.

    Args:
        row (pd.Series): Row from the DataFrame containing product information.
        description (str): Description extracted from the HTML.

    Returns:
        str: Formatted product description.
    """
    return f"Product: {row['title']}\nSupplier Website: {row['brand']}\nDescription:\n{description}"


def get_product_description(html_text: str, tag_map: Dict[str, str]) -> Optional[str]:
    """
    Extracts the product description from HTML using a tag selector.

    Args:
        html_text (str): HTML text of the product page.
        tag_map (Dict[str, str]): Tag mapping containing the selector path ('path').

    Returns:
        Optional[str]: Plain text product description, or None if not found or invalid.
    """
    try:
        soup = BeautifulSoup(html_text, 'html.parser')

        # Select HTML content based on the path specified in tag_map
        html_content = soup.select_one(tag_map['path'])
        if not html_content:
            return None

        # Convert HTML to plain text ignoring links, images, and emphasis
        html_converter = html2text.HTML2Text()
        html_converter.ignore_links = True
        html_converter.ignore_images = True
        html_converter.ignore_emphasis = True
        html_converter.body_width = 0

        plain_text: str = html_converter.handle(str(html_content))

        # Check if the text is too short; return None if so
        if len(plain_text.strip()) < 10:
            return None

        return plain_text.strip()

    except Exception as e:
        print(f"Error in function get_product_description: {e}")
        return None


def get_product_url_images(html_text: str, tag_map: Dict[str, str]) -> Optional[List[str]]:
    """
    Extracts image URLs from the product HTML using a tag selector.

    Args:
        html_text (str): HTML text of the product page.
        tag_map (Dict[str, str]): Tag mapping containing the selector path ('path').

    Returns:
        Optional[List[str]]: List of image URLs, or None if not found.
    """
    try:
        # Create BeautifulSoup object
        soup = BeautifulSoup(html_text, 'html.parser')

        # Select all elements that match the path in tag_map
        html_content = soup.select(tag_map['path'])

        if not html_content:
            return None

        # Capture all image links
        image_urls: List[str] = []
        for element in html_content:
            # Look for <img> tags within the element
            img_tags = element.find_all('img')
            for img_tag in img_tags:
                if img_tag and 'src' in img_tag.attrs:
                    img_src: str = img_tag['src']
                    if img_src:
                        img_src = img_src.replace("//www.", "https://www.")
                        image_urls.append(img_src)

        return image_urls if image_urls else None

    except Exception as e:
        print(f"Error in function get_product_url_images: {e}")
        return None


def update_old_products_metadata_by_url(job_base: JobBase, url: str) -> None:
    """
    Updates the metadata of an old product page by URL if there are errors in tags.

    Args:
        job_base (JobBase): An instance of JobBase containing job configurations.
        url (str): The URL of the product to update.
    """
    message("Updating old page by reference if page has errors in tags")
    job_base.page.html_scroll_page = True
    job_base.check_if_job_is_ready = False
    job_base.update_all_products = False
    job_base.update_all_products_metadata = True

    message(f"Updating URL: {url}")
    crawler(job_base, url)
