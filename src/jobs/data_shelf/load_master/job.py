import os
from datetime import datetime

import pandas as pd
from src.lib.utils.dataframe import (drop_duplicates_for_columns,
                                     read_and_stack_csvs_dataframes,
                                     read_and_stack_historical_csvs_dataframes)
from src.lib.utils.general_functions import get_pages_with_status_true
from src.lib.utils.file_system import DATE_FORMAT, create_directory_if_not_exists
from src.lib.utils.log import message
from src.lib.wordlist.wordlist import WORDLIST

def set_conf(args, local):
    conf = {}
    conf["local"] = local
    conf["job_name"] = args.job_name
    conf["page_name"] = args.page_name
    conf["page_type"] = args.page_type
    conf["country"] = args.country
    conf["src_data_path"] = f"{local}/data/{conf['page_type']}/{conf['country']}"
    conf["data_path"] = f"{conf['src_data_path']}/history_price"
    conf["pages_path"] = f"{local}/src/jobs/slave_page/pages/{conf['country']}"
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