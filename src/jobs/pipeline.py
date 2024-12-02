import importlib
import os
from datetime import datetime
from typing import List

from src.lib.utils.file_system import (create_directory_if_not_exists,
                                       file_or_path_exists)
from src.lib.utils.log import message


class JobBase:
    """Class that provides a base structure (skeleton) for a job."""

    def __init__(self, args: object) -> None:
        
        # job config
        self.name: str = args.job_name
        self.options: str = args.options
        self.page_name: str = args.page_name
        self.country: str = args.country
        self.local: str = args.local
        self.date_format: str = "%Y-%m-%d"
        self.date_ref = datetime.today().strftime(self.date_format)
        
        self.crawler_use_headless: bool = False
        self.update_all_products: bool = False
        self.update_all_products_metadata: bool = False

        # main paths
        self.src_data_path: str = f"{self.local}/data"
        self.data_path: str = f"{self.src_data_path}/{self.name}"
        self.modules_path: str = f"{self.local}/src/modules/"

        # create initial directories 
        create_directory_if_not_exists(f"{self.data_path}/products")
        create_directory_if_not_exists(f"{self.data_path}/history_price")

        # data paths
        ## history paths
        self.path_history_price: str = f"{self.data_path}/history_price"
        self.path_history_price_file: str = os.path.join(f"{self.data_path}/history_price", f"products_history_price_{self.date_ref}.csv")
        
        ## extract paths
        self.path_extract_csl: str = os.path.join(self.data_path, "extract_csl.csv")
        self.path_extract_temp: str = os.path.join(self.data_path, "extract_temp.csv")
        self.df_columns: List[str] = ["ref", "title", "price", "image_url", "product_url", "ing_date"]
        
        
        ## transform paths
        self.path_transform_csl: str = os.path.join(self.data_path, "transform_csl.csv")
        self.path_metadata_transform: str = os.path.join(self.data_path, "metadata_transform.csv")
        
        ## load paths
        self.path_load_csl: str = os.path.join(self.data_path, "load_csl.csv")
        self.path_memory_shopify: str = os.path.join(self.data_path, "memory_shopify.csv")
        self.path_shopify_csl: str = os.path.join(self.data_path, "shopify_csl.csv")

        if not file_or_path_exists(self.path_extract_csl) and self.options != "verify_page_elements":
            self.options = "create_new_page"
        
        # initialization variables
        self.page: object = None
    
    def set_page(self, page: classmethod) -> None:
        self.page = page
        

def pipeline(args):
    message("pipeline start")
    job_base = JobBase(args)
    
    job_script = importlib.import_module(f"src.jobs.{job_base.name}")
    job_script.run(job_base)
    
    message("pipeline end")