import ast
import functools
import json
import time
import threading
from typing import Tuple
from urllib.parse import parse_qs, urlparse

import pandas as pd
import requests

# Importações de configurações e utilitários (ajuste conforme necessário)
from src.config.setup.shopify import BASE_URL, HEADERS
from src.lib.utils.file_system import path_exists, read_file, read_json
from src.lib.utils.log import message

# Definição de constantes
MAX_RETRIES = 3  # Número máximo de tentativas
WAIT_SECONDS = 3  # Tempo de espera entre as tentativas em segundos

# Implementação da classe RateLimitedSession
class RateLimitedSession(requests.Session):
    def __init__(self, max_calls_per_second, max_retries, wait_seconds, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_interval = 1.0 / float(max_calls_per_second)
        self.last_call = 0.0
        self.lock = threading.Lock()
        self.max_retries = max_retries
        self.wait_seconds = wait_seconds

    def request(self, method, url, *args, **kwargs):
        retries = 0
        while True:
            with self.lock:
                elapsed = time.time() - self.last_call
                left_to_wait = self.min_interval - elapsed
                if left_to_wait > 0:
                    time.sleep(left_to_wait)
                self.last_call = time.time()
            response = super().request(method, url, *args, **kwargs)
            if response.status_code == 429:
                retries += 1
                if retries >= self.max_retries:
                    message(f"Máximo de tentativas alcançado para a URL '{url}'. Status 429.")
                    response.raise_for_status()
                else:
                    message(f"Erro 429 na URL '{url}'. Tentativa {retries}/{self.max_retries}. Aguardando {self.wait_seconds} segundos antes de tentar novamente.")
                    time.sleep(self.wait_seconds)
            else:
                return response

def test_connection() -> bool:
    """
    Testa a conexão com a API da Shopify.
    """
    session = RateLimitedSession(max_calls_per_second=2, max_retries=MAX_RETRIES, wait_seconds=WAIT_SECONDS)
    session.headers.update(HEADERS)
    url = f"{BASE_URL}products.json"
    response = session.get(url)
    
    if response.status_code == 200:
        message("Conexão bem-sucedida! A API está acessível.")
        return True
    else:
        message(f"Erro ao conectar: {response.status_code} - {response.text}")
        return False

def generate_price_chart(prices: list) -> str:
    """
    Gera o código HTML e JavaScript para exibir um gráfico de preços usando Chart.js.
    
    Args:
    - prices: Lista de dicionários com os dados de preço e data.
    
    Returns:
    - Código HTML + JS do gráfico para ser incorporado ao body_html.
    """
    # Extraindo datas e preços dos dados
    dates = [entry['date'] for entry in prices]
    prices_data = [entry['price'] for entry in prices]
    
    # Definir a escala mínima e máxima com base nos valores de preço
    min_price = int(min(prices_data) - 1)
    max_price = int(max(prices_data) + 1)

    # Geração do código HTML e JS para o gráfico
    chart_html = f'''
    <br>
    <br>
    <div class="chart-container" style="position: relative; height:300px; width:100%;">
        <canvas id="priceChart"></canvas>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        var ctx = document.getElementById('priceChart').getContext('2d');
        var priceChart = new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: {json.dumps(dates)},  // Datas do gráfico
                datasets: [{{
                    label: 'Preço (R$)',
                    data: {json.dumps(prices_data)},  // Preços do gráfico
                    fill: false,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    pointBackgroundColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                scales: {{
                    y: {{
                        beginAtZero: false,
                        min: {min_price},  // Escala mínima do eixo Y
                        max: {max_price},  // Escala máxima do eixo Y
                        grid: {{
                            display: true
                        }}
                    }},
                    x: {{
                        grid: {{
                            display: true
                        }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top',
                    }}
                }}
            }}
        }});
    </script>
    '''
    
    return chart_html

def format_product_for_shopify(row: pd.Series) -> Tuple[dict, dict]:
    """
    Formata os dados de um produto para o formato esperado pela API da Shopify.
    
    Returns:
    - product_data: dict com dados do produto
    - variant_data: dict com dados da variante
    """
    try:
        description_ai = None
        path_description_ai = f"{CONF['data_path']}/products/{row['ref']}_description_ai.txt"
        if path_exists(path_description_ai):
            description_ai = read_file(path_description_ai)
                   
        body_html = f'''
            <a href="{row['product_url']}" target="_blank" id="product_url-link">
                <button id="product_url" role="button">Ir para loja do suplemento</button>
            </a>
        '''
        
        if description_ai:
            formatted_description = f"<br><br><br>{description_ai.replace('\n', '<br>')}"
            body_html += f'''
                <div id="product-description">
                    {formatted_description}
                </div>
            '''
        
        check_prices = pd.notna(row['prices'])
        if check_prices and isinstance(row['prices'], str):
            row['prices'] = json.loads(row['prices'].replace("'", '"')) 
        
            if check_prices and isinstance(row['prices'], list) and len(row['prices']) > 1:
                price_chart_html = generate_price_chart(row['prices'])
                body_html += price_chart_html
        
        product_type = row['product_tags']
        product_data = {
            "title": row['title_extract'],
            "body_html": body_html,
            "vendor": row['brand'].title(),
            "tags": product_type if pd.notna(product_type) else "Outros",
            "product_type": "",
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

def get_all_skus_with_product_ids() -> dict:
    """
    Obtém todas as SKUs de todos os produtos da Shopify, incluindo o product_id e o vendor.

    Returns:
    - dict: Um dicionário onde as chaves são SKUs e os valores são listas de dicionários
            contendo 'variant_id', 'product_id' e 'vendor'.
    """
    try:
        session = RateLimitedSession(max_calls_per_second=2, max_retries=MAX_RETRIES, wait_seconds=WAIT_SECONDS)
        session.headers.update(HEADERS)

        sku_variants = {}  # Dicionário para mapear SKUs a uma lista de variantes
        limit = 250
        params = {
            "limit": limit,
            "fields": "id,variants,vendor"
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
                vendor = product.get('vendor', '')
                for variant in product.get('variants', []):
                    variant_id = variant.get('id')
                    sku = variant.get('sku', '').strip()
                    if sku:
                        if sku not in sku_variants:
                            sku_variants[sku] = []
                        sku_variants[sku].append({
                            'variant_id': variant_id,
                            'product_id': product_id,
                            'vendor': vendor
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
            de variantes (com 'variant_id', 'product_id', 'vendor') associadas a essa SKU.
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
        session = RateLimitedSession(max_calls_per_second=2, max_retries=MAX_RETRIES, wait_seconds=WAIT_SECONDS)
        session.headers.update(HEADERS)
        for sku, variants in duplicate_skus.items():
            for variant in variants:
                product_id = variant['product_id']
                variant_id = variant['variant_id']
                
                # Verifica o número de variantes restantes no produto
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

def delete_extra_skus(skus_to_delete: list):
    if skus_to_delete:
        message(f"Encontrado {len(skus_to_delete)} SKUs para deletar.")
        session = RateLimitedSession(max_calls_per_second=2, max_retries=MAX_RETRIES, wait_seconds=WAIT_SECONDS)
        session.headers.update(HEADERS)
        for item in skus_to_delete:
            product_id = item['product_id']
            variant_id = item['variant_id']
            sku = item['sku']

            # Verifica o número de variantes restantes no produto
            variant_count = get_variant_count(session, product_id)

            if variant_count > 1:
                # Se o produto tem mais de uma variante, apenas a variante será deletada
                delete_variant(session, variant_id)
                message(f"Variante {variant_id} do produto {product_id} (SKU {sku}) deletada.")
            else:
                # Se o produto só tem uma variante, o produto será deletado
                delete_product(session, product_id)
                message(f"Produto {product_id} (SKU {sku}) deletado porque tinha apenas uma variante.")

        message("Processo de deleção de SKUs concluído.")
    else:
        message("Nenhuma SKU para deletar.")

def find_extra_skus_to_delete(sku_data: dict, refs: list, brand: str) -> list:
    """
    Encontra SKUs que estão na Shopify mas não estão na lista de 'refs', para um determinado 'brand' (vendor).

    Args:
    - sku_data (dict): Dicionário retornado pela função get_all_skus_with_product_ids.
    - refs (list): Lista de SKUs que deveriam existir.
    - brand (str): O 'vendor' (marca) para filtrar.

    Returns:
    - list: Lista de dicionários com 'sku', 'variant_id', 'product_id' que precisam ser deletados.
    """
    skus_to_delete = []
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
    session = RateLimitedSession(max_calls_per_second=2, max_retries=MAX_RETRIES, wait_seconds=WAIT_SECONDS)
    session.headers.update(HEADERS)

    if sku in sku_data:
        variants = sku_data[sku]
        product_id = variants[0]['product_id']
        variant_id = variants[0]['variant_id']
        # Atualiza o produto
        product_success = update_product(session, product_id, product_data)
        # Atualiza a variante
        variant_success = update_variant(session, product_id, variant_id, variant_data)
        
        product_images = []
        path_product_images = f"{CONF['data_path']}/products/{row['ref']}_images.json"
        if path_exists(path_product_images):
            product_images = read_json(path_product_images)['url_images']
        product_images.insert(0, row['image_url'])
        
        # Atualiza imagens
        images_success = update_images(session, product_id, product_images)
        # Atualiza coleções
        collections_success = update_collections(session, product_id, row)
        return product_success and variant_success and images_success and collections_success
    else:
        message(f"SKU '{sku}' não encontrado nos dados da Shopify.")
        return False

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

def update_images(session, product_id: int, image_urls: list) -> bool:
    """
    Atualiza as imagens de um produto na Shopify, substituindo as imagens atuais pelas novas.
    """
    try:
        # Prepara a lista de novas imagens
        new_images = [{"src": url} for url in image_urls]

        # Atualiza as imagens do produto em uma única chamada
        product_data = {
            "product": {
                "id": product_id,
                "images": new_images
            }
        }
        response = session.put(f"{BASE_URL}products/{product_id}.json", json=product_data)
        if response.status_code in [200, 201]:
            message(f"Imagens do produto {product_id} atualizadas com sucesso.")
            return True
        else:
            error_message = response.json().get('errors', response.text)
            message(f"Erro ao atualizar imagens do produto {product_id}: {response.status_code} - {error_message}")
            return False

    except Exception as e:
        message(f"Erro ao atualizar imagens do produto {product_id}: {e}")
        return False

def update_collections(session, product_id: int, row: pd.Series) -> bool:
    """
    Atualiza as coleções de um produto, adicionando e removendo conforme necessário.
    """
    try:
        collections_field = row['collections']
        if pd.isna(collections_field):
            desired_collections = ["Sem coleção"]
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

        success = True

        # Passo 1: Obter todas as coleções atuais do produto
        current_collections = []
        page_info = None
        while True:
            params = {
                "product_id": product_id,
                "fields": "collection_id",
                "limit": 250
            }
            if page_info:
                params["page_info"] = page_info

            response = session.get(f"{BASE_URL}collects.json", params=params)
            if response.status_code != 200:
                message(f"Erro ao obter coleções atuais do produto {product_id}: {response.status_code} - {response.text}")
                success = False
                break

            collects = response.json().get('collects', [])
            for collect in collects:
                current_collections.append(collect['collection_id'])

            # Verifica paginação
            link_header = response.headers.get('Link')
            if link_header and 'rel="next"' in link_header:
                links = link_header.split(',')
                for link in links:
                    if 'rel="next"' in link:
                        start = link.find('<') + 1
                        end = link.find('>')
                        url = link[start:end]
                        parsed_url = urlparse(url)
                        query_params = parse_qs(parsed_url.query)
                        page_info = query_params.get('page_info', [None])[0]
                        break
            else:
                break

        # Passo 2: Mapear títulos de coleções desejadas para IDs
        desired_collection_ids = []
        for collection_title in desired_collections:
            # Buscar a coleção, criar se não existir
            response = session.get(f"{BASE_URL}custom_collections.json", params={"title": collection_title})
            if response.status_code != 200:
                message(f"Erro ao buscar coleções: {response.status_code} - {response.text}")
                success = False
                continue

            collections = response.json().get('custom_collections', [])
            if not collections:
                # Criar a coleção
                collection_payload = {
                    "custom_collection": {
                        "title": collection_title,
                        "published": True
                    }
                }
                response = session.post(f"{BASE_URL}custom_collections.json", json=collection_payload)
                if response.status_code != 201:
                    error_message = response.json().get('errors', response.text)
                    message(f"Erro ao criar coleção '{collection_title}': {response.status_code} - {error_message}")
                    success = False
                    continue
                collection_id = response.json()['custom_collection']['id']
                message(f"Coleção '{collection_title}' criada com ID {collection_id}.")
            else:
                collection_id = collections[0]['id']
            desired_collection_ids.append(collection_id)

        # Passo 3: Determinar coleções para adicionar e remover
        collections_to_add = set(desired_collection_ids) - set(current_collections)
        collections_to_remove = set(current_collections) - set(desired_collection_ids)

        # Passo 4: Adicionar produto às novas coleções
        for collection_id in collections_to_add:
            collect_payload = {
                "collect": {
                    "product_id": product_id,
                    "collection_id": collection_id
                }
            }
            response = session.post(f"{BASE_URL}collects.json", json=collect_payload)
            if response.status_code == 201:
                message(f"Produto {product_id} adicionado à coleção ID {collection_id}.")
            else:
                error_message = response.json().get('errors', response.text)
                message(f"Erro ao adicionar produto {product_id} à coleção ID {collection_id}: {response.status_code} - {error_message}")
                success = False

        # Passo 5: Remover produto das coleções que não deve mais pertencer
        for collection_id in collections_to_remove:
            # Encontrar o collect ID
            response = session.get(f"{BASE_URL}collects.json", params={"collection_id": collection_id, "product_id": product_id})
            if response.status_code != 200:
                message(f"Erro ao buscar collect para produto {product_id} e coleção {collection_id}: {response.status_code} - {response.text}")
                success = False
                continue
            collects = response.json().get('collects', [])
            if collects:
                collect_id = collects[0]['id']
                # Deletar o collect
                response = session.delete(f"{BASE_URL}collects/{collect_id}.json")
                if response.status_code in [200, 204]:
                    message(f"Produto {product_id} removido da coleção ID {collection_id}.")
                else:
                    error_message = response.json().get('errors', response.text)
                    message(f"Erro ao remover produto {product_id} da coleção ID {collection_id}: {response.status_code} - {error_message}")
                    success = False

        return success
    except Exception as e:
        message(f"Erro ao atualizar coleções do produto {product_id}: {e}")
        return False

def create_product(product_data: dict):
    """
    Cria um novo produto na Shopify com os dados fornecidos.
    
    Args:
    - product_data (dict): Dados formatados do produto para criação.
    
    Returns:
    - dict: O produto criado retornado pela API Shopify, ou None em caso de erro.
    """
    session = RateLimitedSession(max_calls_per_second=2, max_retries=MAX_RETRIES, wait_seconds=WAIT_SECONDS)
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

def get_product_by_sku(sku: str):
    """
    Obtém o produto com base no SKU.
    """
    session = RateLimitedSession(max_calls_per_second=2, max_retries=MAX_RETRIES, wait_seconds=WAIT_SECONDS)
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

def process_and_ingest_products(conf: dict, df: pd.DataFrame, refs: list, brand) -> None:
    global CONF
    CONF = conf
    
    is_connected = test_connection()
    
    if not is_connected:
        raise ValueError("Sem conexão com a Shopify") 

    # Cria uma sessão RateLimitedSession para uso global
    session = RateLimitedSession(max_calls_per_second=2, max_retries=MAX_RETRIES, wait_seconds=WAIT_SECONDS)
    session.headers.update(HEADERS)
    
    sku_data = get_all_skus_with_product_ids()

    # Encontra SKUs duplicadas e deleta
    duplicate_skus = find_duplicate_skus(sku_data)
    delete_duplicates_products(duplicate_skus)
    # Atualiza sku_data após deletar duplicatas
    sku_data = get_all_skus_with_product_ids()

    # Encontra SKUs extras e deleta
    if (type(brand) == list):
        for i in brand:
            skus_to_delete = find_extra_skus_to_delete(sku_data, refs, i)
    else:
        skus_to_delete = find_extra_skus_to_delete(sku_data, refs, brand)
        
    delete_extra_skus(skus_to_delete)

    # Atualiza sku_data após deletar SKUs extras
    sku_data = get_all_skus_with_product_ids()

    message("INGESTION START")
    
    for index, row in df.iterrows():
        product_data, variant_data = format_product_for_shopify(row)
        if product_data is None or variant_data is None:
            continue

        sku = row['ref']
        message(f"REF - {sku} - {row['title']}")

        product_exist = update_product_by_sku(sku, product_data, variant_data, row, sku_data)

        if not product_exist:
            # Prepara os dados completos para criar o produto
            full_product_data = product_data.copy()
            full_product_data['variants'] = [variant_data]
            product_images = []
            path_product_images = f"{CONF['data_path']}/products/{row['ref']}_images.json"
            if path_exists(path_product_images):
                product_images = read_json(path_product_images)['url_images']
            product_images.insert(0, row['image_url'])
            full_product_data['images'] = [{"src": url} for url in product_images]
            create_product(full_product_data)
            
            # Após criar o produto, adiciona-o à coleção
            # Precisamos obter o product_id do produto recém-criado
            created_product = get_product_by_sku(sku)
            if created_product:
                product_id = created_product['id']
                update_collections(session, product_id, row)
    message("INGESTION END")