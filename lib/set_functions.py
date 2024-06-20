import importlib

from utils.general_functions import list_directory


def get_pages_with_status_true(conf, return_job_name=True):
    pages = list_directory(conf["pages_path"])
    page_type = conf["page_type"]
    country = conf["country"]

    pages_data_path = []
    for page in pages:
        module_name = f"jobs.{page_type}.{country}.pages.{page}.conf"
        page_conf = importlib.import_module(module_name)
        if page_conf.STATUS:
            value = page_conf.JOB_NAME if return_job_name else page_conf.BRAND
            pages_data_path.append(value)
            
    return sorted(pages_data_path)