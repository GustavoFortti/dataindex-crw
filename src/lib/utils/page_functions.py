import importlib
from typing import List, Dict, Any
from src.lib.utils.file_system import list_directory


def get_pages_with_status_true(conf: Dict[str, Any], return_job_name: bool = True) -> List[str]:
    """
    Retrieves a list of pages with a `STATUS` value of True, either returning the job name or brand.

    Args:
        conf (Dict[str, Any]): Configuration dictionary containing the `pages_path` and `country` keys.
        return_job_name (bool, optional): If True, returns the job name. If False, returns the brand. Defaults to True.

    Returns:
        List[str]: A sorted list of job names or brands for pages with `STATUS` set to True.
    """
    pages: List[str] = list_directory(conf["pages_path"])
    pages_data_path: List[str] = []

    for page in pages:
        module_name: str = f"src.jobs.slave_page.pages.{conf['country']}.{page}.conf"

        try:
            page_conf = importlib.import_module(module_name)
            if getattr(page_conf, "STATUS", False):
                value = getattr(page_conf, "JOB_NAME", None) if return_job_name else getattr(page_conf, "BRAND", None)
                if value:
                    pages_data_path.append(value)
        except ModuleNotFoundError as e:
            # Log or handle the error if necessary
            print(f"Module {module_name} not found: {e}")
        except AttributeError as e:
            # Log or handle the error if necessary
            print(f"Error accessing attributes in module {module_name}: {e}")

    return sorted(pages_data_path)
