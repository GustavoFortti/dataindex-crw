import os
import pandas as pd
from typing import List

def get_all_origins(data_path: str, file_name: str) -> pd.DataFrame:
    """Recursively traverse directory and its subdirectories to find and concatenate all files with the given name into a single DataFrame"""
    dataframes: List[pd.DataFrame] = []

    for root, _, files in os.walk(data_path):
        for file_found in files:
            if file_found == file_name:
                full_path = os.path.join(root, file_found)
                df = pd.read_csv(full_path)
                dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=True)
    return combined_df
