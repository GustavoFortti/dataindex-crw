import pandas as pd
from typing import List, Optional

def filter_dataframe_for_columns(df: pd.DataFrame, columns: List[str], keywords: List[str], blacklist: Optional[List[str]] = None) -> pd.DataFrame:
    """Filters a DataFrame for specified columns based on keywords and an optional blacklist to exclude certain terms"""
    global_mask = pd.Series([False] * len(df), index=df.index)
    
    for col in columns:
        df[col] = df[col].astype(str).fillna('')
        global_mask |= df[col].str.contains('|'.join(keywords), case=False)
    
    filtered_df = df[global_mask]
    
    if blacklist:
        for col in columns:
            blacklist_mask = ~filtered_df[col].str.contains('|'.join(blacklist), case=False)
            filtered_df = filtered_df[blacklist_mask]
    
    filtered_df = filtered_df.drop_duplicates().reset_index(drop=True)
    
    return filtered_df
