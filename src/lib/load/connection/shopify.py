import json

import pandas as pd
import requests
from src.config.setup.shopify import BASE_URL, HEADERS
from src.lib.utils.log import message


def test_connection() -> None:
    """
    Testa a conexão com a API da Shopify.
    """
    url = f"{BASE_URL}products.json"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        message("Conexão bem-sucedida! A API está acessível.")
    else:
        message(f"Erro ao conectar: {response.status_code} - {response.text}")


def format_product_for_shopify(row: pd.Series) -> dict:
    """
    Formata os dados de um produto para o formato esperado pela API da Shopify.
    """
    try:
        product_type = row['product_def_pred_tag'] if pd.notna(row['product_def_pred_tag']) else row['product_def_tag']
        
        button_html = f'''
            <a href="{row['product_url']}" target="_blank" id="product_url-link">
                <button id="product_url" role="button">Ir para loja do suplemento</button>
            </a>
        '''
        
        product_data = {
            "title": row['title_extract'],
            "body_html": button_html,
            "vendor": row['brand'].title(),
            "tags": product_type if pd.notna(product_type) else "Outros",
            "product_type": "",
            "variants": [
                {
                    "price": str(row['price_numeric']),
                    "sku": row['ref'],
                    "inventory_quantity": 1,
                    "weight": float(row['quantity']) if pd.notna(row['quantity']) else None,
                    "weight_unit": "g" if pd.notna(row['quantity']) else None,
                    "compare_at_price": str(row['compare_at_price']) if pd.notna(row['compare_at_price']) else None,
                }
            ],
            "images": [
                {
                    "src": row['image_url']
                }
            ],
            "collections": [
                {
                    "title": row['collection'] if pd.notna(row['collection']) else "Sem coleção"
                }
            ]
        }
        
        return product_data
    except Exception as e:
        message(f"Erro ao formatar o produto '{row['title_extract']}': {e}")
        return None


def search_products_by_sku(sku: str) -> list:
    """
    Busca produtos na Shopify pelo SKU (ref) e retorna uma lista de produtos que possuem o SKU.
    """
    try:
        url = f"{BASE_URL}products.json?limit=250&fields=id,variants"
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            products = response.json().get('products', [])
            matching_products = [product for product in products if any(variant['sku'] == sku for variant in product['variants'])]
            return matching_products
        else:
            message(f"Erro ao buscar produtos com SKU '{sku}': {response.status_code} - {response.text}")
            return []
    except Exception as e:
        message(f"Erro na requisição ao buscar produtos com SKU '{sku}': {e}")
        return []


def delete_products_by_sku(sku: str) -> None:
    """
    Deleta todos os produtos na Shopify que possuem o SKU fornecido.
    """
    matching_products = search_products_by_sku(sku)
    
    if matching_products:
        for product in matching_products:
            product_id = product['id']
            try:
                url = f"{BASE_URL}products/{product_id}.json"
                response = requests.delete(url, headers=HEADERS)
                
                if response.status_code == 200:
                    message(f"Produto com ID '{product_id}' e SKU '{sku}' deletado com sucesso.")
                else:
                    message(f"Erro ao deletar produto com ID '{product_id}': {response.status_code} - {response.text}")
            except Exception as e:
                message(f"Erro ao deletar produto com ID '{product_id}': {e}")
    else:
        message(f"Nenhum produto encontrado com SKU '{sku}' para deletar.")


def create_product_on_shopify(product_data: dict) -> None:
    """
    Envia os dados formatados de um produto para a API da Shopify para criação.
    """
    try:
        url = f"{BASE_URL}products.json"
        response = requests.post(url, headers=HEADERS, data=json.dumps({"product": product_data}))
        
        if response.status_code == 201:
            product = response.json()['product']
            message(f"Produto '{product_data['title']}' criado com sucesso! ID: {product['id']}")
        else:
            message(f"Erro ao criar o produto '{product_data['title']}': {response.status_code} - {response.text}")
    except Exception as e:
        message(f"Erro na requisição para o produto '{product_data['title']}': {e}")


def update_product_by_sku(sku: str, updated_data: dict) -> None:
    """
    Atualiza o produto encontrado na Shopify pelo SKU fornecido.
    
    Args:
    - sku (str): O SKU do produto a ser atualizado.
    - updated_data (dict): Os dados formatados do produto no formato esperado pela API da Shopify.
    """
    # Busca produtos com o SKU fornecido
    matching_products = search_products_by_sku(sku)
    
    if not matching_products:
        message(f"Produto com SKU '{sku}' não encontrado para atualização.")
        return

    # Atualiza o primeiro produto encontrado com o SKU
    product_id = matching_products[0]['id']
    
    try:
        url = f"{BASE_URL}products/{product_id}.json"
        response = requests.put(url, headers=HEADERS, data=json.dumps({"product": updated_data}))
        
        if response.status_code == 200:
            message(f"Produto com SKU '{sku}' atualizado com sucesso! ID: {product_id}")
        else:
            message(f"Erro ao atualizar o produto com SKU '{sku}': {response.status_code} - {response.text}")
    except Exception as e:
        message(f"Erro ao atualizar o produto com SKU '{sku}': {e}")


def sku_exists_in_shopify(sku: str) -> tuple:
    """
    Verifica se um produto com o SKU fornecido existe na Shopify e retorna quantas vezes foi encontrado.
    
    Args:
    - sku (str): O SKU do produto que será verificado.
    
    Returns:
    - tuple: (bool, int) 
        - bool: True se o SKU for encontrado, False caso contrário.
        - int: O número de vezes que o SKU foi encontrado.
    """
    try:
        # Faz uma requisição para obter todos os produtos (limite de 250 produtos por requisição)
        url = f"{BASE_URL}products.json?limit=250&fields=id,variants"
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            # Extrai a lista de produtos da resposta
            products = response.json().get('products', [])
            
            # Contador de quantas vezes o SKU foi encontrado
            sku_count = 0
            
            # Verifica se algum produto tem o SKU informado
            for product in products:
                for variant in product['variants']:
                    if variant['sku'] == sku:
                        sku_count += 1
            
            # Verifica se o SKU foi encontrado
            if sku_count > 0:
                message(f"SKU '{sku}' encontrado {sku_count} vez(es) na Shopify.")
                return True, sku_count
            else:
                message(f"SKU '{sku}' não encontrado na Shopify.")
                return False, 0
        else:
            # Caso a requisição falhe
            message(f"Erro ao buscar produtos com SKU '{sku}': {response.status_code} - {response.text}")
            return False, 0
    except Exception as e:
        message(f"Erro na requisição para verificar o SKU '{sku}': {e}")
        return False, 0


def get_collection_by_title(title: str) -> dict:
    try:
        url = f"{BASE_URL}custom_collections.json?title={requests.utils.quote(title)}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            collections = response.json().get('custom_collections', [])
            if collections:
                return collections[0]
            else:
                return None
        else:
            message(f"Erro ao buscar coleção '{title}': {response.status_code} - {response.text}")
            return None
    except Exception as e:
        message(f"Erro na requisição para buscar coleção '{title}': {e}")
        return None


def create_custom_collection(title: str) -> dict:
    try:
        url = f"{BASE_URL}custom_collections.json"
        payload = {
            "custom_collection": {
                "title": title
            }
        }
        response = requests.post(url, headers=HEADERS, data=json.dumps(payload))
        if response.status_code == 201:
            collection = response.json()['custom_collection']
            message(f"Coleção '{title}' criada com sucesso! ID: {collection['id']}")
            return collection
        else:
            message(f"Erro ao criar coleção '{title}': {response.status_code} - {response.text}")
            return None
    except Exception as e:
        message(f"Erro na requisição para criar coleção '{title}': {e}")
        return None


def assign_product_to_collection(product_id: int, collection_id: int) -> bool:
    """
    Atribui um produto a uma coleção no Shopify, verificando previamente se já está atribuído.

    Args:
    - product_id (int): ID do produto.
    - collection_id (int): ID da coleção.

    Returns:
    - bool: True se a atribuição foi bem-sucedida ou já existente, False caso contrário.
    """
    try:
        # Verifica se o produto já está na coleção
        if is_product_in_collection(product_id, collection_id):
            message(f"Produto ID '{product_id}' já está atribuído à coleção ID '{collection_id}'. Nenhuma ação necessária.")
            return True  # Considera como sucesso, já que o produto já está na coleção

        # Se não estiver, procede com a atribuição
        url = f"{BASE_URL}collects.json"
        payload = {
            "collect": {
                "product_id": product_id,
                "collection_id": collection_id
            }
        }
        response = requests.post(url, headers=HEADERS, data=json.dumps(payload))
        if response.status_code == 201:
            message(f"Produto ID '{product_id}' atribuído à coleção ID '{collection_id}' com sucesso.")
            return True
        else:
            message(f"Erro ao atribuir produto ID '{product_id}' à coleção ID '{collection_id}': {response.status_code} - {response.text}")
            return False
    except Exception as e:
        message(f"Erro na requisição para atribuir produto ID '{product_id}' à coleção ID '{collection_id}': {e}")
        return False


def is_product_in_collection(product_id: int, collection_id: int) -> bool:
    """
    Verifica se um produto já está atribuído a uma coleção específica.

    Args:
    - product_id (int): ID do produto.
    - collection_id (int): ID da coleção.

    Returns:
    - bool: True se o produto já estiver na coleção, False caso contrário.
    """
    try:
        url = f"{BASE_URL}collects.json?collection_id={collection_id}&product_id={product_id}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            collects = response.json().get('collects', [])
            return len(collects) > 0
        else:
            message(f"Erro ao verificar se o produto ID '{product_id}' está na coleção ID '{collection_id}': {response.status_code} - {response.text}")
            return False
    except Exception as e:
        message(f"Erro na requisição para verificar a coleção: {e}")
        return False


def create_product_on_shopify(product_data: dict) -> int:
    try:
        url = f"{BASE_URL}products.json"
        response = requests.post(url, headers=HEADERS, data=json.dumps({"product": product_data}))
        if response.status_code == 201:
            product = response.json()['product']
            message(f"Produto '{product_data['title']}' criado com sucesso! ID: {product['id']}")
            return product['id']
        else:
            message(f"Erro ao criar o produto '{product_data['title']}': {response.status_code} - {response.text}")
            return None
    except Exception as e:
        message(f"Erro na requisição para o produto '{product_data['title']}': {e}")
        return None


def process_and_ingest_products(df: pd.DataFrame) -> None:
    for index, row in df.iterrows():
        product_data = format_product_for_shopify(row)
        if product_data is None:
            continue
        
        sku = row['ref']
        product_exists, n_of_times = sku_exists_in_shopify(sku)
        
        # Gerenciar a coleção
        collection_title = row['collection'] if pd.notna(row['collection']) else "Sem coleção"
        collection = get_collection_by_title(collection_title)
        
        if not collection:
            # Cria a coleção se não existir
            collection = create_custom_collection(collection_title)
            if not collection:
                message(f"Falha ao criar ou obter a coleção '{collection_title}'. Produto '{product_data['title']}' não será atribuído a nenhuma coleção.")
        
        if product_exists and n_of_times > 1:
            delete_products_by_sku(sku)
        elif product_exists:
            update_product_by_sku(sku, product_data)
            # Após atualizar, obter o ID do produto para atribuição
            matching_products = search_products_by_sku(sku)
            if matching_products:
                product_id = matching_products[0]['id']
                if collection:
                    assign_product_to_collection(product_id, collection['id'])
            continue
        
        # Cria o produto e obtém o ID
        product_id = create_product_on_shopify(product_data)
        if product_id and collection:
            assign_product_to_collection(product_id, collection['id'])
