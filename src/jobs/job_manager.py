import importlib
import os
from datetime import datetime
from typing import List, Optional

from selenium.webdriver.remote.webdriver import WebDriver
from src.lib.utils.file_system import (create_directory_if_not_exists,
                                       file_or_path_exists)
from src.lib.utils.log import message
from src.pages.page import Page

class JobBase:
    """Class that provides a base structure (skeleton) for a job."""

    def __init__(self, args: object) -> None:
        
        # job config
        self.name: str = args.job_name
        self.options: str = args.options
        self.country: str = args.country
        self.local: str = args.local
        self.mode: str = args.mode
        self.date_format: str = "%Y-%m-%d"
        self.date_today = datetime.today().strftime(self.date_format)

        # main paths
        self.src_data_path: str = f"{self.local}/data"
        self.data_path: str = f"{self.src_data_path}/{self.name}"
        self.pages_path: str = f"{self.local}/src/pages"
        
        self.file_name_extract_csl: str = f"extract_csl.csv" 
        self.file_name_extract_temp: str = f"extract_temp.csv" 
        self.file_name_transform_csl: str = f"transform_csl.csv" 
        self.file_name_metadata_transform: str = f"metadata_transform.csv"
        self.file_name_load_csl: str = "load_csl.csv"
        self.file_name_memory_shopify: str = "memory_shopify.csv"
        self.file_name_shopify_csl: str = "shopify_csl.csv"
        
        self.page: Optional[Page] = None
        self.pages: List[Page] = []
        
        if self.name in ["data_extract", "data_transform"]:
            self.extract_and_transform_configurations(args)
        elif self.name in ["data_load"]:
            self.load_configurations()
        
    def extract_and_transform_configurations(self, args) -> None:
        # job config
        self.page_name: str = args.page_name
        
        # crawler configs
        self.driver: Optional[WebDriver] = None
        self.driver_use_headless: bool = False
        
        self.data_path = f"{self.src_data_path}/{self.page_name}"
        self.products_path: str = f"{self.data_path}/products"
        self.history_price_path: str = f"{self.data_path}/history_price"

        # create initial directories 
        create_directory_if_not_exists(f"{self.data_path}/products")
        create_directory_if_not_exists(f"{self.data_path}/history_price")

        # data paths
        ## history paths
        self.path_history_price: str = f"{self.data_path}/history_price"
        self.file_path_history_price: str = os.path.join(f"{self.data_path}/history_price", f"products_history_price_{self.date_today}.csv")
        
        ## extract config
        self.path_extract_csl: str = os.path.join(self.data_path, self.file_name_extract_csl)
        self.path_extract_temp: str = os.path.join(self.data_path, self.file_name_extract_temp)
        self.extract_dataframe_columns: List[str] = ["ref", "title", "price", "image_url", "product_url", "ing_date"]
        self.control_update_all_products: str = os.path.join(self.data_path, "_control_update_all_products_")
        self.control_update_all_products_metadata: str = os.path.join(self.data_path, "_control_update_all_products_metadata_")
        self.control_control_update_old_products_metadata: str = os.path.join(self.data_path, "_control_control_update_old_products_metadata_")
        self.checkpoint_extract_data: bool = self.mode == "prd"
        self.check_if_job_is_ready: bool = self.options == "check_if_job_is_ready"
        self.update_all_products: bool = self.options == "update_all_products"
        self.update_all_products_metadata: bool = self.options == "update_all_products_metadata"
        
        ## transform paths
        self.path_transform_csl: str = os.path.join(self.data_path, self.file_name_transform_csl)
        self.path_metadata_transform: str = os.path.join(self.data_path, self.file_name_metadata_transform)
        
        if not file_or_path_exists(self.path_extract_csl) and self.options != "check_if_job_is_ready":
            self.options = "create_new_page"
            
    def load_configurations(self) -> None:
        self.path_load_csl: str = os.path.join(self.data_path, self.file_name_load_csl)
        self.path_memory_shopify: str = os.path.join(self.data_path, self.file_name_memory_shopify)
        self.path_shopify_csl: str = os.path.join(self.data_path, self.file_name_shopify_csl)
        
    def set_page(self, page: Page) -> None:
        self.page = page
    
    def append_pages(self, page: Page) -> None:
        self.pages.append(page)

def job_manager(args):
    message("job_manager start")
    job_base = JobBase(args)
    
    job_script = importlib.import_module(f"src.jobs.{job_base.name}")
    job_script.run(job_base)
    
    message("job_manager end")