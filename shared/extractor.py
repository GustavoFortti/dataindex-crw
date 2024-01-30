import pandas as pd
from datetime import date

from shared.selenium_service import get_html
from shared.data_quality import tags_work
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

def map_seed(driver, map_seed_conf, is_origin=False, update_fields=[]):
    data_path = map_seed_conf['data_path']
    get_next_url = map_seed_conf["get_next_url"]
    get_last_page_index = map_seed_conf["get_last_page_index"]
    get_items = map_seed_conf["get_items"]
    time = map_seed_conf["time"]
    scroll_page = map_seed_conf["scroll_page"]
    get_elements_seed = map_seed_conf["get_elements_seed"]
    option = map_seed_conf['option']

    seed_path = map_seed_conf['seed_path'] + "/seed.json"
    seeds = read_json(seed_path)

    tree_path = data_path + "/tree.csv"
    tree_temp_path = data_path + "/tree_temp.csv"
    columns = ["ref", "titulo" ,"preco" ,"link_imagem", "link_produto", "ing_date"]
    df_tree = pd.DataFrame(columns=columns)

    origin_path = f'{data_path}/origin.csv'
    if (path_exist(origin_path) & (update_fields != [])):
        df_tree = pd.read_csv(origin_path)
    
    for seed in seeds:
        url = get_next_url(seed['url'], 1)
        
        soup = get_html(driver, url, time, scroll_page)
        max_itens_by_page = 0
        ref = ""
        last_page_by_ref = ""
        last_page_num = get_last_page_index(soup)
        i = 1
        while (i <= last_page_num):
            i = i + 1
            
            url = get_next_url(seed['url'], i)
            items = get_items(soup)
            n_items = len(items)
            last_page_by_ref = ref
            print(f"itens = {n_items}")
            
            for item in items:
                product_link, title, price, link_imagem = get_elements_seed(item)
                ref = generate_hash(product_link)
                create_directory_if_not_exists(data_path + "/img_temp/")
                download_image(link_imagem, data_path + "/img_temp/", ref)
                
                if (price): price = clean_string_break_line(price)
                if (title): title = clean_string_break_line(title)

                data_atual = date.today()
                data_formatada = data_atual.strftime(DATE_FORMAT)

                new_row = {"ref": ref, "titulo": title, "preco": price, "link_imagem": link_imagem, "link_produto": product_link, "ing_date": data_formatada}
                index = df_tree["ref"] == new_row['ref']
                print(new_row)
                
                if (option == 'test_tag'):
                    tags_work(df_tree, columns, new_row)
                
                if ((update_fields) and (index.any())):
                    for field in update_fields:
                        df_tree.loc[index, field] = new_row[field]
                else:
                    df_tree.loc[len(df_tree)] = new_row

                df_tree.to_csv(tree_temp_path, index=False)

            if ((i > last_page_num) or (n_items == 0) or (last_page_by_ref == ref)): 
                break
            if (n_items >= max_itens_by_page):
                max_itens_by_page = n_items
            else:
                break

            soup = get_html(driver, url, time, scroll_page)
    
    df_tree_temp = pd.read_csv(tree_temp_path)
    df_tree_temp = df_tree_temp.drop_duplicates(subset='link_produto').reset_index(drop=True)
    df_tree_temp = format_column_date(df_tree_temp, 'ing_date')

    if (is_origin):
        df_tree = df_tree.dropna(subset=['preco'])
        df_tree = df_tree[~df_tree['titulo'].apply(lambda x: find_in_text_with_word_list(x, BLACK_LIST))]
        df_tree.to_csv(origin_path, index=False)

    df_tree_temp.to_csv(tree_path, index=False)
    delete_file(tree_temp_path)

def map_tree(driver, map_tree_conf, update=False, filter_ref=False):
    data_path = map_tree_conf['data_path']
    get_elements_tree = map_tree_conf["get_elements_tree"]
    time = map_tree_conf["time"]
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

    # Define as colunas para o DataFrame e cria um arquivo CSV, se não existir
    columns = ["ref", "titulo" ,"preco" ,"link_imagem", "link_produto", "ing_date"]
    head = ",".join(map(str, columns))
    create_file_if_not_exists(origin_temp_path, head)

    # Carrega e filtra o DataFrame df_origin por data
    df_tree = df_tree[~df_tree['titulo'].apply(lambda x: find_in_text_with_word_list(x, BLACK_LIST))]
    df_origin_temp = pd.read_csv(origin_temp_path)
    df_tree = df_tree.dropna(subset=['preco'])
    
    if (df_tree.empty):
        print("df_tree is empty")
        return
    
    # Processamento principal: itera sobre df_tree para extrair e processar dados
    for index, row in df_tree.iterrows():
        # Extrai dados da linha atual
        ref = row['ref']
        url = row['link_produto']
        price = row['preco']
        title = row['titulo']
        link_imagem = row['link_imagem']

        print(f"{index} - {ref} - {url}")

        # Verifica se o arquivo de texto já existe e é antigo
        textfile_path = f"{textfiles_path}/{ref}.txt"
        is_old_file = check_if_is_old_file(textfile_path)

        # Processo de requisição e extração de dados da página
        if ((not update) & (is_old_file)):
            soup, text = get_html(driver, url, time, scroll_page, return_text)
            with open(textfile_path, 'w') as file:
                file.write(text)
                print(f"File '{textfile_path}' created successfully.")

            is_old_file = False
        else:
            soup = get_html(driver, url, 1, False, False)
        
        # Extrai novo título e formata a data
        new_title, new_price, new_link_imagem = get_elements_tree(soup)

        data_atual = date.today()
        data_formatada = data_atual.strftime(DATE_FORMAT)

        if (new_link_imagem): 
            link_imagem = new_link_imagem
            download_image(ref, data_path + "/img_temp/", new_link_imagem)
        if (new_price): price = clean_string_break_line(new_price)
        if (new_title): 
            new_title = clean_string_break_line(new_title)
            if (len(new_title) > len(title)):
                title = new_title

        # Cria um novo registro e adiciona ao DataFrame de origem
        new_row = {"ref": ref, "titulo": title, "preco": price, "link_imagem": link_imagem, "link_produto": url, "ing_date": data_formatada}
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