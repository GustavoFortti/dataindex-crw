import pandas as pd
from utils.general_functions import create_file_if_not_exists

def tags_work(df, columns, new_row):
    tags_path = "./data/tags.csv"
    head = ",".join(map(str, columns))
    create_file_if_not_exists(tags_path, head)
    
    df_tags = pd.read_csv(tags_path)
    df_tags.loc[len(df)] = new_row
    df_tags.to_csv(tags_path, index=False)
    
    exit(0)