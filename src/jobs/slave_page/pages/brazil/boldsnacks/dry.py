import pandas as pd
from src.lib.transform.transform import transform
from src.lib.utils.dataframe import read_df

def create_products_transform_csl():
    df = read_df(CONF['path_products_extract_csl'], dtype={'ref': str})

    def_string = "barrinha "
    df['title'] = def_string + df['title']

    df = transform(CONF, df)

    df['name'] = df['name'].str.slice(len(def_string))
    df['title_extract'] = df['title_extract'].str.slice(len(def_string))

    df.to_csv(CONF['path_products_transform_csl'], index=False)
    print("Success in saving products_transform_csl")

def dry(conf):
    global CONF
    CONF = conf

    print("Data Dry")
    create_products_transform_csl()