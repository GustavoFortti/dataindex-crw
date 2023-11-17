import os
import pandas as pd
import re
from bs4 import BeautifulSoup
from utils.dry_functions import clean_text, path_exist, remove_spaces, loading

pd.set_option('display.max_rows', None)

def init(conf, location):
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

    df = keywords_page_specification(df, file_path, location)
    print(df)

    return df

def keywords_page_specification(df, file_path, location):
    products_path = f"{file_path}/products"

    df['especificacao'] = None
    for index, ref in enumerate(df["ref"]):
        loading(index, len(df))
        page_path = f"{products_path}/{ref}.txt"

        try:
            with open(page_path, 'r') as product_file:
                html_text = product_file.read()
                soup = BeautifulSoup(html_text, 'html.parser')

                tag = soup.find(location['tag'], class_=location['class'])
                text = clean_text(tag.text)
                keywords = []
                for item in WORD_LIST:
                    for sub_item in item:
                        if re.search(clean_text(sub_item), text):
                            keywords.append(sub_item)
                            break
                
                if (keywords != []):
                    keywords = " ".join(keywords)

                df.loc[index, 'especificacao'] = keywords
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
        is_text = path_exist(text_path)
        
        product_text_path = text_path if is_text else page_path

        with open(product_text_path, 'r') as product_file:
            product = product_file.read()

            if (~is_text):
                product = clear_page(product)
                product = ' '.join(product.split())

            words = best_words(product)
            df.loc[index, 'especificacao_rota'] = words

            with open(text_path, 'w') as new_file:
                new_file.write(product)

    return df

def text_processing(texto):
    pass

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


def best_words(text):
    text = clean_text(text)

    words_count = {}
    for item in WORD_LIST:
        for sub_item in item:
            count = len(re.findall(clean_text(sub_item), text))
            if (count != 0):
                words_count[sub_item] = count

    if (words_count == {}):
        return None

    words_count = dict(sorted(words_count.items(), key=lambda item: item[1], reverse=True))
    limit = int(list(words_count.values())[0] * 0.30)
    words = ""
    limit_size = 5
    for item, value in words_count.items():
        if ((value >= limit) & (limit_size > 0)): 
            limit_size -= 1
            words += f" {item}"
        else: break

    return words

def count_occurrences_substring(text, word):
    count = text.count(word)
    return count

def keywords_column(df, column, type):
    new_word_list = [clean_text(word) for word in WORD_LIST]
    df['keywords_' + column + '_' + type] = df[column].apply(find_matches, args=(new_word_list,))
    
    return df

def find_matches(value):
    value = clean_text(value)
    keywords = [word for word in WORD_LIST if re.search(word, value)]

    return ', '.join(keywords) if keywords else None
