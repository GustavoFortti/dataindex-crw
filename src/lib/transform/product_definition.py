from copy import deepcopy
import re
from typing import List, Dict, Any
import pandas as pd
from src.lib.utils.log import message
from src.lib.utils.py_functions import flatten_list
from src.lib.utils.text_functions import clean_text, get_all_words_with_wordlist
from src.lib.utils.file_system import path_exists, read_file
from src.lib.wordlist.collection import COLLECTIONS

def has_conflict(title: str, key: str, wordlist: Dict[str, Any], get_words_func) -> bool:
    """Verifica se há conflitos para uma determinada chave."""
    for conflict_key in wordlist[key].get("conflict", []):
        conflict_words = get_words_func(f" {title} ", wordlist[conflict_key]["synonyms"], True)
        if conflict_words:
            longest_conflict = max(conflict_words, key=len)
            longest_word = max(get_words_func(f" {title} ", wordlist[key]["synonyms"], True), key=len)
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
        words = get_all_words_with_wordlist(f" {text} ", attributes["synonyms"], True)
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

def extract_collection_terms_in_text(wordlist, text, collection, collection_key):
    wordlist_keys = collection[collection_key]
    terms = []
    for wordlist_key in wordlist_keys:
        words_synonyms = get_all_words_with_wordlist(text, wordlist[wordlist_key]["synonyms"], wordlist[wordlist_key]['exact_term'])
        words_conflict = get_all_words_with_wordlist(text, wordlist[wordlist_key]['conflict'], True)
        
        if (words_synonyms != []):
            terms.append(wordlist_key)
    
    return { "terms": terms }

def process_collection_terms(text, wordlist, wordlist_flavor, collection):
    """
    Extrai os termos de uma coleção e seus sinônimos com base em diferentes categorias
    (sinônimos, características, ingredientes, etc.).
    """
    fields = ["product", "features", "ingredients", "flavor", "format", "is_not"]
    terms = {}
    for field in fields:
        current_wordlist = wordlist_flavor if field == "flavor" else wordlist
        terms[field] = extract_collection_terms_in_text(current_wordlist, text, collection, field)
    return terms

def get_collections(row, title, description, clean_tags, wordlist, wordlist_flavor):
    """
    Processa os termos de coleções de um título e descrição, criando um conjunto de textos para exibição.
    """
    if not description:
        description = ""

    collections_found = []
    for key, collection in COLLECTIONS.items():
        # Processa os termos do título
        title_terms = process_collection_terms(title, wordlist, wordlist_flavor, collection)

        # Remove a coleção se houver termos em "is_not" no título
        if title_terms["is_not"]["terms"]:
            continue
        
        # Processa os termos das tags e descrição
        clean_tags_terms = process_collection_terms(clean_tags, wordlist, wordlist_flavor, collection)
        description_terms = process_collection_terms(description, wordlist, wordlist_flavor, collection)
        
        # Combina todos os sabores encontrados
        flavors = set(
            title_terms["flavor"]["terms"] +
            description_terms["flavor"]["terms"] +
            clean_tags_terms["flavor"]["terms"]
        )

        # Clona os índices da coleção
        collection_indices = deepcopy(collection["indices"])

        # Adiciona sabores aos índices, se aplicável
        if flavors and collection["indices_flavor"] != []:
            indices_flavor = deepcopy(collection["indices_flavor"])
            for flavor in flavors:
                for key_index_flavor, value_index_flavor in indices_flavor.items():
                    # Atualiza o sabor nos índices
                    flavored_index = deepcopy(value_index_flavor)
                    flavored_index["flavor"] = flavor
                    index_key = f"{key_index_flavor}_{flavor}"
                    collection_indices[index_key] = flavored_index

        # Verifica se os termos correspondem aos índices
        for key_index, index in collection_indices.items():
            required_terms = len(index)
            matched_terms = 0
            for key_term, term in index.items():
                all_terms = set(
                    title_terms[key_term]["terms"] +
                    description_terms[key_term]["terms"] +
                    clean_tags_terms[key_term]["terms"]
                )
                if term in all_terms:
                    matched_terms += 1
            if matched_terms == required_terms:
                collections_found.append(key_index)

        rule_fields = collection.get("rule_fields")
        if collections_found and rule_fields:
            for rule_field in rule_fields:
                greater_than_equal, less_than_equal = rule_field["range"]
                if (int(row["quantity"]) >= greater_than_equal and int(row["quantity"]) <= less_than_equal):
                    collections_found.append(f"{key}_{rule_field['name']}")

    return collections_found if collections_found else None

def create_product_cols(df: pd.DataFrame, conf: Dict[str, Any]) -> pd.DataFrame:
    message("Criando colunas de descrição do produto")
    
    # Inicializa as colunas no DataFrame
    df["product_definition_key"] = None
    df["product_definition"] = None
    
    wordlist = conf["wordlist"]
    wordlist_flavor = conf["wordlist_flavor"]
    country = conf["country"]

    for idx, row in df.iterrows():
        ref = row['ref']
        title = row['title']
        
        message(f'ref - {ref} | {title} | create_product_cols ')
        
        page_name = row['page_name']
        blacklist_description = ['growth_supplements']
        
        # Processa o título do produto
        product_keys_title = find_product_keys(title, wordlist)

        # Processa a descrição AI, se existir
        description_ai = None
        clean_tags = ""
        description_ai_path = f"{conf.get('data_path', '')}/products/{ref}_description_ai.txt"
        if (path_exists(description_ai_path) & (page_name not in blacklist_description)):
            description_ai = read_file(description_ai_path)
            clean_tags = extract_tags(description_ai)
            product_keys_tags = find_product_keys(clean_tags, wordlist)
            product_keys_title.extend(product_keys_tags)
        
        collections = get_collections(row, title, description_ai, clean_tags, wordlist, wordlist_flavor)
        df.at[idx, "collections"] = str(collections)
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
