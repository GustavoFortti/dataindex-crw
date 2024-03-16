from utils.log import message

from shared.data_prep.score_prep import load_score_prep

from shared.data_prep.data_prep_functions import (
    filter_nulls,
    apply_generic_filters,
    create_quantity_column,
    remove_blacklisted_products
)

def data_prep(conf, df):
    global CONF
    global WORDLIST
    global DATA_PATH

    CONF = conf
    WORDLIST = CONF['wordlist']
    DATA_PATH = CONF['data_path']

    message("Filtro de nulos")
    df = filter_nulls(df, DATA_PATH)

    message("Aplicando filtros de nome|preço|marca")
    df = apply_generic_filters(df, CONF)

    message("Criando coluna quantidade")
    df = create_quantity_column(df)

    message("Removendo produtos da blacklist")
    df = remove_blacklisted_products(df)

    # df = df[df['ref'] == "fb3585d7"]
    message("Criando colunas de definição para produtos")
    df = create_product_definition_column(df, CONF)
    exit()

def create_product_definition_column(df, conf):
    message("criada colunas de definição do produto")
    df['product'] = None

    message("Load_models_prep")
    load_score_prep(df, conf)
    