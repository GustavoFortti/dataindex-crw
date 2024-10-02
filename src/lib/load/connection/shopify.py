import functools
import time
from typing import Tuple
from urllib.parse import parse_qs, urlparse

import pandas as pd
import requests

from src.config.setup.shopify import BASE_URL, HEADERS
from src.lib.utils.log import message


def retry_on_failure(max_retries, wait_seconds):
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):
            retries = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                    retries += 1
                    if retries >= max_retries:
                        message(f"Máximo de tentativas alcançado para função '{func.__name__}'. Erro: {e}")
                        raise
                    else:
                        message(f"Erro de conexão na função '{func.__name__}'. Tentativa {retries}/{max_retries}. Aguardando {wait_seconds} segundos antes de tentar novamente.")
                        time.sleep(wait_seconds)
        return wrapper_retry
    return decorator_retry

MAX_RETRIES = 3  # Número máximo de tentativas
WAIT_SECONDS = 3  # Tempo de espera entre as tentativas em segundos

@retry_on_failure(MAX_RETRIES, WAIT_SECONDS)
def test_connection() -> None:
    """
    Testa a conexão com a API da Shopify.
    """
    url = f"{BASE_URL}products.json"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        message("Conexão bem-sucedida! A API está acessível.")
        return True
    else:
        message(f"Erro ao conectar: {response.status_code} - {response.text}")
        return False

def format_product_for_shopify(row: pd.Series) -> Tuple[dict, dict]:
    """
    Formata os dados de um produto para o formato esperado pela API da Shopify.
    
    Returns:
    - product_data: dict com dados do produto
    - variant_data: dict com dados da variante
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
            # Removemos 'variants', 'images' e 'collections' do produto para atualização
        }
        
        variant_data = {
            "price": str(row['price_numeric']),
            "sku": row['ref'],
            "inventory_quantity": 1,
            "weight": float(row['quantity']) if pd.notna(row['quantity']) else None,
            "weight_unit": "g" if pd.notna(row['quantity']) else None,
            "compare_at_price": str(row['compare_at_price']) if pd.notna(row['compare_at_price']) else None,
        }
        
        return product_data, variant_data
    except Exception as e:
        message(f"Erro ao formatar o produto '{row['title_extract']}': {e}")
        return None, None

@retry_on_failure(MAX_RETRIES, WAIT_SECONDS)
def get_all_skus_with_product_ids() -> dict:
    """
    Obtém todas as SKUs de todos os produtos da Shopify, incluindo o product_id.
    
    Returns:
    - dict: Um dicionário onde as chaves são SKUs e os valores são listas de dicionários
            contendo 'variant_id' e 'product_id'.
    """
    try:
        session = requests.Session()
        session.headers.update(HEADERS)

        sku_variants = {}  # Dicionário para mapear SKUs a uma lista de variantes
        limit = 250
        params = {
            "limit": limit,
            "fields": "id,variants"
        }
        next_page_info = None
        has_more = True

        # Passo 1: Obter todos os produtos e variantes
        while has_more:
            if next_page_info:
                params["page_info"] = next_page_info

            response = session.get(f"{BASE_URL}products.json", params=params)

            if response.status_code != 200:
                message(f"Erro ao buscar produtos: {response.status_code} - {response.text}")
                return sku_variants

            products = response.json().get('products', [])

            for product in products:
                product_id = product.get('id')
                for variant in product.get('variants', []):
                    variant_id = variant.get('id')
                    sku = variant.get('sku', '').strip()
                    if sku:
                        if sku not in sku_variants:
                            sku_variants[sku] = []
                        sku_variants[sku].append({
                            'variant_id': variant_id,
                            'product_id': product_id
                        })

            # Verifica se há mais páginas utilizando os headers de Link
            link_header = response.headers.get('Link')
            if link_header:
                links = link_header.split(',')
                next_page_info = None  # Reinicializa para a próxima iteração
                for link in links:
                    if 'rel="next"' in link:
                        # Extrai o valor de page_info da URL
                        start = link.find('<') + 1
                        end = link.find('>')
                        url = link[start:end]
                        parsed_url = urlparse(url)
                        query_params = parse_qs(parsed_url.query)
                        next_page_info = query_params.get('page_info', [None])[0]
                        break
                if next_page_info:
                    has_more = True
                else:
                    has_more = False
            else:
                has_more = False  # Não há mais páginas

        return sku_variants

    except Exception as e:
        message(f"Erro ao buscar SKUs: {e}")
        return {}

def find_duplicate_skus(sku_data: dict) -> dict:
    """
    Encontra SKUs duplicadas no dicionário de SKUs.
    
    Args:
    - sku_data (dict): O dicionário retornado pela função get_all_skus_with_product_ids.
    
    Returns:
    - dict: Um dicionário onde as chaves são SKUs duplicadas e os valores são listas
            de variantes (com 'variant_id' e 'product_id') associadas a essa SKU.
    """
    duplicate_skus = {}

    for sku, variants in sku_data.items():
        if len(variants) > 1:
            # Se a SKU tiver mais de uma variante, é considerada duplicada
            duplicate_skus[sku] = variants

    return duplicate_skus

def delete_duplicates_products(duplicate_skus):
    if duplicate_skus:
        message(f"Encontrado {len(duplicate_skus)} SKUs duplicadas.")
        # Deletar todos os produtos e variantes encontrados
        for sku, variants in duplicate_skus.items():
            for variant in variants:
                product_id = variant['product_id']
                variant_id = variant['variant_id']
                
                # Verifica o número de variantes restantes no produto
                session = requests.Session()
                session.headers.update(HEADERS)
                variant_count = get_variant_count(session, product_id)
                
                if variant_count > 1:
                    # Se o produto tem mais de uma variante, apenas a variante duplicada será deletada
                    delete_variant(session, variant_id)
                    message(f"Variante {variant_id} do produto {product_id} deletada.")
                else:
                    # Se o produto só tem uma variante, o produto será deletado
                    delete_product(session, product_id)
                    message(f"Produto {product_id} deletado porque tinha apenas uma variante.")

        message("Processo de remoção de SKUs duplicadas concluído.")
    else:
        message("Nenhuma SKU duplicada encontrada.")

@retry_on_failure(MAX_RETRIES, WAIT_SECONDS)
def get_variant_count(session, product_id):
    """
    Obtém o número de variantes de um produto.
    
    Args:
    - session: Sessão de requisição autenticada.
    - product_id: ID do produto.
    
    Returns:
    - int: Número de variantes do produto.
    """
    response = session.get(f"{BASE_URL}products/{product_id}.json", params={"fields": "variants"})
    if response.status_code == 200:
        product = response.json().get('product', {})
        variants = product.get('variants', [])
        return len(variants)
    else:
        message(f"Erro ao obter variantes do produto {product_id}: {response.status_code} - {response.text}")
        return 0

@retry_on_failure(MAX_RETRIES, WAIT_SECONDS)
def delete_variant(session, variant_id):
    """
    Deleta uma variante específica.
    
    Args:
    - session: Sessão de requisição autenticada.
    - variant_id: ID da variante a ser deletada.
    """
    response = session.delete(f"{BASE_URL}variants/{variant_id}.json")
    if response.status_code != 200:
        message(f"Erro ao deletar variante {variant_id}: {response.status_code} - {response.text}")

@retry_on_failure(MAX_RETRIES, WAIT_SECONDS)
def delete_product(session, product_id):
    """
    Deleta um produto específico.
    
    Args:
    - session: Sessão de requisição autenticada.
    - product_id: ID do produto a ser deletado.
    """
    response = session.delete(f"{BASE_URL}products/{product_id}.json")
    if response.status_code != 200:
        message(f"Erro ao deletar produto {product_id}: {response.status_code} - {response.text}")

def update_product_by_sku(sku: str, product_data: dict, variant_data: dict, row: pd.Series, sku_data: dict) -> bool:
    session = requests.Session()
    session.headers.update(HEADERS)

    if sku in sku_data:
        variants = sku_data[sku]
        product_id = variants[0]['product_id']
        variant_id = variants[0]['variant_id']
        # Atualiza o produto
        product_success = update_product(session, product_id, product_data)
        # Atualiza a variante
        variant_success = update_variant(session, product_id, variant_id, variant_data)
        # Atualiza imagens
        images_success = update_images(session, product_id, row)
        # Atualiza coleções
        collections_success = update_collections(session, product_id, row)
        return product_success and variant_success and images_success and collections_success
    else:
        message(f"SKU '{sku}' não encontrado nos dados da Shopify.")
        return False

@retry_on_failure(MAX_RETRIES, WAIT_SECONDS)
def update_product(session, product_id: int, product_data: dict) -> bool:
    url = f"{BASE_URL}products/{product_id}.json"
    product_data['id'] = product_id
    response = session.put(url, json={"product": product_data})

    if response.status_code == 200:
        message(f"Produto {product_id} atualizado com sucesso.")
        return True
    else:
        error_message = response.json().get('errors', response.text)
        message(f"Erro ao atualizar o produto {product_id}: {response.status_code} - {error_message}")
        return False

@retry_on_failure(MAX_RETRIES, WAIT_SECONDS)
def update_images(session, product_id: int, row: pd.Series) -> bool:
    """
    Atualiza as imagens de um produto na Shopify, garantindo que apenas a nova imagem esteja associada ao produto.
    """
    try:
        # Obtém as imagens atuais do produto
        response = session.get(f"{BASE_URL}products/{product_id}/images.json")
        if response.status_code != 200:
            message(f"Erro ao obter imagens do produto {product_id}: {response.status_code} - {response.text}")
            return False

        current_images = response.json().get('images', [])
        new_image_src = row['image_url']

        if pd.notna(new_image_src):
            # Remove todas as imagens atuais
            for image in current_images:
                image_id = image.get('id')
                delete_response = session.delete(f"{BASE_URL}products/{product_id}/images/{image_id}.json")
                if delete_response.status_code not in [200, 204]:
                    message(f"Erro ao deletar imagem {image_id} do produto {product_id}: {delete_response.status_code} - {delete_response.text}")
                    return False
                else:
                    message(f"Imagem {image_id} do produto {product_id} deletada.")

            # Adiciona a nova imagem
            image_payload = {
                "image": {
                    "src": new_image_src
                }
            }
            response = session.post(f"{BASE_URL}products/{product_id}/images.json", json=image_payload)
            if response.status_code in [200, 201]:
                message(f"Nova imagem adicionada ao produto {product_id}.")
                return True
            else:
                error_message = response.json().get('errors', response.text)
                message(f"Erro ao adicionar imagem ao produto {product_id}: {response.status_code} - {error_message}")
                return False
        else:
            # Se não houver uma nova imagem, mas o produto possui imagens atuais, removê-las
            if current_images:
                for image in current_images:
                    image_id = image.get('id')
                    delete_response = session.delete(f"{BASE_URL}products/{product_id}/images/{image_id}.json")
                    if delete_response.status_code not in [200, 204]:
                        message(f"Erro ao deletar imagem {image_id} do produto {product_id}: {delete_response.status_code} - {delete_response.text}")
                        return False
                    else:
                        message(f"Imagem {image_id} do produto {product_id} deletada.")
            message(f"Nenhuma nova imagem para adicionar ao produto {product_id}.")
            return True
    except Exception as e:
        message(f"Erro ao atualizar imagens do produto {product_id}: {e}")
        return False

@retry_on_failure(MAX_RETRIES, WAIT_SECONDS)
def update_collections(session, product_id: int, row: pd.Series) -> bool:
    """
    Adiciona o produto a uma coleção manual na Shopify.
    """
    try:
        collection_title = row['collection'] if pd.notna(row['collection']) else "Sem coleção"

        # Obtém todas as coleções manuais (Custom Collections)
        response = session.get(f"{BASE_URL}custom_collections.json", params={"title": collection_title})
        if response.status_code != 200:
            message(f"Erro ao obter coleções: {response.status_code} - {response.text}")
            return False

        collections = response.json().get('custom_collections', [])
        if not collections:
            # Cria a coleção se não existir
            collection_payload = {
                "custom_collection": {
                    "title": collection_title,
                    "published": True
                }
            }
            response = session.post(f"{BASE_URL}custom_collections.json", json=collection_payload)
            if response.status_code != 201:
                error_message = response.json().get('errors', response.text)
                message(f"Erro ao criar a coleção '{collection_title}': {response.status_code} - {error_message}")
                return False
            collection_id = response.json()['custom_collection']['id']
            message(f"Coleção '{collection_title}' criada com ID {collection_id}.")
        else:
            collection_id = collections[0]['id']

        # Verifica se o produto já está na coleção
        response = session.get(f"{BASE_URL}collects.json", params={"collection_id": collection_id, "product_id": product_id})
        if response.status_code != 200:
            message(f"Erro ao verificar se o produto {product_id} está na coleção {collection_id}: {response.status_code} - {response.text}")
            return False

        collects = response.json().get('collects', [])
        if not collects:
            # Adiciona o produto à coleção
            collect_payload = {
                "collect": {
                    "product_id": product_id,
                    "collection_id": collection_id
                }
            }
            response = session.post(f"{BASE_URL}collects.json", json=collect_payload)
            if response.status_code == 201:
                message(f"Produto {product_id} adicionado à coleção '{collection_title}'.")
                return True
            else:
                error_message = response.json().get('errors', response.text)
                message(f"Erro ao adicionar o produto {product_id} à coleção '{collection_title}': {response.status_code} - {error_message}")
                return False
        else:
            message(f"Produto {product_id} já está na coleção '{collection_title}'.")
            return True
    except Exception as e:
        message(f"Erro ao atualizar coleções do produto {product_id}: {e}")
        return False

@retry_on_failure(MAX_RETRIES, WAIT_SECONDS)
def update_variant(session, product_id: int, variant_id: int, variant_data: dict) -> bool:
    url = f"{BASE_URL}variants/{variant_id}.json"

    variant_data['id'] = variant_id

    response = session.put(url, json={"variant": variant_data})

    if response.status_code == 200:
        message(f"Variante {variant_id} do produto {product_id} atualizada com sucesso.")
        return True
    else:
        try:
            error_message = response.json().get('errors', response.text)
        except ValueError:
            error_message = response.text
        message(f"Erro ao atualizar a variante {variant_id} do produto {product_id}: {response.status_code} - {error_message}")
        return False

@retry_on_failure(MAX_RETRIES, WAIT_SECONDS)
def create_product(product_data: dict):
    """
    Cria um novo produto na Shopify com os dados fornecidos.
    
    Args:
    - product_data (dict): Dados formatados do produto para criação.
    
    Returns:
    - dict: O produto criado retornado pela API Shopify, ou None em caso de erro.
    """
    session = requests.Session()
    session.headers.update(HEADERS)

    url = f"{BASE_URL}products.json"
    
    # Faz a requisição POST para criar o produto
    response = session.post(url, json={"product": product_data})
    
    if response.status_code == 201:
        message(f"Produto '{product_data.get('title')}' criado com sucesso.")
        return response.json()  # Retorna o produto criado
    else:
        try:
            error_message = response.json().get('errors', response.text)
        except ValueError:
            error_message = response.text
        message(f"Erro ao criar o produto '{product_data.get('title')}': {response.status_code} - {error_message}")
        return None

@retry_on_failure(MAX_RETRIES, WAIT_SECONDS)
def get_product_by_sku(sku: str):
    """
    Obtém o produto com base no SKU.
    """
    session = requests.Session()
    session.headers.update(HEADERS)
    params = {
        "fields": "id,variants",
        "limit": 250,
        "variants.sku": sku
    }
    response = session.get(f"{BASE_URL}products.json", params=params)
    if response.status_code == 200:
        products = response.json().get('products', [])
        for product in products:
            for variant in product.get('variants', []):
                if variant.get('sku') == sku:
                    return product
    else:
        message(f"Erro ao buscar produto pelo SKU '{sku}': {response.status_code} - {response.text}")
    return None

def process_and_ingest_products(df: pd.DataFrame) -> None:
    is_connected = test_connection()
    
    if not is_connected:
        raise ValueError("Sem conexão com a Shopify") 
    
    sku_data = get_all_skus_with_product_ids()

    duplicate_skus = find_duplicate_skus(sku_data)
    delete_duplicates_products(duplicate_skus)

    # Atualiza sku_data após deletar duplicatas
    sku_data = get_all_skus_with_product_ids()

    for index, row in df.iterrows():
        product_data, variant_data = format_product_for_shopify(row)
        if product_data is None or variant_data is None:
            continue

        sku = row['ref']
        message("START PRODUCT INGESTION | REF - {sku}")

        product_exist = update_product_by_sku(sku, product_data, variant_data, row, sku_data)

        if not product_exist:
            # Prepara os dados completos para criar o produto
            full_product_data = product_data.copy()
            full_product_data['variants'] = [variant_data]
            if pd.notna(row['image_url']):
                full_product_data['images'] = [{"src": row['image_url']}]
            create_product(full_product_data)
            # Após criar o produto, adiciona-o à coleção
            # Precisamos obter o product_id do produto recém-criado
            created_product = get_product_by_sku(sku)
            if created_product:
                product_id = created_product['id']
                update_collections(requests.Session(), product_id, row)
                
    message("INGESTION END")