import ast
import json
import random
import threading
import time
from typing import Tuple
from urllib.parse import parse_qs, urlparse

import pandas as pd
import requests

from src.config.setup.shopify import BASE_URL, HEADERS
from src.lib.load.components.cupom_code_button import cupom_code_button
from src.lib.load.components.redirecionamento_button import redirecionamento_button
from src.lib.load.components.generate_price_chart import generate_price_chart
from src.lib.utils.file_system import file_or_path_exists, read_file, read_json
from src.lib.utils.log import message
from src.jobs.pipeline import JobBase

# Constants
MAX_RETRIES: int = 3  # Maximum number of retries
WAIT_SECONDS: int = 3  # Wait time between retries in seconds


class RateLimitedSession(requests.Session):
    """
    A requests.Session subclass that enforces rate limiting and retry logic for HTTP requests.
    """
    def __init__(
        self, 
        max_calls_per_second: float, 
        max_retries: int, 
        wait_seconds: int, 
        *args, 
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.min_interval: float = 1.0 / float(max_calls_per_second)
        self.last_call: float = 0.0
        self.lock: threading.Lock = threading.Lock()
        self.max_retries: int = max_retries
        self.wait_seconds: int = wait_seconds

    def request(self, method: str, url: str, *args, **kwargs) -> requests.Response:
        """
        Override the request method to add rate limiting and retry logic.
        
        Args:
            method (str): HTTP method (GET, POST, etc.).
            url (str): The URL to request.
        
        Returns:
            requests.Response: The HTTP response.
        """
        retries: int = 0
        while True:
            with self.lock:
                elapsed: float = time.time() - self.last_call
                left_to_wait: float = self.min_interval - elapsed
                if left_to_wait > 0:
                    time.sleep(left_to_wait)
                self.last_call = time.time()
            response: requests.Response = super().request(method, url, *args, **kwargs)
            if response.status_code == 429:
                retries += 1
                if retries >= self.max_retries:
                    message(f"Maximum retries reached for URL '{url}'. Status 429.")
                    response.raise_for_status()
                else:
                    message(
                        f"Error 429 on URL '{url}'. Attempt {retries}/{self.max_retries}. "
                        f"Waiting {self.wait_seconds} seconds before retrying."
                    )
                    time.sleep(self.wait_seconds)
            else:
                return response


def test_connection() -> bool:
    """
    Tests the connection to the Shopify API.
    
    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    session: RateLimitedSession = RateLimitedSession(
        max_calls_per_second=2, 
        max_retries=MAX_RETRIES, 
        wait_seconds=WAIT_SECONDS
    )
    session.headers.update(HEADERS)
    url: str = f"{BASE_URL}products.json"
    response: requests.Response = session.get(url)
    
    if response.status_code == 200:
        message("Connection successful! The Shopify API is accessible.")
        return True
    else:
        message(f"Connection error: {response.status_code} - {response.text}")
        return False


def format_product_for_shopify(job_base: JobBase, row: pd.Series) -> Tuple[dict, dict]:
    """
    Formats product data into the structure expected by the Shopify API.
    
    Args:
        job_base (JobBase): The job base containing source data path.
        row (pd.Series): A row from the DataFrame containing product information.
    
    Returns:
        Tuple[dict, dict]: 
            - product_data: Dictionary containing product data.
            - variant_data: Dictionary containing variant data.
    """
    try:
        body_html: str = ""
        
        # Determine the product URL
        product_url: str = (
            row.get("product_url_affiliated")
            if pd.notna(row.get("product_url_affiliated"))
            else row.get("product_url")
        )
        body_html += redirecionamento_button(product_url)
        
        # Add coupon code button if available
        if pd.notna(row["cupom_code"]) and pd.notna(row["discount_percent_cupom"]):
            body_html += cupom_code_button(row["cupom_code"], row["discount_percent_cupom"])
        
        # Add AI-generated product description if available
        description_ai: str | None = None
        path_description_ai: str = f"{job_base.src_data_path}/{row['page_name']}/products/{row['ref']}_description_ai.txt"
        if file_or_path_exists(path_description_ai):
            description_ai = read_file(path_description_ai)
        
        if description_ai:
            formatted_description: str = f"<br>{description_ai.replace('\n', '<br>')}"
            body_html += f'''
                <div id="product-description">
                    <br>
                    <strong>Product Description</strong>
                    {formatted_description}
                </div>
            '''
        
        # Add price chart if prices data is available
        check_prices: bool = pd.notna(row['prices'])
        if check_prices and isinstance(row['prices'], str):
            row['prices'] = json.loads(row['prices'].replace("'", '"'))
            
            if check_prices and isinstance(row['prices'], list) and len(row['prices']) > 1:
                price_chart_html: str = generate_price_chart(row['prices'])
                body_html += price_chart_html
        
        product_type: str = row['product_tags']
        product_data: dict = {
            "title": row['title_extract'],
            "body_html": body_html,
            "vendor": row['brand'].title(),
            "tags": product_type if pd.notna(product_type) else "Others",
            "product_type": "",
        }
        
        variant_data: dict = {
            "price": str(row['price_numeric']),
            "sku": row['ref'],
            "inventory_quantity": 1,
            "weight": float(row['quantity']) if pd.notna(row['quantity']) else None,
            "weight_unit": "g" if pd.notna(row['quantity']) else None,
            "compare_at_price": str(row['compare_at_price']) if pd.notna(row['compare_at_price']) else None,
            "fulfillment_service": 'manual',
            "inventory_management": 'shopify',
        }
        
        return product_data, variant_data
    except Exception as e:
        message(f"Error formatting product '{row['title_extract']}': {e}")
        return {}, {}


def get_all_skus_with_product_ids() -> dict:
    """
    Retrieves all SKUs for all Shopify products, including product_id, vendor, and inventory_item_id.
    
    Returns:
        dict: A dictionary where keys are SKUs and values are lists of dictionaries containing
              'variant_id', 'product_id', 'vendor', and 'inventory_item_id'.
    """
    try:
        session: RateLimitedSession = RateLimitedSession(
            max_calls_per_second=2, 
            max_retries=MAX_RETRIES, 
            wait_seconds=WAIT_SECONDS
        )
        session.headers.update(HEADERS)

        sku_variants: dict = {}  # Dictionary to map SKUs to a list of variants
        limit: int = 250
        params: dict = {
            "limit": limit,
            "fields": "id,variants,vendor"
        }
        next_page_info: str | None = None
        has_more: bool = True

        # Step 1: Retrieve all products and variants
        while has_more:
            if next_page_info:
                params["page_info"] = next_page_info

            response: requests.Response = session.get(f"{BASE_URL}products.json", params=params)

            if response.status_code != 200:
                message(f"Error fetching products: {response.status_code} - {response.text}")
                return sku_variants

            products: list = response.json().get('products', [])

            for product in products:
                product_id: int = product.get('id')
                vendor: str = product.get('vendor', '')
                for variant in product.get('variants', []):
                    variant_id: int = variant.get('id')
                    sku: str = variant.get('sku', '').strip()
                    inventory_item_id: int = variant.get('inventory_item_id')
                    if sku:
                        if sku not in sku_variants:
                            sku_variants[sku] = []
                        sku_variants[sku].append({
                            'variant_id': variant_id,
                            'product_id': product_id,
                            'vendor': vendor,
                            'inventory_item_id': inventory_item_id
                        })

            # Check if there are more pages using Link headers
            link_header: str | None = response.headers.get('Link')
            if link_header:
                links: list = link_header.split(',')
                next_page_info = None  # Reset for the next iteration
                for link in links:
                    if 'rel="next"' in link:
                        # Extract the page_info value from the URL
                        start: int = link.find('<') + 1
                        end: int = link.find('>')
                        url: str = link[start:end]
                        parsed_url: urlparse = urlparse(url)
                        query_params: dict = parse_qs(parsed_url.query)
                        next_page_info = query_params.get('page_info', [None])[0]
                        break
                if next_page_info:
                    has_more = True
                else:
                    has_more = False
            else:
                has_more = False  # No more pages

        return sku_variants

    except Exception as e:
        message(f"Error fetching SKUs: {e}")
        return {}


def find_duplicate_skus(sku_data: dict) -> dict:
    """
    Identifies duplicate SKUs in the SKU dictionary.
    
    Args:
        sku_data (dict): The dictionary returned by get_all_skus_with_product_ids.
    
    Returns:
        dict: A dictionary where keys are duplicated SKUs and values are lists of variants 
              (with 'variant_id', 'product_id', 'vendor') associated with that SKU.
    """
    duplicate_skus: dict = {}

    for sku, variants in sku_data.items():
        if len(variants) > 1:
            # If the SKU has more than one variant, it's considered duplicated
            duplicate_skus[sku] = variants

    return duplicate_skus


def delete_duplicates_products(duplicate_skus: dict) -> None:
    """
    Deletes duplicate products based on duplicated SKUs.
    
    Args:
        duplicate_skus (dict): Dictionary of duplicated SKUs and their associated variants.
    """
    if duplicate_skus:
        message(f"Found {len(duplicate_skus)} duplicated SKUs.")
        session: RateLimitedSession = RateLimitedSession(
            max_calls_per_second=2, 
            max_retries=MAX_RETRIES, 
            wait_seconds=WAIT_SECONDS
        )
        session.headers.update(HEADERS)
        for sku, variants in duplicate_skus.items():
            for variant in variants:
                product_id: int = variant['product_id']
                variant_id: int = variant['variant_id']
                
                # Check the number of remaining variants in the product
                variant_count: int = get_variant_count(session, product_id)
                
                if variant_count > 1:
                    # If the product has more than one variant, only the duplicate variant is deleted
                    delete_variant(session, variant_id)
                    message(f"Variant {variant_id} of product {product_id} deleted.")
                else:
                    # If the product has only one variant, the product itself is deleted
                    delete_product(session, product_id)
                    message(f"Product {product_id} deleted because it had only one variant.")

        message("Duplicate SKUs removal process completed.")
    else:
        message("No duplicated SKUs found.")


def delete_extra_skus(skus_to_delete: list) -> None:
    """
    Deletes extra SKUs that are not present in the reference list.
    
    Args:
        skus_to_delete (list): List of dictionaries containing 'sku', 'variant_id', and 'product_id' to delete.
    """
    if skus_to_delete:
        message(f"Found {len(skus_to_delete)} SKUs to delete.")
        session: RateLimitedSession = RateLimitedSession(
            max_calls_per_second=2, 
            max_retries=MAX_RETRIES, 
            wait_seconds=WAIT_SECONDS
        )
        session.headers.update(HEADERS)
        for item in skus_to_delete:
            product_id: int = item['product_id']
            variant_id: int = item['variant_id']
            sku: str = item['sku']

            # Check the number of remaining variants in the product
            variant_count: int = get_variant_count(session, product_id)

            if variant_count > 1:
                # If the product has more than one variant, only the variant is deleted
                delete_variant(session, variant_id)
                message(f"Variant {variant_id} of product {product_id} (SKU {sku}) deleted.")
            else:
                # If the product has only one variant, the product is deleted
                delete_product(session, product_id)
                message(f"Product {product_id} (SKU {sku}) deleted because it had only one variant.")

        message("SKU deletion process completed.")
    else:
        message("No SKUs to delete.")


def find_extra_skus_to_delete(sku_data: dict, refs: list, brand: str) -> list:
    """
    Finds SKUs that exist in Shopify but are not in the reference list for a specific brand.
    
    Args:
        sku_data (dict): Dictionary returned by get_all_skus_with_product_ids.
        refs (list): List of SKUs that should exist.
        brand (str): The 'vendor' (brand) to filter.
    
    Returns:
        list: List of dictionaries with 'sku', 'variant_id', and 'product_id' that need to be deleted.
    """
    skus_to_delete: list = []
    for sku, variants in sku_data.items():
        for variant in variants:
            if variant['vendor'].lower() == brand.lower():
                if sku not in refs:
                    skus_to_delete.append({
                        'sku': sku,
                        'variant_id': variant['variant_id'],
                        'product_id': variant['product_id']
                    })
    return skus_to_delete


def get_variant_count(session: RateLimitedSession, product_id: int) -> int:
    """
    Retrieves the number of variants for a given product.
    
    Args:
        session (RateLimitedSession): Authenticated request session.
        product_id (int): The ID of the product.
    
    Returns:
        int: Number of variants in the product.
    """
    response: requests.Response = session.get(f"{BASE_URL}products/{product_id}.json", params={"fields": "variants"})
    if response.status_code == 200:
        product: dict = response.json().get('product', {})
        variants: list = product.get('variants', [])
        return len(variants)
    else:
        message(f"Error fetching variants for product {product_id}: {response.status_code} - {response.text}")
        return 0


def delete_variant(session: RateLimitedSession, variant_id: int) -> None:
    """
    Deletes a specific variant.
    
    Args:
        session (RateLimitedSession): Authenticated request session.
        variant_id (int): The ID of the variant to delete.
    """
    response: requests.Response = session.delete(f"{BASE_URL}variants/{variant_id}.json")
    if response.status_code != 200:
        message(f"Error deleting variant {variant_id}: {response.status_code} - {response.text}")


def delete_product(session: RateLimitedSession, product_id: int) -> None:
    """
    Deletes a specific product.
    
    Args:
        session (RateLimitedSession): Authenticated request session.
        product_id (int): The ID of the product to delete.
    """
    response: requests.Response = session.delete(f"{BASE_URL}products/{product_id}.json")
    if response.status_code != 200:
        message(f"Error deleting product {product_id}: {response.status_code} - {response.text}")


def update_product_by_sku(
    job_base: JobBase, 
    sku: str, 
    product_data: dict, 
    variant_data: dict, 
    row: pd.Series, 
    sku_data: dict
) -> bool:
    """
    Updates a product in Shopify based on its SKU.
    
    Args:
        job_base (JobBase): The job base containing source data path.
        sku (str): The SKU of the product.
        product_data (dict): The formatted product data for updating.
        variant_data (dict): The formatted variant data for updating.
        row (pd.Series): A row from the DataFrame containing product information.
        sku_data (dict): Dictionary of SKUs and their associated variants.
    
    Returns:
        bool: True if the update was successful, False otherwise.
    """
    session: RateLimitedSession = RateLimitedSession(
        max_calls_per_second=2, 
        max_retries=MAX_RETRIES, 
        wait_seconds=WAIT_SECONDS
    )
    session.headers.update(HEADERS)

    if sku in sku_data:
        variants: list = sku_data[sku]
        product_id: int = variants[0]['product_id']
        variant_id: int = variants[0]['variant_id']
        # Update the product
        product_success: bool = update_product(session, product_id, product_data)
        # Extract quantity_sold from row
        if 'product_score' in row and pd.notna(row['product_score']):
            quantity_sold: int = random.randint(row['product_score'], row['product_score'] * 2)
        else:
            quantity_sold = 1
        # Update the variant
        variant_success: bool = update_variant(session, product_id, variant_id, variant_data, quantity_sold)
        
        product_images: list = []
        path_product_images: str = f"{job_base.src_data_path}/{row['page_name']}/products/{row['ref']}_images.json"
        message(f"Reading {path_product_images}")
        if file_or_path_exists(path_product_images):
            product_images = read_json(path_product_images)['url_images']
        product_images.insert(0, row['image_url'])
        
        # Update images
        images_success: bool = update_images(session, product_id, product_images)
        # Update collections only if 'collections' exists
        if 'collections' in row and pd.notna(row['collections']):
            collections_success: bool = update_collections(session, product_id, row)
        else:
            collections_success = True  # No collections to update

        return product_success and variant_success and images_success and collections_success
    else:
        message(f"SKU '{sku}' not found in Shopify data.")
        return False


def update_product(session: RateLimitedSession, product_id: int, product_data: dict) -> bool:
    """
    Updates a product in Shopify.
    
    Args:
        session (RateLimitedSession): Authenticated request session.
        product_id (int): The ID of the product to update.
        product_data (dict): The product data to update.
    
    Returns:
        bool: True if the update was successful, False otherwise.
    """
    url: str = f"{BASE_URL}products/{product_id}.json"
    product_data['id'] = product_id
    response: requests.Response = session.put(url, json={"product": product_data})

    if response.status_code == 200:
        message(f"Product {product_id} updated successfully.")
        return True
    else:
        try:
            error_message: str = response.json().get('errors', response.text)
        except json.decoder.JSONDecodeError:
            error_message = response.text
        message(f"Error updating product {product_id}: {response.status_code} - {error_message}")
        return False


def update_variant(
    session: RateLimitedSession, 
    product_id: int, 
    variant_id: int, 
    variant_data: dict, 
    quantity_sold: int
) -> bool:
    """
    Updates a variant of a product in Shopify and updates its inventory level.
    
    Args:
        session (RateLimitedSession): Authenticated request session.
        product_id (int): The ID of the product.
        variant_id (int): The ID of the variant to update.
        variant_data (dict): The variant data to update.
        quantity_sold (int): The quantity sold to update inventory level.
    
    Returns:
        bool: True if both the variant and inventory level were successfully updated, False otherwise.
    """
    url: str = f"{BASE_URL}variants/{variant_id}.json"
    variant_data['id'] = variant_id
    variant_data['fulfillment_service'] = 'manual'
    variant_data['inventory_management'] = 'shopify'

    response: requests.Response = session.put(url, json={"variant": variant_data})

    if response.status_code == 200:
        message(f"Variant {variant_id} of product {product_id} updated successfully.")
        
        # Get the inventory_item_id of the variant
        variant_info: dict = response.json().get('variant', {})
        inventory_item_id: int | None = variant_info.get('inventory_item_id')
        
        if inventory_item_id:
            # Update the inventory level
            success: bool = update_inventory_level(session, inventory_item_id, quantity_sold)
            return success
        else:
            message(f"Could not obtain inventory_item_id for variant {variant_id}.")
            return False
    else:
        try:
            error_message: str = response.json().get('errors', response.text)
        except ValueError:
            error_message = response.text
        message(f"Error updating variant {variant_id} of product {product_id}: {response.status_code} - {error_message}")
        return False


def enable_inventory_tracking(session: RateLimitedSession, inventory_item_id: int) -> bool:
    """
    Enables inventory tracking for the given inventory item.
    
    Args:
        session (RateLimitedSession): Authenticated request session.
        inventory_item_id (int): The ID of the inventory item.
    
    Returns:
        bool: True if tracking was successfully enabled, False otherwise.
    """
    url: str = f"{BASE_URL}inventory_items/{inventory_item_id}.json"
    payload: dict = {
        "inventory_item": {
            "id": inventory_item_id,
            "tracked": True  # Enable inventory tracking
        }
    }

    response: requests.Response = session.put(url, json=payload)
    if response.status_code == 200:
        message(f"Inventory tracking enabled for item {inventory_item_id}.")
        return True
    else:
        error_message: str = response.text
        message(f"Error enabling inventory tracking for item {inventory_item_id}: {response.status_code} - {error_message}")
        return False


def update_inventory_level(session: RateLimitedSession, inventory_item_id: int, quantity_sold: int) -> bool:
    """
    Updates the inventory level for a given inventory item.
    
    Args:
        session (RateLimitedSession): Authenticated request session.
        inventory_item_id (int): The ID of the inventory item.
        quantity_sold (int): The quantity sold to adjust inventory level.
    
    Returns:
        bool: True if the inventory level was successfully updated, False otherwise.
    """
    # Obtain the location_id
    location_id: int | None = get_location_id(session)
    if not location_id:
        message("Could not obtain location_id.")
        return False

    # Enable inventory tracking if not already enabled
    if not enable_inventory_tracking(session, inventory_item_id):
        message(f"Could not enable inventory tracking for item {inventory_item_id}.")
        return False

    # Set the new inventory level to 1
    new_quantity: int = 1

    # Update the inventory level to always be 1
    payload: dict = {
        "location_id": location_id,
        "inventory_item_id": inventory_item_id,
        "available": new_quantity
    }
    response: requests.Response = session.post(f"{BASE_URL}inventory_levels/set.json", json=payload)
    if response.status_code == 200:
        message(f"Inventory level updated for inventory_item_id {inventory_item_id} at location {location_id}. New quantity: {new_quantity}")
        return True
    else:
        error_message: str = response.text
        message(f"Error updating inventory level for inventory_item_id {inventory_item_id} at location {location_id}: {response.status_code} - {error_message}")
        return False


def get_location_id(session: RateLimitedSession) -> int | None:
    """
    Retrieves the location ID for inventory management.
    
    Args:
        session (RateLimitedSession): Authenticated request session.
    
    Returns:
        int | None: The ID of the first location if available, otherwise None.
    """
    response: requests.Response = session.get(f"{BASE_URL}locations.json")
    if response.status_code == 200:
        locations: list = response.json().get('locations', [])
        if locations:
            # For simplicity, use the first location
            return locations[0]['id']
        else:
            message("No locations found.")
            return None
    else:
        message(f"Error fetching locations: {response.status_code} - {response.text}")
        return None


def get_current_inventory_level(session: RateLimitedSession, inventory_item_id: int, location_id: int) -> int | None:
    """
    Retrieves the current inventory level for a given inventory item and location.
    
    Args:
        session (RateLimitedSession): Authenticated request session.
        inventory_item_id (int): The ID of the inventory item.
        location_id (int): The ID of the location.
    
    Returns:
        int | None: The available inventory level if found, otherwise None.
    """
    params: dict = {
        "inventory_item_ids": inventory_item_id,
        "location_ids": location_id
    }
    response: requests.Response = session.get(f"{BASE_URL}inventory_levels.json", params=params)
    if response.status_code == 200:
        inventory_levels: list = response.json().get('inventory_levels', [])
        if inventory_levels:
            available: int = inventory_levels[0].get('available')
            return available
        else:
            message(f"Inventory level not found for inventory_item_id {inventory_item_id} at location {location_id}.")
            return None
    else:
        message(f"Error fetching inventory level: {response.status_code} - {response.text}")
        return None


def update_images(session: RateLimitedSession, product_id: int, image_urls: list) -> bool:
    """
    Updates the images of a product in Shopify by replacing current images with new ones.
    
    Args:
        session (RateLimitedSession): Authenticated request session.
        product_id (int): The ID of the product.
        image_urls (list): List of image URLs to set for the product.
    
    Returns:
        bool: True if images were successfully updated, False otherwise.
    """
    try:
        # Step 1: Retrieve existing images
        response: requests.Response = session.get(f"{BASE_URL}products/{product_id}/images.json")
        if response.status_code != 200:
            message(f"Error fetching current images for product {product_id}: {response.status_code} - {response.text}")
            return False
        existing_images: list = response.json().get('images', [])

        # Step 2: Delete existing images
        for image in existing_images:
            image_id: int = image.get('id')
            del_response: requests.Response = session.delete(f"{BASE_URL}products/{product_id}/images/{image_id}.json")
            if del_response.status_code not in [200, 204]:
                try:
                    error_message: str = del_response.json().get('errors', del_response.text)
                except json.decoder.JSONDecodeError:
                    error_message = del_response.text
                message(f"Error deleting image {image_id} of product {product_id}: {del_response.status_code} - {error_message}")
                # Continue attempting to delete other images
            else:
                message(f"Image {image_id} of product {product_id} deleted successfully.")

        # Step 3: Prepare and add new images
        for url in image_urls:
            # Ensure the URL starts with 'http://' or 'https://'
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url  # Prepend 'https://'

            image_payload: dict = {"image": {"src": url}}
            add_response: requests.Response = session.post(f"{BASE_URL}products/{product_id}/images.json", json=image_payload)
            if add_response.status_code not in [200, 201]:
                try:
                    error_message: str = add_response.json().get('errors', add_response.text)
                except json.decoder.JSONDecodeError:
                    error_message = add_response.text
                message(f"Error adding image to product {product_id}: {add_response.status_code} - {error_message}")
                # Continue attempting to add other images
            else:
                added_image: dict = add_response.json().get('image', {})
                message(f"Image {added_image.get('id')} added to product {product_id} successfully.")

        message(f"Images for product {product_id} updated successfully.")
        return True

    except Exception as e:
        message(f"Error updating images for product {product_id}: {e}")
        return False


def update_collections(session: RateLimitedSession, product_id: int, row: pd.Series) -> bool:
    """
    Updates the collections of a product by adding and removing as necessary.
    
    Args:
        session (RateLimitedSession): Authenticated request session.
        product_id (int): The ID of the product.
        row (pd.Series): A row from the DataFrame containing product information.
    
    Returns:
        bool: True if collections were successfully updated, False otherwise.
    """
    try:
        collections_field = row['collections']
        if pd.isna(collections_field):
            desired_collections: list = ["No Collection"]
        elif isinstance(collections_field, list):
            desired_collections = collections_field
        elif isinstance(collections_field, str):
            try:
                desired_collections = ast.literal_eval(collections_field)
            except (ValueError, SyntaxError):
                desired_collections = [collections_field]
        else:
            desired_collections = [collections_field]
        desired_collections = [str(c).strip() for c in desired_collections]

        success: bool = True

        # Step 1: Retrieve all current collections of the product
        current_collections: list = []
        page_info: str | None = None
        while True:
            params: dict = {
                "product_id": product_id,
                "fields": "collection_id",
                "limit": 250
            }
            if page_info:
                params["page_info"] = page_info

            response: requests.Response = session.get(f"{BASE_URL}collects.json", params=params)
            if response.status_code != 200:
                message(f"Error fetching current collections for product {product_id}: {response.status_code} - {response.text}")
                success = False
                break

            collects: list = response.json().get('collects', [])
            for collect in collects:
                current_collections.append(collect['collection_id'])

            # Check pagination
            link_header: str | None = response.headers.get('Link')
            if link_header and 'rel="next"' in link_header:
                links: list = link_header.split(',')
                for link in links:
                    if 'rel="next"' in link:
                        start: int = link.find('<') + 1
                        end: int = link.find('>')
                        url: str = link[start:end]
                        parsed_url: urlparse = urlparse(url)
                        query_params: dict = parse_qs(parsed_url.query)
                        page_info = query_params.get('page_info', [None])[0]
                        break
            else:
                break

        # Step 2: Map desired collection titles to IDs
        desired_collection_ids: list = []
        for collection_title in desired_collections:
            # Search for the collection, create it if it does not exist
            response: requests.Response = session.get(f"{BASE_URL}custom_collections.json", params={"title": collection_title})
            if response.status_code != 200:
                message(f"Error searching collections: {response.status_code} - {response.text}")
                success = False
                continue

            collections: list = response.json().get('custom_collections', [])
            if not collections:
                # Create the collection
                collection_payload: dict = {
                    "custom_collection": {
                        "title": collection_title,
                        "published": True
                    }
                }
                create_response: requests.Response = session.post(f"{BASE_URL}custom_collections.json", json=collection_payload)
                if create_response.status_code != 201:
                    try:
                        error_message: str = create_response.json().get('errors', create_response.text)
                    except json.decoder.JSONDecodeError:
                        error_message = create_response.text
                    message(f"Error creating collection '{collection_title}': {create_response.status_code} - {error_message}")
                    success = False
                    continue
                collection_id: int = create_response.json()['custom_collection']['id']
                message(f"Collection '{collection_title}' created with ID {collection_id}.")
            else:
                collection_id: int = collections[0]['id']
            desired_collection_ids.append(collection_id)

        # Step 3: Determine collections to add and remove
        collections_to_add: set = set(desired_collection_ids) - set(current_collections)
        collections_to_remove: set = set(current_collections) - set(desired_collection_ids)

        # Step 4: Add product to new collections
        for collection_id in collections_to_add:
            collect_payload: dict = {
                "collect": {
                    "product_id": product_id,
                    "collection_id": collection_id
                }
            }
            add_response: requests.Response = session.post(f"{BASE_URL}collects.json", json=collect_payload)
            if add_response.status_code == 201:
                message(f"Product {product_id} added to collection ID {collection_id}.")
            else:
                try:
                    error_message: str = add_response.json().get('errors', add_response.text)
                except json.decoder.JSONDecodeError:
                    error_message = add_response.text
                message(f"Error adding product {product_id} to collection ID {collection_id}: {add_response.status_code} - {error_message}")
                success = False

        # Step 5: Remove product from collections it should no longer belong to
        for collection_id in collections_to_remove:
            # Find the collect ID
            response: requests.Response = session.get(
                f"{BASE_URL}collects.json", 
                params={"collection_id": collection_id, "product_id": product_id}
            )
            if response.status_code != 200:
                message(f"Error fetching collect for product {product_id} and collection {collection_id}: {response.status_code} - {response.text}")
                success = False
                continue
            collects: list = response.json().get('collects', [])
            if collects:
                collect_id: int = collects[0]['id']
                # Delete the collect
                delete_response: requests.Response = session.delete(f"{BASE_URL}collects/{collect_id}.json")
                if delete_response.status_code in [200, 204]:
                    message(f"Product {product_id} removed from collection ID {collection_id}.")
                else:
                    try:
                        error_message: str = delete_response.json().get('errors', delete_response.text)
                    except json.decoder.JSONDecodeError:
                        error_message = delete_response.text
                    message(f"Error removing product {product_id} from collection ID {collection_id}: {delete_response.status_code} - {error_message}")
                    success = False

        return success
    except Exception as e:
        message(f"Error updating collections for product {product_id}: {e}")
        return False


def create_product(product_data: dict) -> dict | None:
    """
    Creates a new product in Shopify with the provided data.
    
    Args:
        product_data (dict): The formatted product data for creation.
    
    Returns:
        dict | None: The created product returned by the Shopify API, or None if there was an error.
    """
    session: RateLimitedSession = RateLimitedSession(
        max_calls_per_second=2, 
        max_retries=MAX_RETRIES, 
        wait_seconds=WAIT_SECONDS
    )
    session.headers.update(HEADERS)

    url: str = f"{BASE_URL}products.json"
    
    # Make the POST request to create the product
    response: requests.Response = session.post(url, json={"product": product_data})
    
    if response.status_code == 201:
        message(f"Product '{product_data.get('title')}' created successfully.")
        return response.json()  # Returns the created product
    else:
        try:
            error_message: str = response.json().get('errors', response.text)
        except ValueError:
            error_message = response.text
        message(f"Error creating product '{product_data.get('title')}': {response.status_code} - {error_message}")
        return None


def get_product_by_sku(sku: str) -> dict | None:
    """
    Retrieves a product from Shopify based on its SKU.
    
    Args:
        sku (str): The SKU of the product.
    
    Returns:
        dict | None: The product dictionary if found, otherwise None.
    """
    session: RateLimitedSession = RateLimitedSession(
        max_calls_per_second=2, 
        max_retries=MAX_RETRIES, 
        wait_seconds=WAIT_SECONDS
    )
    session.headers.update(HEADERS)
    params: dict = {
        "fields": "id,variants",
        "limit": 250,
        "variants.sku": sku
    }
    response: requests.Response = session.get(f"{BASE_URL}products.json", params=params)
    if response.status_code == 200:
        products: list = response.json().get('products', [])
        for product in products:
            for variant in product.get('variants', []):
                if variant.get('sku') == sku:
                    return product
    else:
        message(f"Error fetching product by SKU '{sku}': {response.status_code} - {response.text}")
    return None


def process_and_ingest_products(
    job_base: JobBase, 
    df: pd.DataFrame, 
    refs: list, 
    brands: list
) -> None:
    """
    Processes and ingests products into Shopify.
    
    Args:
        job_base (JobBase): The job base containing source data paths and memory paths.
        df (pd.DataFrame): DataFrame containing product data to ingest.
        refs (list): List of SKUs that should exist.
        brands (list): List of brands (vendors) to filter SKUs for deletion.
    
    Raises:
        ValueError: If the connection to Shopify fails.
    """
    is_connected: bool = test_connection()
    
    if not is_connected:
        raise ValueError("No connection to Shopify.") 

    # Create a RateLimitedSession for global use
    session: RateLimitedSession = RateLimitedSession(
        max_calls_per_second=2, 
        max_retries=MAX_RETRIES, 
        wait_seconds=WAIT_SECONDS
    )
    session.headers.update(HEADERS)
    
    sku_data: dict = get_all_skus_with_product_ids()

    # Find and delete duplicated SKUs
    duplicate_skus: dict = find_duplicate_skus(sku_data)
    delete_duplicates_products(duplicate_skus)
    # Update sku_data after deleting duplicates
    sku_data = get_all_skus_with_product_ids()

    # Find and delete extra SKUs
    for brand in brands:
        skus_to_delete: list = find_extra_skus_to_delete(sku_data, refs, brand)
        delete_extra_skus(skus_to_delete)

    # Update sku_data after deleting extra SKUs
    sku_data = get_all_skus_with_product_ids()

    message("INGESTION START")
    
    df_products_memory_shopify: pd.DataFrame = pd.DataFrame(columns=df.columns)
    total_rows: int = len(df)
    for index, row in df.iterrows():
        product_data, variant_data = format_product_for_shopify(job_base, row)
        if not product_data or not variant_data:
            continue

        sku: str = row['ref']
        message(f"{index}/{total_rows} REF - {sku} - {row['title']}")

        # Update the product if it already exists
        product_exists: bool = update_product_by_sku(job_base, sku, product_data, variant_data, row, sku_data)

        if not product_exists:
            # Prepare full data to create the product if it does not exist
            full_product_data: dict = product_data.copy()
            full_product_data['variants'] = [variant_data]
            product_images: list = []
            path_product_images: str = f"{job_base.src_data_path}/{row['page_name']}/products/{row['ref']}_images.json"
            if file_or_path_exists(path_product_images):
                product_images = read_json(path_product_images)['url_images']
            product_images.insert(0, row['image_url'])
            full_product_data['images'] = [{"src": url} for url in product_images]
            
            # Create the new product
            created_product: dict | None = create_product(full_product_data)
            
            # After creating the product, add it to collections and update inventory
            if created_product:
                product_id: int = created_product['product']['id']
                update_collections(session, product_id, row)
                
                # Update the inventory level for the new product
                variant_info: dict = created_product['product']['variants'][0]
                inventory_item_id: int | None = variant_info.get('inventory_item_id')
                variant_id: int = variant_info.get('id')
                if 'quantity_sold' in row and pd.notna(row['quantity_sold']):
                    quantity_sold: int = row['quantity_sold']
                else:
                    quantity_sold = 1000
                update_inventory_level(session, inventory_item_id, quantity_sold)
                
                # Add the new SKU to sku_data
                sku_data[sku] = [{
                    'variant_id': variant_id,
                    'product_id': product_id,
                    'vendor': product_data['vendor'],
                    'inventory_item_id': inventory_item_id
                }]
        
        if not pd.DataFrame([row]).isna().all().all():
            df_products_memory_shopify = pd.concat(
                [df_products_memory_shopify, pd.DataFrame([row])], 
                ignore_index=True
            )

        # Save the result to the specified path
        df_products_memory_shopify.to_csv(job_base.path_memory_shopify, index=False)
        message("path_products_memory_shopify saved successfully.")
    
    message("INGESTION END")