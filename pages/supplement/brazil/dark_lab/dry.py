import pandas as pd
from shared.data_enrichment import process_data

def create_origin_dry():
    file_path = CONF['data_path']

    df = pd.read_csv(file_path + "/origin.csv")
    df = process_data(CONF, df)
    
    df.to_csv(file_path + "/origin_dry.csv", index=False)
    print("Success in saving origin_dry")

def dry(conf):
    global CONF
    CONF = conf

    print("Data Dry")
    create_origin_dry()

