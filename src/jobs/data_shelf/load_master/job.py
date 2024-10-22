import os

from src.lib.utils.dataframe import read_and_stack_csvs_dataframes
from src.lib.utils.general_functions import get_pages_with_status_true
from src.lib.utils.file_system import create_directory_if_not_exists
from src.lib.utils.log import message
from src.lib.load.load_master import load

def set_conf(args, local):
    conf = {}
    conf["local"] = local
    conf["job_name"] = args.job_name
    conf["page_name"] = args.page_name
    conf["page_type"] = args.page_type
    conf["country"] = args.country
    conf["src_data_path"] = f"{local}/data/{conf['page_type']}/{conf['country']}"
    conf["data_path"] = f"{conf['src_data_path']}/load_master"
    conf["pages_path"] = f"{local}/src/jobs/slave_page/pages/{conf['country']}"
    
    conf["path_products_load_csl"] = os.path.join(conf['data_path'], "products_load_csl.csv")
    conf["path_products_shopify_csl"] = os.path.join(conf['data_path'], "products_shopify_csl.csv")
    
    return conf

def run(args):
    global LOCAL
    
    LOCAL = os.getenv('LOCAL')
    conf = set_conf(args, LOCAL)

    print("JOB_NAME: " + conf["job_name"])
    conf.update(vars(args))
    src_data_path = conf["src_data_path"]
    data_path = conf['data_path']

    create_directory_if_not_exists(data_path)
    
    message("read data")
    pages_with_status_true = get_pages_with_status_true(conf)
    df_products_transform_csl = read_and_stack_csvs_dataframes(src_data_path, pages_with_status_true, "products_transform_csl.csv", dtype={'ref': str})
    df_products_transform_csl = df_products_transform_csl.drop_duplicates(subset='ref').reset_index(drop=True)
    df_products_transform_csl = df_products_transform_csl.sample(frac=1).reset_index(drop=True)
    
    conf["brand"] = list(set(df_products_transform_csl['brand'].values))
    load(conf, df_products_transform_csl)