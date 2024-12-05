import os

ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
SHOP_NAME = os.getenv("SHOPIFY_SHOP_NAME")
API_VERSION = os.getenv("SHOPIFY_API_VERSION")

BASE_URL = f"https://{SHOP_NAME}.myshopify.com/admin/api/{API_VERSION}/"

HEADERS = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": ACCESS_TOKEN
}