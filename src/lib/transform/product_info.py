from typing import Dict, List, Optional

import html2text
import pandas as pd
from bs4 import BeautifulSoup

from src.lib.extract.extract import products_metadata_update_old_pages_by_ref
from src.lib.extract.page_elements import Page
from src.lib.utils.file_system import file_modified_within_x_hours, read_file, save_file, save_json
from src.lib.utils.log import message
from src.lib.utils.py_functions import flatten_list
from src.lib.transform.product_definition import create_product_cols

def create_product_info_cols(df: pd.DataFrame, conf: Dict) -> None:
    message("CARREGANDO dados dos produtos")
    if (conf["mode"] == "prd"):
        load_product_info(df, conf)
    
    message("CRIANDO colunas [produtc_definition, product_collection]")
    return create_product_cols(df, conf)

def load_product_info(df: pd.DataFrame, conf: Dict) -> None:
    """
    Inicializa o processo de extração de metadados de produtos a partir de um DataFrame.

    Args:
        df (pd.DataFrame): DataFrame contendo as informações dos produtos.
    """
    message("RUNNING MODEL PREP...")

    global CONF, DATA_PATH
    CONF = conf
    DATA_PATH = conf["data_path"]

    extract_metadata_from_page(df)

def extract_metadata_from_page(df: pd.DataFrame) -> None:
    """
    Percorre cada linha do DataFrame e extrai as informações do produto.

    Args:
        df (pd.DataFrame): DataFrame contendo as informações dos produtos.
    """
    for idx, row in df.iterrows():
        ref: str = str(row['ref'])
        product_url: str = row['product_url']

        # Definir caminhos de arquivos
        products_path: str = f"{DATA_PATH}/products"
        description_path: str = f"{products_path}/{ref}_description.txt"
        images_path: str = f"{products_path}/{ref}_images.json"
        page_path: str = f"{products_path}/{ref}.txt"

        # Tentar carregar o HTML da página, atualizar se não existir
        html_text: Optional[str] = fetch_product_page_html(page_path, product_url)

        if ("text" in CONF["tag_map_preference"]):
            # Extrair descrição com base nas tags configuradas
            description: Optional[str] = extract_element_from_html(html_text, CONF["product_description_tag_map"], get_product_description)
            
            if not description:
                html_text: Optional[str] = fetch_product_page_html(page_path, product_url, True)
                description: Optional[str] = extract_element_from_html(html_text, CONF["product_description_tag_map"], get_product_description)
        
            # Se a descrição foi extraída, formata e salva o arquivo
            if description:
                description = " ".join(description)
                formatted_description: str = format_product_description(row, description)
                message(f"save {ref} description")
                save_file(formatted_description, description_path)
                
        if ("image" in CONF["tag_map_preference"]):
            url_images: Optional[str] = extract_element_from_html(html_text, CONF["product_images_tag_map"], get_product_url_images)
            url_images = flatten_list(url_images)
            if (CONF["first_image_is_duplicate"]):
                url_images = url_images[1:]
            
            save_json(images_path, {
                "url_images": url_images
            })
    
def fetch_product_page_html(page_path: str, product_url: str, force: bool = None) -> Optional[str]:
    """
    Tenta ler o HTML da página do produto, atualiza a página se não encontrar o arquivo.

    Args:
        page_path (str): Caminho do arquivo HTML do produto.
        product_url (str): URL do produto.

    Returns:
        Optional[str]: Texto HTML da página do produto, ou None se não encontrado.
    """
    html_text: Optional[str] = read_file(page_path)

    is_page_updated = file_modified_within_x_hours(page_path, 6)
    if (((not html_text) or (force)) and (not is_page_updated)):
        # Atualizar o metadata e tentar novamente
        products_metadata_update_old_pages_by_ref(CONF, Page, product_url)
        html_text = read_file(page_path)

    return html_text

def extract_element_from_html(html_text: Optional[str], tags_map: str, get_function) -> Optional[str]:
    """
    Extrai a descrição do produto do HTML utilizando as tags configuradas.

    Args:
        html_text (Optional[str]): Texto HTML da página do produto.

    Returns:
        Optional[str]: Descrição extraída do HTML, ou None se não encontrada.
    """
    elements = []
    
    if html_text:
        for tag_map in tags_map:
            element: Optional[str] = get_function(html_text, tag_map)
            if element:
                elements.append(element)
            
    if elements:
        return elements
    
    return None

def format_product_description(row: pd.Series, description: str) -> str:
    """
    Formata a descrição do produto incluindo o título e a marca.

    Args:
        row (pd.Series): Linha do DataFrame contendo as informações do produto.
        description (str): Descrição extraída do HTML.

    Returns:
        str: Descrição formatada do produto.
    """
    return f"Produto: {row['title']}\nMarca: {row['brand']}\nDescrição:\n{description}"

def get_product_description(html_text: str, tag_map: Dict[str, str]) -> Optional[str]:
    """
    Extrai a descrição do produto de um HTML usando um seletor de tag.

    Args:
        html_text (str): Texto HTML da página do produto.
        tag_map (Dict[str, str]): Mapeamento da tag contendo o seletor de caminho ('path').

    Returns:
        Optional[str]: Descrição do produto em texto simples ou None se não encontrado ou inválido.
    """
    try:
        soup = BeautifulSoup(html_text, 'html.parser')

        # Selecionar o conteúdo HTML baseado no caminho especificado no tag_map
        html_content = soup.select_one(tag_map['path'])
        if not html_content:
            return None

        # Converter o HTML para texto simples ignorando links, imagens e ênfases
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.ignore_emphasis = True
        h.body_width = 0

        plain_text = h.handle(str(html_content))

        # Verificar se o texto é muito curto, retornando None se for o caso
        if len(plain_text) < 10:
            return None

        return plain_text

    except Exception as e:
        print(f"Erro na função get_product_description: {e}")
        return None
    
def get_product_url_images(html_text: str, tag_map: Dict[str, str]) -> Optional[List[str]]:
    try:
        # Criar o objeto BeautifulSoup
        soup = BeautifulSoup(html_text, 'html.parser')

        # Selecionar todos os elementos que correspondem ao caminho no tag_map
        html_content = soup.select(tag_map['path'])
        
        if not html_content:
            return None
        
        # Capturar todos os links de imagens
        image_urls = []
        for element in html_content:
            # Procurar por tags <img> dentro do elemento
            imgs_tag = element.find_all('img')
            for img_tag in imgs_tag:
                if img_tag and 'src' in img_tag.attrs:
                    img_src = img_tag['src']
                    if img_src:
                        img_src = img_src.replace("//www.", "https://www.")
                        image_urls.append(img_src)

        return image_urls if image_urls else None
    except Exception as e:
        print(f"Erro na função get_product_url_images: {e}")
        return None