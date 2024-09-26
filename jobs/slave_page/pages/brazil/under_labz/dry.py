import pandas as pd
from lib.data_prep.data_manager import data_prep

def create_origin_dry():
    file_path = CONF['data_path']

    df = pd.read_csv(file_path + "/origin.csv")
    df = data_prep(CONF, df)
    
    df.to_csv(file_path + "/origin_dry.csv", index=False)
    print("Success in saving origin_dry")

def dry(conf):
    global CONF
    CONF = conf

    print("Data Dry")
    create_origin_dry()

