from src.jobs.job_manager import JobBase
import pandas as pd
from src.lib.utils.log import message
from src.lib.utils.file_system import file_or_path_exists, read_file

def create_product_cols_by_class(job_base: JobBase, df: pd.DataFrame) -> pd.DataFrame:
    """
    Main function to create product description columns.

    Args:
        job_base (JobBase): The job base object containing configurations.
        df (pd.DataFrame): The DataFrame containing product data.

    Returns:
        pd.DataFrame: The DataFrame with new product columns added.
    """
    message("Creating product description columns")
    data = []
    for row in df.itertuples(index=False):
        ref: str = row.ref
        title: str = row.title

        message(f'ref - {ref} | {title} | create_product_cols ')
        
        product_class_path: str = f"{job_base.products_path}/{ref}_class.txt"
        product_class: str = read_file(product_class_path)
        
        aux_class = str(product_class.split(",")) if product_class else None
        data.append(aux_class)
        
    df['collections'] = data
    return df
        
        