import os

import pandas as pd
from datetime import date

from shared.selenium_service import get_html
from shared.data_quality import status_tag
from utils.wordlist import BLACK_LIST
from utils.general_functions import (DATE_FORMAT,
                                 read_json, 
                                 generate_hash, 
                                 delete_file, 
                                 create_directory_if_not_exists, 
                                 check_if_is_old_file,
                                 create_file_if_not_exists,
                                 find_in_text_with_word_list,
                                 format_column_date,
                                 clean_string_break_line,
                                 download_image,
                                 path_exist)

def map_seed_new(driver, map_seed_conf, is_origin=False, update_fields=[]):
    pass

def map_seed(driver, map_seed_conf, is_origin=False, update_fields=[]):
    data_path = map_seed_conf['data_path']
    get_next_url = map_seed_conf["get_next_url"]
    get_last_page_index = map_seed_conf["get_last_page_index"]
    get_items = map_seed_conf["get_items"]
    time_sleep_page = map_seed_conf["time_sleep_page"]
    scroll_page = map_seed_conf["scroll_page"]
    get_elements_seed = map_seed_conf["get_elements_seed"]
    option = map_seed_conf['option']

    seed_path = map_seed_conf['seed_path'] + "/seed.json"
    seeds = read_json(seed_path)

    tree_path = data_path + "/tree.csv"
    tree_temp_path = data_path + "/tree_temp.csv"
    delete_file(tree_temp_path)
    columns = ["ref", "title" ,"price" ,"image_url", "product_url", "ing_date"]
    df_tree = pd.DataFrame(columns=columns)

    images_tmp_path = data_path + "/img_tmp/"
    if (path_exist(images_tmp_path) & (option != 'status_job')):
        for img_tmp in os.listdir(images_tmp_path):
            delete_file(images_tmp_path + img_tmp)

    origin_path = f'{data_path}/origin.csv'
    if (path_exist(origin_path) & (update_fields != [])):
        df_tree = pd.read_csv(origin_path)
    
    for seed in seeds:
        url = get_next_url(seed['url'], 1)
        
        soup = get_html(driver, url, time_sleep_page, scroll_page, False, functions_to_check_load=[get_items, get_elements_seed])

        ref = ""
        last_page_num = get_last_page_index(soup)
        i = 1
        while (i <= last_page_num):
            i = i + 1
            
            url = get_next_url(seed['url'], i)
            items = get_items(soup)
            n_items = len(items)
            print(f"itens = {n_items}")
            
            for item in items:
                product_url, title, price, image_url = get_elements_seed(item)
                ref = generate_hash(product_url)
                create_directory_if_not_exists(data_path + "/img_tmp/")
                if (option != 'status_job'):
                    download_image(image_url, data_path + "/img_tmp/", ref)
                
                if (price): price = clean_string_break_line(price)
                if (title): title = clean_string_break_line(title)

                data_atual = date.today()
                formatted_date = data_atual.strftime(DATE_FORMAT)

                new_row = {"ref": ref, "title": title, "price": price, "image_url": image_url, "product_url": product_url, "ing_date": formatted_date}
                index = df_tree["ref"] == new_row['ref']
                print(new_row)
                
                if (option == 'status_job'):
                    status_tag(new_row)
                
                if ((update_fields) and (index.any())):
                    for field in update_fields:
                        df_tree.loc[index, field] = new_row[field]
                else:
                    df_tree.loc[len(df_tree)] = new_row

                df_tree.to_csv(tree_temp_path, index=False)

            if ((i > last_page_num) or (n_items == 0)): 
                break

            soup = get_html(driver, url, time_sleep_page, scroll_page, functions_to_check_load=[get_items, get_elements_seed])
    
    df_tree_temp = pd.read_csv(tree_temp_path)
    df_tree_temp = df_tree_temp.drop_duplicates(subset='product_url').reset_index(drop=True)
    df_tree_temp = format_column_date(df_tree_temp, 'ing_date')

    if (is_origin):
        df_tree = df_tree.dropna(subset=['price'])
        df_tree = df_tree[~df_tree['title'].apply(lambda x: find_in_text_with_word_list(x, BLACK_LIST))]
        df_tree.to_csv(origin_path, index=False)

    df_tree_temp.to_csv(tree_path, index=False)
    delete_file(tree_temp_path)

def map_tree(driver, map_tree_conf, update=False, filter_ref=False):
    data_path = map_tree_conf['data_path']
    get_elements_tree = map_tree_conf["get_elements_tree"]
    time_sleep_page = map_tree_conf["time_sleep_page"]
    scroll_page = map_tree_conf["scroll_page"]
    return_text = map_tree_conf["return_text"]

    # Carrega um DataFrame a partir de um arquivo CSV e remove duplicatas
    df_tree = pd.read_csv(f'{data_path}/tree.csv')

    # Filtra o DataFrame por um valor específico de 'ref', se fornecido
    if (filter_ref):
        print(filter_ref)
        filtered_df = df_tree[df_tree['ref'] == filter_ref]
        if not filtered_df.empty:
            index_value = filtered_df.index[0]
            df_tree = df_tree[df_tree.index >= index_value]

    # Cria um diretório para salvar arquivos de texto, se não existir
    textfiles_path = f"{data_path}/products"
    create_directory_if_not_exists(textfiles_path)

    # Define os caminhos para os arquivos CSV de origem e temporário
    origin_temp_path = data_path + "/origin_temp.csv"
    delete_file(origin_temp_path)

    # Define as colunas para o DataFrame e cria um arquivo CSV, se não existir
    columns = ["ref", "title" ,"price" ,"image_url", "product_url", "ing_date"]
    head = ",".join(map(str, columns))
    create_file_if_not_exists(origin_temp_path, head)

    # Carrega e filtra o DataFrame df_origin por data
    df_tree = df_tree[~df_tree['title'].apply(lambda x: find_in_text_with_word_list(x, BLACK_LIST))]
    df_origin_temp = pd.read_csv(origin_temp_path)
    df_tree = df_tree.dropna(subset=['price'])
    
    if (df_tree.empty):
        print("df_tree is empty")
        return
    
    # Processamento principal: itera sobre df_tree para extrair e processar dados
    for index, row in df_tree.iterrows():
        # Extrai dados da linha atual
        ref = row['ref']
        url = row['product_url']
        price = row['price']
        title = row['title']
        image_url = row['image_url']

        print(f"{index} - {ref} - {url}")

        # Verifica se o arquivo de texto já existe e é antigo
        textfile_path = f"{textfiles_path}/{ref}.txt"
        is_old_file = check_if_is_old_file(textfile_path)

        # Processo de requisição e extração de dados da página
        if ((not update) & (is_old_file)):
            soup, text = get_html(driver, url, time_sleep_page, scroll_page, return_text)
            with open(textfile_path, 'w') as file:
                file.write(text)
                print(f"File '{textfile_path}' created successfully.")

            is_old_file = False
        else:
            soup = get_html(driver, url, 1, False, False)
        
        # Extrai novo título e formata a data
        new_title, new_price, new_image_url = get_elements_tree(soup)

        data_atual = date.today()
        formatted_date = data_atual.strftime(DATE_FORMAT)

        if (new_image_url): 
            image_url = new_image_url
            download_image(ref, data_path + "/img_tmp/", new_image_url)
        if (new_price): price = clean_string_break_line(new_price)
        if (new_title): 
            new_title = clean_string_break_line(new_title)
            if (len(new_title) > len(title)):
                title = new_title

        # Cria um novo registro e adiciona ao DataFrame de origem
        new_row = {"ref": ref, "title": title, "price": price, "image_url": image_url, "product_url": url, "ing_date": formatted_date}
        print(new_row)
        df_origin_temp.loc[len(df_origin_temp)] = new_row
        
        # Salva temporariamente o DataFrame df_origin
        df_origin_temp = format_column_date(df_origin_temp, 'ing_date')
        df_origin_temp.to_csv(origin_temp_path, index=False)

    # Carrega o DataFrame temporário e o salva no arquivo CSV final
    origin_path = data_path + "/origin.csv"
    delete_file(origin_path)
    df_origin_temp = pd.read_csv(origin_temp_path)
    df_origin_temp = format_column_date(df_origin_temp, 'ing_date')
    df_origin_temp.to_csv(origin_path, index=False)
    delete_file(origin_temp_path)