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

    # df = df[df['ref'].isin(["4e35200b"])]
    # ac875a98                                     barrinha, whey nutrata
    # e4f29a35                             whey, barrinha, cafein nutrata
    # aedc32cf                                    whey, chocolate dux
    # b61198db                                                kit under
    # e4ae1ec1                               whey, protein, wafer ath
    # eb12db3f                                         iso, wafer ath
    # f4938c96                                          chocolate ath
    # f4a37fb3                                        wafer, whey ath
    # f41a237e                                    mass, chocolate ghr
    # f8773015                             barrinha, protein, veg ghr
    # f9fda4d5                                  cafein, chocolate ghr
    # f9c3f957                                     coco, barrinha bold
    message("Criando colunas de definição para produtos")
    df = create_product_definition_column(df, CONF)
    exit()

def create_product_definition_column(df, conf):
    message("criada colunas de definição do produto")
    df['product'] = None

    message("Load_models_prep")
    load_score_prep(df, conf)
    