import importlib
from typing import List, Dict, Any
from src.lib.utils.file_system import list_directory
from src.jobs.job_manager import JobBase


def get_pages_with_status_true(job_base: JobBase) -> List[str]:
    """
    Retrieves the names of pages with status set to True.
    
    Args:
        job_base (JobBase): An object containing job configurations and paths.

    Returns:
        List[str]: A list of page names with status set to True.
    """

    pages_with_status_true = []
    for page in job_base.pages:
        if page.page_production_status:
            pages_with_status_true.append(page.name)

    return sorted(pages_with_status_true)
