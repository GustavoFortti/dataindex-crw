import re
import copy
from typing import Any, Dict, List, Set, Optional, Pattern, Tuple
import pandas as pd

from src.lib.utils.file_system import file_or_path_exists, read_file
from src.lib.utils.log import message
from src.lib.utils.text_functions import clean_text
from src.lib.wordlist.collection import COLLECTIONS
from src.jobs.pipeline import JobBase


def extract_tags(description_ai: str) -> str:
    """
    Extracts and cleans tags from the description text.

    Args:
        description_ai (str): The description text containing tags.

    Returns:
        str: A string of cleaned tags separated by commas.
    """
    tags: List[str] = re.findall(r'#\w+', description_ai)
    tags_modificadas: List[str] = [re.sub(r'([a-z])([A-Z])', r'\1 \2', tag[1:]) for tag in tags]
    clean_tags: str = " , ".join([clean_text(tag) for tag in tags_modificadas])
    return clean_tags


def format_product_definitions(keys: List[str], wordlist: Dict[str, Any], country: str) -> List[str]:
    """
    Formats product definitions for proper capitalization.

    Args:
        keys (List[str]): List of keys to retrieve definitions from the wordlist.
        wordlist (Dict[str, Any]): The wordlist containing definitions.
        country (str): The country code to select the appropriate language.

    Returns:
        List[str]: A list of formatted product definitions.
    """
    definitions: List[str] = [wordlist[key][country] for key in keys]
    formatted_definitions: List[str] = [' '.join([w.capitalize() for w in word.split()]) for word in definitions]
    return formatted_definitions


def preprocess_wordlist(wordlist: Dict[str, Any]) -> Pattern:
    """
    Preprocesses the wordlist to compile a regex pattern with named groups for efficient searching.

    Args:
        wordlist (Dict[str, Any]): The wordlist containing components and synonyms.

    Returns:
        Pattern: The compiled regex pattern.
    """
    patterns: List[str] = []
    for component, info in wordlist.items():
        exact_term: bool = info.get("exact_term", False)
        synonyms: List[str] = info.get('synonyms', [])
        component_patterns: List[str] = []
        for synonym in synonyms:
            synonym_cleaned: str = clean_text(synonym)
            if exact_term:
                pattern: str = r'\b' + re.escape(synonym_cleaned) + r'\b'
            else:
                pattern = re.escape(synonym_cleaned)
            component_patterns.append(pattern)
        if component_patterns:
            # Ensure the group name is a valid identifier
            group_name: str = re.sub(r'\W+', '_', component)
            group_pattern: str = '(?P<' + group_name + '>' + '|'.join(component_patterns) + ')'
            patterns.append(group_pattern)
    combined_pattern: str = '|'.join(patterns)
    compiled_regex: Pattern = re.compile(combined_pattern)
    return compiled_regex


def find_matches_in_wordlist(text: str, compiled_regex: Pattern) -> List[str]:
    """
    Finds components in the text using the precompiled regex with named groups.

    Args:
        text (str): The text to analyze.
        compiled_regex (Pattern): The precompiled regex pattern for matching.

    Returns:
        List[str]: A list of unique components found in the text.
    """
    text_cleaned: str = clean_text(text)
    all_matches: List[Dict[str, Any]] = []

    for match in compiled_regex.finditer(text_cleaned):
        component: Optional[str] = match.lastgroup  # The name of the matched group
        synonym: str = match.group(0)
        if component:
            all_matches.append({
                'component': component,
                'synonym': synonym,
                'start': match.start(),
                'end': match.end(),
                'length': match.end() - match.start()
            })

    # Sort matches by descending length and starting position
    all_matches_sorted: List[Dict[str, Any]] = sorted(all_matches, key=lambda x: (-x['length'], x['start']))

    selected_matches: List[Dict[str, Any]] = []
    occupied: List[bool] = [False] * len(text_cleaned)

    for match in all_matches_sorted:
        if any(occupied[pos] for pos in range(match['start'], match['end'])):
            continue
        selected_matches.append(match)
        for pos in range(match['start'], match['end']):
            occupied[pos] = True

    # Collect unique components from selected matches
    found_components: Set[str] = {match['component'] for match in selected_matches}
    return list(found_components)


class TrieNode:
    def __init__(self) -> None:
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end: bool = False
        self.component: Optional[str] = None
        self.exact_term: bool = False


def insert_into_trie(root: TrieNode, word: str, component: str, exact_term: bool) -> None:
    """
    Inserts words into the Trie.

    Args:
        root (TrieNode): The root node of the Trie.
        word (str): The word to insert.
        component (str): The component associated with the word.
        exact_term (bool): Flag indicating if the term should be matched exactly.
    """
    node: TrieNode = root
    for char in word:
        node = node.children.setdefault(char, TrieNode())
    node.is_end = True
    node.component = component
    node.exact_term = exact_term


def build_trie(wordlist: Dict[str, Any]) -> TrieNode:
    """
    Builds a Trie from the wordlist.

    Args:
        wordlist (Dict[str, Any]): The wordlist containing components and synonyms.

    Returns:
        TrieNode: The root of the constructed Trie.
    """
    root: TrieNode = TrieNode()
    for component, info in wordlist.items():
        exact_term: bool = info.get("exact_term", False)
        synonyms: List[str] = info.get('synonyms', [])
        for synonym in synonyms:
            synonym_cleaned: str = clean_text(synonym)
            insert_into_trie(root, synonym_cleaned, component, exact_term)
    return root


def search_trie(text: str, root: TrieNode, wordlist: Dict[str, Any]) -> List[str]:
    """
    Searches for components in the text using the Trie.

    Args:
        text (str): The text to search.
        root (TrieNode): The root node of the Trie.
        wordlist (Dict[str, Any]): The wordlist containing components and synonyms.

    Returns:
        List[str]: A list of found components.
    """
    text_cleaned: str = clean_text(text)
    n: int = len(text_cleaned)
    all_matches: List[Dict[str, Any]] = []

    for i in range(n):
        node: TrieNode = root
        j: int = i
        while j < n and text_cleaned[j] in node.children:
            node = node.children[text_cleaned[j]]
            if node.is_end:
                start: int = i
                end: int = j + 1
                word_found: str = text_cleaned[start:end]
                # Check for exact term if necessary
                if node.exact_term:
                    if (start > 0 and text_cleaned[start - 1].isalnum()) or \
                       (end < n and text_cleaned[end].isalnum()):
                        j += 1
                        continue  # Not an exact term
                all_matches.append({
                    'component': node.component,
                    'synonym': word_found,
                    'start': start,
                    'end': end,
                    'length': end - start,
                })
            j += 1

    # Sort matches by descending length and ascending start position
    all_matches_sorted: List[Dict[str, Any]] = sorted(all_matches, key=lambda x: (-x['length'], x['start']))

    selected_matches: List[Dict[str, Any]] = []
    occupied: List[bool] = [False] * n
    found_components: List[str] = []
    existing_components: Set[str] = set()
    component_conflicts: Dict[str, Set[str]] = {component: set(info.get('conflict', [])) for component, info in wordlist.items()}

    for match in all_matches_sorted:
        # Check for overlap
        if any(occupied[pos] for pos in range(match['start'], match['end'])):
            continue
        # Check for conflicts
        component: str = match['component']
        conflicts: Set[str] = component_conflicts.get(component, set())
        if conflicts & existing_components:
            continue
        # Select the match
        selected_matches.append(match)
        for pos in range(match['start'], match['end']):
            occupied[pos] = True
        found_components.append(component)
        existing_components.add(component)

    return found_components


def extract_collection_terms_in_text(found_components: List[str], required_keys: List[str], collection_key: str) -> Dict[str, List[str]]:
    """
    Extracts relevant terms from found components based on required keys.

    Args:
        found_components (List[str]): The list of components found in the text.
        required_keys (List[str]): The required keys for the collection.
        collection_key (str): The key of the collection being processed.

    Returns:
        Dict[str, List[str]]: A dictionary containing the terms found.
    """
    terms: List[str] = [item for item in required_keys if item in found_components]
    if (collection_key == "product") and (not all(item in found_components for item in required_keys)):
        return {"terms": []}
    return {"terms": terms}


def process_collection_terms(
    text: str,
    trie_root: TrieNode,
    trie_root_flavor: TrieNode,
    collection: Dict[str, Any],
    wordlist: Dict[str, Any],
    wordlist_flavor: Dict[str, Any]
) -> Dict[str, Dict[str, List[str]]]:
    """
    Processes collection terms from the text.

    Args:
        text (str): The text to process.
        trie_root (TrieNode): The root node of the general Trie.
        trie_root_flavor (TrieNode): The root node of the flavor Trie.
        collection (Dict[str, Any]): The collection definitions.
        wordlist (Dict[str, Any]): The general wordlist.
        wordlist_flavor (Dict[str, Any]): The flavor wordlist.

    Returns:
        Dict[str, Dict[str, List[str]]]: A dictionary containing terms categorized by collection keys.
    """
    terms: Dict[str, Dict[str, List[str]]] = {}
    # Process general terms
    found_components: List[str] = search_trie(text, trie_root, wordlist)
    terms["product"] = extract_collection_terms_in_text(found_components, collection["product"], "product")
    terms["features"] = extract_collection_terms_in_text(found_components, collection["features"], "features")
    terms["ingredients"] = extract_collection_terms_in_text(found_components, collection["ingredients"], "ingredients")
    terms["format"] = extract_collection_terms_in_text(found_components, collection["format"], "format")
    terms["is_not"] = extract_collection_terms_in_text(found_components, collection["is_not"], "is_not")
    # Process flavor terms
    found_flavors: List[str] = search_trie(text, trie_root_flavor, wordlist_flavor)
    terms["flavor"] = extract_collection_terms_in_text(found_flavors, collection["flavor"], "flavor")
    return terms


def get_collections(
    row: Any,
    title: str,
    product_class: str,
    flavor_ai: str,
    description_ai: str,
    trie_root: TrieNode,
    trie_root_flavor: TrieNode,
    wordlist: Dict[str, Any],
    wordlist_flavor: Dict[str, Any]
) -> Tuple[List[str], List[str], Dict[str, List[str]], int]:
    """
    Main function to obtain collections for a product.

    Args:
        row (Any): The row from the DataFrame.
        title (str): The product title.
        product_class (str): The product class.
        flavor_ai (str): Flavor information.
        description_ai (str): AI-generated description.
        trie_root (TrieNode): The root node of the general Trie.
        trie_root_flavor (TrieNode): The root node of the flavor Trie.
        wordlist (Dict[str, Any]): The general wordlist.
        wordlist_flavor (Dict[str, Any]): The flavor wordlist.

    Returns:
        Tuple[List[str], List[str], Dict[str, List[str]], int]: Collections chosen, product tags, title terms, and product score.
    """
    if not description_ai:
        description_ai = ""

    all_collections: List[Dict[str, Any]] = []
    product_tags: List[str] = []
    title_field: Dict[str, List[str]] = {'product': [], 'features': [], 'ingredients': [], 'flavor': []}
    for key, collection in COLLECTIONS.items():
        score: float = 0.0
        collections_found: List[str] = []

        # Process the terms of the title, description_ai, and tags
        title_terms: Dict[str, Dict[str, List[str]]] = process_collection_terms(
            title, trie_root, trie_root_flavor, collection, wordlist, wordlist_flavor)
        product_class_terms: Dict[str, Dict[str, List[str]]] = process_collection_terms(
            product_class, trie_root, trie_root_flavor, collection, wordlist, wordlist_flavor)
        
        if title_terms["is_not"]["terms"] or product_class_terms["is_not"]["terms"]:
            continue

        description_ai_terms: Dict[str, Dict[str, List[str]]] = process_collection_terms(
            description_ai, trie_root, trie_root_flavor, collection, wordlist, wordlist_flavor)
        flavor_terms: Dict[str, Dict[str, List[str]]] = process_collection_terms(
            flavor_ai, trie_root, trie_root_flavor, collection, wordlist, wordlist_flavor)

        tags: str = extract_tags(description_ai)
        tags_terms: Dict[str, Dict[str, List[str]]] = process_collection_terms(
            tags, trie_root, trie_root_flavor, collection, wordlist, wordlist_flavor)
        
        categories: List[str] = ["product", "features", "ingredients", "format", "flavor"]

        sources: List[Dict[str, Dict[str, List[str]]]] = [title_terms, product_class_terms, flavor_terms, tags_terms]

        product_tags.extend(
            [term for source in sources for category in categories for term in source[category]["terms"]]
        )

        # Check for too many "is_not" terms
        flag_in_title: bool = bool(title_terms["product"]["terms"] or product_class_terms["product"]["terms"])
        if ((not flag_in_title) and (len(description_ai_terms["is_not"]["terms"]) > 2) or (len(tags_terms["is_not"]["terms"]) > 2)):
            continue
        
        score = (
            len(product_class_terms["product"]["terms"]) * 3 +
            len(title_terms["product"]["terms"]) * 2 +
            len(description_ai_terms["product"]["terms"]) * 0.4 +
            len(tags_terms["product"]["terms"]) * 0.5
        )
        
        # Combine all found flavors
        flavors: Set[str] = set(title_terms["flavor"]["terms"])
        if not flavors:
            flavors.update(description_ai_terms["flavor"]["terms"])
            flavors.update(flavor_terms["flavor"]["terms"])
            flavors.update(tags_terms["flavor"]["terms"])

        # Clone the collection indices
        collection_indices: Dict[str, Dict[str, str]] = copy.copy(collection["indices"])

        if collection.get("score_per_ingredients"):
            score_ingredients: float = (
                len(title_terms["ingredients"]["terms"]) * 0.1 +
                len(description_ai_terms["ingredients"]["terms"]) * 0.3 +
                len(tags_terms["ingredients"]["terms"]) * 0.3
            )
            
            if score_ingredients > 0:
                title_terms["product"]["terms"] = list(set(collection["product"] + title_terms["product"]["terms"]))
                score += score_ingredients

        # Add flavors to indices if applicable
        if flavors and collection.get("indices_flavor"):
            indices_flavor: Dict[str, Dict[str, str]] = copy.copy(collection["indices_flavor"])
            for flavor in flavors:
                for key_index_flavor, value_index_flavor in indices_flavor.items():
                    # Update flavor in indices
                    flavored_index: Dict[str, str] = copy.copy(value_index_flavor)
                    flavored_index["flavor"] = flavor
                    index_key: str = f"{key_index_flavor} {flavor.replace('_', ' ').title()}"
                    collection_indices[index_key] = flavored_index

        # Check if terms match the indices
        for key_index, index in collection_indices.items():
            required_terms: int = len(index)
            matched_terms: int = 0
            for key_term, term in index.items():
                title_terms_aux: List[str] = title_terms.get(key_term, {}).get("terms", [])
                product_class_terms_aux: List[str] = product_class_terms.get(key_term, {}).get("terms", [])
                description_ai_terms_aux: List[str] = description_ai_terms.get(key_term, {}).get("terms", [])
                flavor_terms_aux: List[str] = flavor_terms.get(key_term, {}).get("terms", [])
                tags_terms_aux: List[str] = tags_terms.get(key_term, {}).get("terms", [])

                all_terms: Set[str] = set(title_terms_aux).union(
                    product_class_terms_aux, 
                    description_ai_terms_aux, 
                    flavor_terms_aux, 
                    tags_terms_aux
                )

                if term in all_terms:
                    matched_terms += 1
            if matched_terms == required_terms:
                collections_found.append(key_index)
        
        # Apply rules based on quantity
        rule_fields: Optional[List[Dict[str, Any]]] = collection.get("rule_fields")
        flag_incorrect_quantity: bool = False
        if collections_found and rule_fields and pd.notna(row.quantity):
            quantity: int = int(row.quantity)
            for rule_field in rule_fields:
                greater_than_equal, less_than_equal = rule_field["range"]
                if greater_than_equal <= quantity <= less_than_equal:
                    collections_found.append(rule_field['name'])
                elif rule_field.get('required'):
                    flag_incorrect_quantity = True
        
        if flag_incorrect_quantity:
            continue
        
        # Add default collections
        default_collection: Optional[List[str]] = collection.get("default_collection")
        if collections_found and default_collection:
            collections_found += default_collection

        promotion_collection: Optional[str] = collection.get("promotion_collection")
        
        if promotion_collection and collections_found and pd.notna(row.compare_at_price):
            collections_found.append(promotion_collection)
        
        title_field = {
            "product": title_terms["product"]["terms"],
            "features": title_terms["features"]["terms"],
            "ingredients": title_terms["ingredients"]["terms"],
            "flavor": title_terms["flavor"]["terms"]
        }
        
        # Calculate the score and add to the list of all collections
        if collections_found:
            all_collections.append({
                "score": score,
                "collections": collections_found,
                "title_field": title_field
            })
    
    # Select the collection with the highest score
    product_score: int = 0
    collections_chosed: List[str] = []
    if all_collections:
        collections_max: Dict[str, Any] = max(all_collections, key=lambda x: x["score"])
        product_score = int(collections_max['score'] * 100)

        title_field = collections_max["title_field"]
        collections_chosed = collections_max["collections"]

    product_tags = list(set(product_tags))
    collections_chosed = list(set(collections_chosed))
    return collections_chosed, product_tags, title_field, product_score


def create_product_cols(job_base: JobBase, df: pd.DataFrame) -> pd.DataFrame:
    """
    Main function to create product description columns.

    Args:
        job_base (JobBase): The job base object containing configurations.
        df (pd.DataFrame): The DataFrame containing product data.

    Returns:
        pd.DataFrame: The DataFrame with new product columns added.
    """
    message("Creating product description columns")

    wordlist: Dict[str, Any] = job_base.page.wordlist
    wordlist_flavor: Dict[str, Any] = job_base.page.wordlist_flavor
    country: str = job_base.country

    # Build the Tries from the wordlists
    trie_root: TrieNode = build_trie(wordlist)
    trie_root_flavor: TrieNode = build_trie(wordlist_flavor)

    collections_list: List[List[str]] = []
    title_terms_list: List[Dict[str, List[str]]] = []
    product_tags_list: List[str] = []
    product_score_list: List[int] = []

    # Optimize iteration using itertuples
    for row in df.itertuples(index=False):
        ref: str = row.ref
        title: str = row.title

        message(f'ref - {ref} | {title} | create_product_cols ')
        
        description_ai_path: str = f"{job_base.products_path}/{ref}_description_ai.txt"
        description_ai: str = read_file(description_ai_path) if file_or_path_exists(description_ai_path) else ""

        product_class_path: str = f"{job_base.products_path}/{ref}_class.txt"
        product_class: str = read_file(product_class_path) if file_or_path_exists(product_class_path) else ""
        
        flavor_ai_path: str = f"{job_base.products_path}/{ref}_flavor_ai.txt"
        flavor_ai: str = read_file(flavor_ai_path) if file_or_path_exists(flavor_ai_path) else ""

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
        product_tags_formatted: str = ", ".join([wordlist[tags][country].title() for tags in product_tags])
        product_tags_list.append(product_tags_formatted)
        title_terms_list.append(title_terms)
        product_score_list.append(product_score)
    
    df['collections'] = collections_list
    df['product_tags'] = product_tags_list
    df['title_terms'] = title_terms_list
    df['product_score'] = product_score_list
    return df
