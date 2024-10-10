import re
from typing import List, Dict, Any
import pandas as pd
from src.lib.utils.log import message
from src.lib.utils.py_functions import flatten_list
from src.lib.utils.text_functions import clean_text, get_all_words_with_wordlist
from src.lib.utils.file_system import path_exists, read_file
from src.lib.transform.product_info import load_product_info

def has_conflict(title: str, key: str, wordlist: Dict[str, Any], get_words_func) -> bool:
    """Verifica se há conflitos para uma determinada chave."""
    for conflict_key in wordlist[key].get("conflict", []):
        conflict_words = get_words_func(f" {title} ", wordlist[conflict_key]["subject"], True)
        if conflict_words:
            longest_conflict = max(conflict_words, key=len)
            longest_word = max(get_words_func(f" {title} ", wordlist[key]["subject"], True), key=len)
            if len(longest_conflict) > len(longest_word):
                return True
    return False

def extract_tags(description_ai: str) -> str:
    """Extrai e limpa tags do texto de descrição."""
    tags = re.findall(r'#\w+', description_ai)
    tags_modificadas = [re.sub(r'([a-z])([A-Z])', r'\1 \2', tag[1:]) for tag in tags]
    clean_tags = " , ".join([clean_text(tag) for tag in tags_modificadas])
    return clean_tags

def find_product_keys(text: str, wordlist: Dict[str, Any]) -> List[str]:
    """Encontra as chaves de definição de produto com base no texto fornecido."""
    product_definition_key = []
    for key, attributes in wordlist.items():
        words = get_all_words_with_wordlist(f" {text} ", attributes["subject"], True)
        if not words:
            continue
        if has_conflict(text, key, wordlist, get_all_words_with_wordlist):
            continue
        product_definition_key.append(key)
    return flatten_list(product_definition_key)

def format_product_definitions(keys: List[str], wordlist: Dict[str, Any], country: str) -> List[str]:
    """Formata as definições de produto para capitalização adequada."""
    definitions = [wordlist[key][country] for key in keys]
    formatted_definitions = [' '.join([w.capitalize() for w in word.split()]) for word in definitions]
    return formatted_definitions

def create_product_definition_col(df: pd.DataFrame, conf: Dict[str, Any]) -> pd.DataFrame:
    message("Criando colunas de descrição do produto")
    load_product_info(df, conf)
    
    # Inicializa as colunas no DataFrame
    df["product_definition_key"] = None
    df["product_definition"] = None
    
    wordlist = conf["wordlist"]
    country = conf["country"]

    for idx, row in df.iterrows():
        ref = row['ref']
        title = row['title']
        page_name = row['page_name']
        blacklist_description = ['growth_supplements']
        
        # Processa o título do produto
        product_keys_title = find_product_keys(title, wordlist)

        # Processa a descrição AI, se existir
        description_ai_path = f"{conf.get('data_path', '')}/products/{ref}_description_ai.txt"
        if (path_exists(description_ai_path) & (page_name not in blacklist_description)):
            description_ai = read_file(description_ai_path)
            clean_tags = extract_tags(description_ai)
            product_keys_tags = find_product_keys(clean_tags, wordlist)
            product_keys_title.extend(product_keys_tags)
        
        # Remove duplicatas
        product_keys_unique = list(set(product_keys_title))

        if not product_keys_unique:
            df.at[idx, "product_definition_key"] = None
            df.at[idx, "product_definition"] = None
            continue
        
        # Formata as definições de produto
        product_definitions = format_product_definitions(product_keys_unique, wordlist, country)
        
        # Atualiza o DataFrame
        df.at[idx, "product_definition_key"] = ", ".join(product_keys_unique)
        df.at[idx, "product_definition"] = ", ".join(product_definitions)
    
    return df
