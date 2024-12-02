import re
import copy
from typing import Any, Dict, List
import pandas as pd

from src.lib.utils.file_system import path_exists, read_file
from src.lib.utils.log import message
from src.lib.utils.text_functions import clean_text
from src.lib.wordlist.collection import COLLECTIONS

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)

def extract_tags(description_ai: str) -> str:
    """Extrai e limpa tags do texto de descrição."""
    tags = re.findall(r'#\w+', description_ai)
    tags_modificadas = [re.sub(r'([a-z])([A-Z])', r'\1 \2', tag[1:]) for tag in tags]
    clean_tags = " , ".join([clean_text(tag) for tag in tags_modificadas])
    return clean_tags

def format_product_definitions(keys: List[str], wordlist: Dict[str, Any], country: str) -> List[str]:
    """Formata as definições de produto para capitalização adequada."""
    definitions = [wordlist[key][country] for key in keys]
    formatted_definitions = [' '.join([w.capitalize() for w in word.split()]) for word in definitions]
    return formatted_definitions

def preprocess_wordlist(wordlist: Dict[str, Any]) -> re.Pattern:
    """
    Pré-processa o wordlist para compilar um padrão regex com grupos nomeados para busca eficiente.
    """
    patterns = []
    for component, info in wordlist.items():
        exact_term = info.get("exact_term", False)
        synonyms = info.get('synonyms', [])
        component_patterns = []
        for synonym in synonyms:
            synonym_cleaned = clean_text(synonym)
            if exact_term:
                pattern = r'\b' + re.escape(synonym_cleaned) + r'\b'
            else:
                pattern = re.escape(synonym_cleaned)
            component_patterns.append(pattern)
        if component_patterns:
            # Certifique-se de que o nome do grupo seja um identificador válido
            group_name = re.sub(r'\W+', '_', component)
            group_pattern = '(?P<' + group_name + '>' + '|'.join(component_patterns) + ')'
            patterns.append(group_pattern)
    combined_pattern = '|'.join(patterns)
    compiled_regex = re.compile(combined_pattern)
    return compiled_regex

def find_matches_in_wordlist(text: str, compiled_regex: re.Pattern) -> List[str]:
    """
    Encontra componentes no texto usando o regex pré-compilado com grupos nomeados.
    
    Args:
        text (str): Texto a ser analisado.
        compiled_regex (re.Pattern): Padrão regex pré-compilado para correspondência.
    
    Returns:
        list: Lista única de componentes encontrados no texto.
    """
    text_cleaned = clean_text(text)
    all_matches = []

    for match in compiled_regex.finditer(text_cleaned):
        component = match.lastgroup  # O nome do grupo que correspondeu
        synonym = match.group(0)
        if component:
            all_matches.append({
                'component': component,
                'synonym': synonym,
                'start': match.start(),
                'end': match.end(),
                'length': match.end() - match.start()
            })

    # Ordena os matches por comprimento descendente e posição de início
    all_matches_sorted = sorted(all_matches, key=lambda x: (-x['length'], x['start']))

    selected_matches = []
    occupied = [False] * len(text_cleaned)

    for match in all_matches_sorted:
        if any(occupied[pos] for pos in range(match['start'], match['end'])):
            continue
        selected_matches.append(match)
        for pos in range(match['start'], match['end']):
            occupied[pos] = True

    # Coleta os componentes únicos dos matches selecionados
    found_components = {match['component'] for match in selected_matches}
    return list(found_components)

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.component = None
        self.exact_term = False

# Função para inserir palavras na Trie
def insert_into_trie(root, word, component, exact_term):
    node = root
    for char in word:
        node = node.children.setdefault(char, TrieNode())
    node.is_end = True
    node.component = component
    node.exact_term = exact_term

# Função para construir a Trie a partir do wordlist
def build_trie(wordlist):
    root = TrieNode()
    for component, info in wordlist.items():
        exact_term = info.get("exact_term", False)
        synonyms = info.get('synonyms', [])
        for synonym in synonyms:
            synonym_cleaned = clean_text(synonym)
            insert_into_trie(root, synonym_cleaned, component, exact_term)
    return root

# Função para pesquisar na Trie
def search_trie(text, root, wordlist):
    text_cleaned = clean_text(text)
    n = len(text_cleaned)
    all_matches = []

    for i in range(n):
        node = root
        j = i
        while j < n and text_cleaned[j] in node.children:
            node = node.children[text_cleaned[j]]
            if node.is_end:
                start = i
                end = j + 1
                word_found = text_cleaned[start:end]
                # Verifica o termo exato se necessário
                if node.exact_term:
                    if (start > 0 and text_cleaned[start - 1].isalnum()) or \
                       (end < n and text_cleaned[end].isalnum()):
                        j += 1
                        continue  # Não é um termo exato
                all_matches.append({
                    'component': node.component,
                    'synonym': word_found,
                    'start': start,
                    'end': end,
                    'length': end - start,
                })
            j += 1

    # Ordena os matches por comprimento decrescente e posição inicial crescente
    all_matches_sorted = sorted(all_matches, key=lambda x: (-x['length'], x['start']))

    selected_matches = []
    occupied = [False] * n
    found_components = []
    existing_components = set()
    component_conflicts = {component: set(info.get('conflict', [])) for component, info in wordlist.items()}

    for match in all_matches_sorted:
        # Verifica sobreposição
        if any(occupied[pos] for pos in range(match['start'], match['end'])):
            continue
        # Verifica conflitos
        component = match['component']
        conflicts = component_conflicts.get(component, set())
        if conflicts & existing_components:
            continue
        # Seleciona o match
        selected_matches.append(match)
        for pos in range(match['start'], match['end']):
            occupied[pos] = True
        found_components.append(component)
        existing_components.add(component)

    return found_components


# Função para extrair termos relevantes
def extract_collection_terms_in_text(found_components: List[str], required_keys: List[str], collection_key: str) -> Dict[str, List[str]]:
    terms = [item for item in required_keys if item in found_components]
    if (collection_key == "product") and (not all(item in found_components for item in required_keys)):
        return {"terms": []}
    return {"terms": terms}

# Função para processar os termos da coleção
def process_collection_terms(text: str, trie_root, trie_root_flavor, collection: Dict[str, Any],
                             wordlist: Dict[str, Any], wordlist_flavor: Dict[str, Any]) -> Dict[str, Dict[str, List[str]]]:
    terms = {}
    # Processa os termos gerais
    found_components = search_trie(text, trie_root, wordlist)
    terms["product"] = extract_collection_terms_in_text(found_components, collection["product"], "product")
    terms["features"] = extract_collection_terms_in_text(found_components, collection["features"], "features")
    terms["ingredients"] = extract_collection_terms_in_text(found_components, collection["ingredients"], "ingredients")
    terms["format"] = extract_collection_terms_in_text(found_components, collection["format"], "format")
    terms["is_not"] = extract_collection_terms_in_text(found_components, collection["is_not"], "is_not")
    # Processa os termos de sabor
    found_flavors = search_trie(text, trie_root_flavor, wordlist_flavor)
    terms["flavor"] = extract_collection_terms_in_text(found_flavors, collection["flavor"], "flavor")
    return terms

# Função principal para obter as coleções
def get_collections(
    row, 
    title: str, 
    product_class: str, 
    flavor_ai: str, 
    description_ai: str, 
    trie_root, 
    trie_root_flavor,
    wordlist: Dict[str, Any], 
    wordlist_flavor: Dict[str, Any]
) -> List[str]:
    
    if not description_ai:
        description_ai = ""

    all_collections = []
    product_tags = []
    title_field = {'product': [], 'features': [], 'ingredients': [], 'flavor': []}
    for key, collection in COLLECTIONS.items():
        score = 0
        collections_found = []

        # Process the terms of the title, description_ai, and tags
        title_terms = process_collection_terms(title, trie_root, trie_root_flavor, collection, wordlist, wordlist_flavor)
        product_class_terms = process_collection_terms(product_class, trie_root, trie_root_flavor, collection, wordlist, wordlist_flavor)
        
        if title_terms["is_not"]["terms"] or product_class_terms["is_not"]["terms"]:
            continue

        description_ai_terms = process_collection_terms(description_ai, trie_root, trie_root_flavor, collection, wordlist, wordlist_flavor)
        flavor_terms = process_collection_terms(flavor_ai, trie_root, trie_root_flavor, collection, wordlist, wordlist_flavor)

        tags = extract_tags(description_ai)
        tags_terms = process_collection_terms(tags, trie_root, trie_root_flavor, collection, wordlist, wordlist_flavor)

        tags = extract_tags(description_ai)
        tags_terms = process_collection_terms(tags, trie_root, trie_root_flavor, collection, wordlist, wordlist_flavor)
        
        categories = ["product", "features", "ingredients", "format", "flavor"]

        sources = [title_terms, product_class_terms, flavor_terms, tags_terms]

        product_tags.extend(
            [term for source in sources for category in categories for term in source[category]["terms"]]
        )

        # Verifica se há muitos termos "is_not"
        flag_in_title = title_terms["product"]["terms"] or product_class_terms["product"]["terms"]
        if ((not flag_in_title) and (len(description_ai_terms["is_not"]["terms"]) > 2) or (len(tags_terms["is_not"]["terms"]) > 2)):
            continue
        
        score = (
            len(product_class_terms["product"]["terms"]) * 3 +
            len(title_terms["product"]["terms"]) * 2 +
            len(description_ai_terms["product"]["terms"]) * 0.4 +
            len(tags_terms["product"]["terms"]) * 0.5
        )
        
        # Combina todos os sabores encontrados
        flavors = set(title_terms["flavor"]["terms"])
        if (not flavors):
            flavors.update(description_ai_terms["flavor"]["terms"])
            flavors.update(flavor_terms["flavor"]["terms"])
            flavors.update(tags_terms["flavor"]["terms"])

        # Clona os índices da coleção
        collection_indices = copy.copy(collection["indices"])

        if collection.get("score_per_ingredients"):
            score_ingredients = (
                len(title_terms["ingredients"]["terms"]) * 0.1 +
                len(description_ai_terms["ingredients"]["terms"]) * 0.3 +
                len(tags_terms["ingredients"]["terms"]) * 0.3
            )
            
            if (score_ingredients > 0):
                title_terms["product"]["terms"] = list(set(collection["product"] + title_terms["product"]["terms"]))
                score += score_ingredients

        # Adiciona sabores aos índices, se aplicável
        if flavors and collection.get("indices_flavor"):
            indices_flavor = copy.copy(collection["indices_flavor"])
            for flavor in flavors:
                for key_index_flavor, value_index_flavor in indices_flavor.items():
                    # Atualiza o sabor nos índices
                    flavored_index = copy.copy(value_index_flavor)
                    flavored_index["flavor"] = flavor
                    index_key = f"{key_index_flavor} {flavor.replace("_", " ").title()}"
                    collection_indices[index_key] = flavored_index

    
        # Verifica se os termos correspondem aos índices
        for key_index, index in collection_indices.items():
            required_terms = len(index)
            matched_terms = 0
            for key_term, term in index.items():
                title_terms_aux = title_terms.get(key_term, {}).get("terms", [])
                product_class_terms_aux = product_class_terms.get(key_term, {}).get("terms", [])
                description_ai_terms_aux = description_ai_terms.get(key_term, {}).get("terms", [])
                flavor_terms_aux = flavor_terms.get(key_term, {}).get("terms", [])
                tags_terms_aux = tags_terms.get(key_term, {}).get("terms", [])

                all_terms = set(title_terms_aux).union(
                    product_class_terms_aux, 
                    description_ai_terms_aux, 
                    flavor_terms_aux, 
                    tags_terms_aux
                )

                if term in all_terms:
                    matched_terms += 1
            if matched_terms == required_terms:
                collections_found.append(key_index)
        
        
        # Aplica regras baseadas na quantidade
        rule_fields = collection.get("rule_fields")
        flag_incorrect_quantity = False
        if collections_found and rule_fields and pd.notna(row.quantity):
            quantity = int(row.quantity)
            unit_of_measure = row.unit_of_measure
            for rule_field in rule_fields:
                greater_than_equal, less_than_equal = rule_field["range"]
                if ((greater_than_equal <= quantity <= less_than_equal)):
                    
                    collections_found.append(rule_field['name'])
                        
                elif rule_field.get('required'):
                    flag_incorrect_quantity = True
        
        if flag_incorrect_quantity:
            continue
        
        # Adiciona coleções padrão
        default_collection = collection.get("default_collection")
        if collections_found and default_collection:
            collections_found += default_collection

        promotion_collection = collection.get("promotion_collection")
        
        if promotion_collection and collections_found and pd.notna(row.compare_at_price):
            collections_found.append(promotion_collection)
        
        title_field = {
            "product": title_terms["product"]["terms"],
            "features": title_terms["features"]["terms"],
            "ingredients": title_terms["ingredients"]["terms"],
            "flavor": title_terms["flavor"]["terms"]
        }
        
        # Calcula o score e adiciona à lista de todas as coleções
        if collections_found:
            all_collections.append({
                "score": score,
                "collections": collections_found,
                "title_field": title_field
            })
    
    # Seleciona a coleção com maior score
    product_score = 0
    collections_chosed = []
    if all_collections:
        collections_chosed = max(all_collections, key=lambda x: x["score"])
        
        product_score = int(collections_chosed['score'] * 100)

        title_field = collections_chosed["title_field"]
        collections_chosed = collections_chosed["collections"]

    product_tags = list(set(product_tags))
    collections_chosed = list(set(collections_chosed))
    return collections_chosed, product_tags, title_field, product_score

# Função principal para criar as colunas de produto
def create_product_cols(df: pd.DataFrame, conf: Dict[str, Any]) -> pd.DataFrame:
    message("Criando colunas de descrição do produto")

    wordlist = conf["wordlist"]
    wordlist_flavor = conf["wordlist_flavor"]
    country = conf["country"]

    # Build the Tries from the wordlists
    trie_root = build_trie(wordlist)
    trie_root_flavor = build_trie(wordlist_flavor)

    collections_list = []
    title_terms_list = []
    product_tags_list = []
    product_score_list = []

    # Optimize iteration using itertuples
    for row in df.itertuples(index=False):
        ref = row.ref
        title = row.title

        message(f'ref - {ref} | {title} | create_product_cols ')
        
        description_ai_path = f"{conf['data_path']}/products/{ref}_description_ai.txt"
        description_ai = read_file(description_ai_path) if path_exists(description_ai_path) else ""

        product_class_path = f"{conf['data_path']}/products/{ref}_class.txt"
        product_class = read_file(product_class_path) if path_exists(product_class_path) else ""
        
        flavor_ai_path = f"{conf['data_path']}/products/{ref}_flavor_ai.txt"
        flavor_ai = read_file(flavor_ai_path) if path_exists(flavor_ai_path) else ""

        collections, product_tags, title_terms, product_score = get_collections(
            row, 
            title,
            product_class,
            flavor_ai,
            description_ai, 
            trie_root, 
            trie_root_flavor, 
            wordlist, 
            wordlist_flavor
        )

        collections_list.append(collections)
        product_tags_list.append(", ".join([wordlist[tags][country].title() for tags in product_tags]))
        title_terms_list.append(title_terms)
        product_score_list.append(product_score)
    
    df['collections'] = collections_list
    df['product_tags'] = product_tags_list
    df['title_terms'] = title_terms_list
    df['product_score'] = product_score_list
    return df
