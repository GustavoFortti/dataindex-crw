import os
import pandas as pd
from elasticsearch import helpers
from shared.elastic_funcions import create_connection, create_documents_with_pandas

CONF = {
    "name": "_set_",
}

def filter_title(df, keyword):
    filtered_df = df[df['titulo'].str.contains(keyword, case=False)]
    return filtered_df

def exclude_in_title(df, keyword):
    filtered_df = df[~df['titulo'].str.contains(keyword, case=False)]
    return filtered_df

def gen_destaques(wordlist, df):
    df_index = None
    for words in wordlist:
        for keyword in words['keywords']:
            if (words['type'] == 'filter'):
                df_aux = filter_title(df, keyword)
                if df_index is None:
                    df_index = df_aux
                else:
                    df_index = pd.concat([df_index, df_aux], ignore_index=True)
            else:
                df_index = exclude_in_title(df_index, keyword)
    
    return df_index

def create_index(es, indice_elasticsearch):
    if not es.indices.exists(index=indice_elasticsearch):
        es.indices.create(index=indice_elasticsearch)
        print(f"Índice '{indice_elasticsearch}' criado.")
    else:
        print(f"Índice '{indice_elasticsearch}' já existe.")

def get_all_origins():
    diretorio_inicial = './data'
    nome_arquivo = 'origin_csl.csv'

    dataframes = []

    # Percorre recursivamente o diretório e seus subdiretórios
    for pasta_raiz, _, arquivos in os.walk(diretorio_inicial):
        for nome_arquivo_encontrado in arquivos:
            if nome_arquivo_encontrado == nome_arquivo:
                caminho_completo = os.path.join(pasta_raiz, nome_arquivo_encontrado)
                df = pd.read_csv(caminho_completo)
                dataframes.append(df)

    # Una todos os DataFrames em um único DataFrame
    df = pd.concat(dataframes, ignore_index=True)
    return df

def run(args):
    print("JOB_NAME: " + CONF["name"], end="")
    CONF["option"] = args.option

    job_type = args.job_type
    print(" - EXEC: " + job_type)

    es = create_connection()
    
    df = get_all_origins()
    
    print("brazil_supplement_whey")
    sabores = ["banana cream", "baunilha", "beijinho", "beijinho de coco", "brigadeiro","brownie chocolate","cafe","cappuccino","caramelo crocante","cheesecake chocolate","cheesecake de maracuja","cheesecake de morango","chocolate","chocolate crocante","churros","cocco cioccolato","cocco e cioccolato","cookies","cookies cream","cookies e cream","doce de leite","dulce de leche premium","duo bianco al latte","leite cacau avela","leite de coco","limão","maracuja mousse","milho verde","morango","morango com chantilly","napolitano","pao de mel","peanut butter","strawberry milk shake","strawberry milkshake","torta al limone","torta cioccolato bianco","torta de banana","torta de limão","vanilla cream","vitamina de frutas"]
    blacklist = ["barrinha", "barra", 'break', 'bar', 'wafer', 'kit', 'combo']
    keywords = ['whey']
    wordlist = [{"keywords": sabores, "type": "filter"}, {"keywords": blacklist, "type": "exclude"}]

    df_index = gen_destaques(wordlist, df)
    df_index = filter_title(df_index, keywords[0])
    df_index = df_index.sample(10)

    indice_elasticsearch = 'brazil_supplement_whey'
    create_index(es, indice_elasticsearch)
    es.delete_by_query(index=indice_elasticsearch, body={"query": {"match_all": {}}})
    helpers.bulk(es, create_documents_with_pandas(df_index, indice_elasticsearch))
    
    
    print("brazil_supplement_bar")
    sabores = ["avela", "banoffee", "beijinho", "beijinho de coco", "berries crispies", "bombom de coco", "brigadeiro", "brownie chocolate", "brownie crispies", "cafe", "cafe doce de leite", "caramelo amendoim", "caramelo crocante", "cheesecake de maracuja", "cheesecake de morango", "chocolate", "churros", "cookie", "cookies cream", "crisp gourmet", "doce de leite", "dulce de leche e limao siciliano", "dulce de leche havanna", "duo bianco al latte", "floresta negra", "leite cacau avelã", "leite condensado", "morango com chantilly", "morango perfetto", "mousse de maracujá", "pacoca", "pacoca chocolate", "pao de mel", "peanut butter", "penaut caramel", "protein crisp", "torta al limone", "torta cioccolato bianco", "torta de banana", "torta de limao", "trufa de avelã", "trufa de chocolate", "trufa de morango"]
    blacklist = ['wafer', 'kit', 'combo']
    keywords = ['bar']
    wordlist = [{"keywords": sabores, "type": "filter"}, {"keywords": blacklist, "type": "exclude"}]

    df_index = gen_destaques(wordlist, df)
    df_index = filter_title(df_index, keywords[0])
    df_index = df_index.sample(10)

    indice_elasticsearch = 'brazil_supplement_bar'
    create_index(es, indice_elasticsearch)
    es.delete_by_query(index=indice_elasticsearch, body={"query": {"match_all": {}}})
    helpers.bulk(es, create_documents_with_pandas(df_index, indice_elasticsearch))

    print("brazil_supplement_preworkout")
    keywords = ['pretreino', 'pre treino', 'preworkout', 'pre workout', 'workout']
    blacklist = ['whey', 'creatina']
    wordlist = [{"keywords": keywords, "type": "filter"},{"keywords": blacklist, "type": "exclude"}]

    df_index = gen_destaques(wordlist, df)
    df_index = filter_title(df_index, keywords[0])
    print(df_index)
    df_index = df_index.sample(10)

    indice_elasticsearch = 'brazil_supplement_preworkout'
    create_index(es, indice_elasticsearch)
    es.delete_by_query(index=indice_elasticsearch, body={"query": {"match_all": {}}})
    helpers.bulk(es, create_documents_with_pandas(df_index, indice_elasticsearch))