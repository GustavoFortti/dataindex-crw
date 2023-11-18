import os
import pandas as pd
import re
from bs4 import BeautifulSoup
from utils.dry_functions import clean_text, path_exist, remove_spaces, loading, find_in_text_with_word_list
from utils.wordlist import BLACK_LIST
pd.set_option('display.max_rows', None)

def init(conf, locations):
    global CONF
    global WORD_LIST

    CONF = conf
    WORD_LIST = CONF['word_list']
    
    file_path = CONF['data_path']

    df = pd.read_csv(file_path + "/origin.csv")
    df = df.drop_duplicates(subset='link_produto').reset_index(drop=True)

    df_nulos = df[df[['titulo', 'preco', 'link_imagem']].isna().any(axis=1)]
    df_nulos.to_csv(file_path + "/origin_del.csv", index=False)

    df = df.dropna(subset=['titulo', 'preco', 'link_imagem'])
    df = df.reset_index(drop=True)

    df['nome'] = df['titulo'].str.lower()
    df['preco'] = df['preco'].str.replace('R$', '').str.replace(' ', '')
    df['marca'] = CONF['marca']
    df['tipo_produto'] = CONF['tipo_produto']
   
    df['preco_numeric'] = df['preco'].str.replace(',', '.').astype(float)
    df['titulo'] = df['titulo'].apply(clean_text)
    df['titulo'] = df['titulo'].apply(remove_spaces)

    df = df[~df['titulo'].apply(lambda x: find_in_text_with_word_list(x, BLACK_LIST))]
    df = keywords_page_specification(df, file_path, locations)
    df = df.dropna(subset=["ref", "titulo", "preco", "link_imagem", "link_produto"], how="any")
    print(df)
    
    return df

def keywords_page_specification(df, file_path, locations):
    products_path = f"{file_path}/products"

    df['especificacao'] = None
    for index, ref in enumerate(df["ref"]):
        loading(index, len(df))
        page_path = f"{products_path}/{ref}.txt"
        keywords_path = f"{products_path}/{ref}_spec.txt"
        keywords_exist = path_exist(keywords_path)

        try:
            product_keywords_path = keywords_path if keywords_exist else page_path
            
            with open(product_keywords_path, 'r') as product_file:
                product = product_file.read()
                keywords = []
                
                if ((not keywords_exist) or (not product)):
                    soup = BeautifulSoup(product, 'html.parser')
                    for location in locations:
                        tag = soup.find(location['tag'], class_=location['class'])
                        if (tag == None): continue
                        keywords = find_matches(tag.text, 3)
                    
                        if (keywords != []): break
                else:
                    keywords = product

                df.loc[index, 'especificacao'] = keywords
                with open(keywords_path, 'w') as new_file:
                    new_file.write(keywords)
        except:
            df.loc[index, 'especificacao'] = None

    print()
    keywords_page(df, file_path)
    print()
    df['especificacao_rota'] = df.apply(lambda row: None if row['especificacao'] is not None else row['especificacao_rota'], axis=1)

    return df

def keywords_page(df, file_path):
    products_path = f"{file_path}/products"

    df['especificacao_rota'] = ""
    for index, ref in enumerate(df["ref"]):
        loading(index, len(df))
        text_path = f"{products_path}/{ref}_text.txt"
        page_path = f"{products_path}/{ref}.txt"
        text_exist = path_exist(text_path)
        
        try:
            product_text_path = text_path if text_exist else page_path

            with open(product_text_path, 'r') as product_file:
                product = product_file.read()

                if (not text_exist):
                    product = clear_page(product)
                    product = ' '.join(product.split())

                words = best_words(product)
                df.loc[index, 'especificacao_rota'] = words

                with open(text_path, 'w') as new_file:
                    new_file.write(product)
        except:
            df.loc[index, 'especificacao_rota'] = None
            print("error file: " + str(ref))

    return df

def clear_page(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')

    remove_tags = ['header', 'footer', 'fieldset', 'select', 'script', 'style', 'iframe', 'svg', 'img', 'link', 'button', 'noscript']
    for remove_tag in remove_tags:
        for tag in soup.find_all(remove_tag):
            tag.decompose()

    tags_com_hidden = soup.find_all(lambda tag: tag.get('class') and 'hidden' in ' '.join(tag.get('class')))
    for tag in tags_com_hidden:
        tag.extract()
        
    def remove_empty_tags(tag):
        if not tag.text.strip():
            tag.extract()

    for tag in soup.find_all():
        remove_empty_tags(tag)

    tags_with_char_count = [(tag, len(tag.get_text(strip=True))) for tag in soup.find_all()]
    sorted_tags = sorted(tags_with_char_count, key=lambda x: x[1], reverse=True)
    half_count = int(len(sorted_tags) // 3)

    for tag, _ in sorted_tags[half_count:]:
        tag.decompose()

    return soup.get_text()

def best_words(text):
    text = clean_text(text)

    words_count = {}
    for item in WORD_LIST:
        for sub_item in item:
            count = len(re.findall(clean_text(sub_item), text))
            if (count != 0):
                words_count[sub_item] = count
                break

    if (words_count == {}):
        return None

    words_count = dict(sorted(words_count.items(), key=lambda item: item[1], reverse=True))
    limit = int(list(words_count.values())[0] * 0.30)
    words = ""
    limit_size = 3
    for item, value in words_count.items():
        if ((value >= limit) & (limit_size > 0)): 
            limit_size -= 1
            words += f" {item}"
        else: break

    return words

def find_matches(text, max_size=10):
    text = clean_text(text)
    keywords = []
    
    for item in WORD_LIST:
        for sub_item in item:
            word = clean_text(sub_item)
            if (re.search(word, text)):
                keywords.append(word)
                break

    if (keywords):
        keywords = keywords[:max_size] if (len(keywords) > max_size) else keywords
        return ' '.join(keywords)
    return None

def create_table(soup):
    try:
        dfs = []
        tables = soup.find_all('table')
        for table in tables:
            table_data = []

            # Loop pelas linhas da tabela
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                data_row = [cell.text.strip() for cell in cells]
                table_data.append(data_row)

            # Remova as linhas vazias
            table_data = [row for row in table_data if row]

            # Verifique se há dados suficientes para criar um DataFrame
            if len(table_data) > 1 and all(len(row) == len(table_data[0]) for row in table_data):
                # A primeira linha contém os cabeçalhos das colunas
                columns = table_data[0]
                
                # Os dados reais começam na segunda linha
                data = table_data[1:]
                
                # Criar um DataFrame pandas a partir dos dados
                df = pd.DataFrame(data, columns=columns)
                
                # Exibir o DataFrame
                primeira_coluna = df['A']
                for valor in primeira_coluna:
                    comando = f'echo {valor}>>./wordlist.txt'
                    os.system(comando)

                dfs.append(df)
            else:
                print("Não há dados suficientes para criar um DataFrame.")

            return dfs
    except:
        return None

def create_table_2(soup):
    try: 
        tables = []
        tags = [tag for tag in soup.find_all() if any(re.search(r'\b(tabela|table)\b', class_, re.IGNORECASE) for class_ in tag.get('class', []))]
        for tag in tags:
            body_el = tag.find_all(recursive=False)
            for table_el in body_el:
                table = []
                rows_el = table_el.find_all(recursive=False)
                for row_el in rows_el:
                    row = row_el.find_all()
                    table.append([(clean_text(col.text)) for col in row])
                tables.append(table)

        dfs = []
        for table in tables:
            data = []
            if (len(table) > 1):
                for row in table:
                    if (len(row) == 3):
                        data.append(row)
                        palavra = row[0]
                        comando = f'echo {palavra}>>./wordlist.txt'
                        os.system(comando)

            df = pd.DataFrame(data)
            dfs.append(df)

        return dfs
    except:
        return None