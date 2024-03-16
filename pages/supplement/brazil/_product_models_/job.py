import numpy as np
import pandas as pd
import joblib

from config.env import LOCAL
from utils.log import message

from utils.general_functions import (
    get_all_dfs_in_dir,
    create_directory_if_not_exists,
    read_json,
    save_json,
    file_exists
)

from shared.data_enrichment.models import (
    prep_dataframe,
    generate_models
)

CONF = {
    "name": "_models_",
}

def run(args):
    global DATA_PATH

    print("JOB_NAME: " + CONF["name"])
    CONF.update(vars(args))
    DATA_PATH = (f'{LOCAL}/data/supplement/brazil')
    MODELS_PATH = (f'{LOCAL}/data/supplement/brazil/_models_')

    create_directory_if_not_exists(MODELS_PATH)
    
    df_x = get_all_dfs_in_dir(DATA_PATH, "model_x")
    df_y = get_all_dfs_in_dir(DATA_PATH, "model_y")

    df_x, df_y = prep_dataframe(df_x, df_y)

    generate_models(df_x, df_y, MODELS_PATH)