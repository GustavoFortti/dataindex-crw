import importlib
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List

from config.env import LOCAL
from lib.elasticsearch.elasticsearch_functions import (
    check_elasticsearch_health, create_connection, create_index_if_not_exits,
    delete_indices, list_all_indices, prepare_synonyms)
from lib.elasticsearch.elasticsearch_index import ALL_INDEXS
from utils.general_functions import create_directory_if_not_exists
from utils.log import message

CONF = {
    "name": "_set_elaticsearch_",
    "data_path": f"{LOCAL}/data/supplement/brazil/_set_elaticsearch_",
}

def run(args: Any) -> None:
    print(f"JOB_NAME: {CONF['name']}", end="")
    CONF.update(vars(args))

    job_type = CONF["job_type"]
    print(f" - job_type: {job_type}")
    
    data_path = CONF["data_path"]
    create_directory_if_not_exists(data_path)
    
    es = create_connection()
    
    message("check_elasticsearch_health")
    check_elasticsearch_health(es)
    
    message("list_all_indices")
    indices = list_all_indices(es)
    
    message("prepare_indices")
    prepare_indices(es)
    
    filtered_indices = filter_recent_indices(indices, 140)
    delete_indices(es, filtered_indices)

def prepare_indices(es: Any) -> None:
    """
    Prepares indices by attempting to create them if they do not already exist.
    """
    module_name = "jobs.supplement.brazil._set_page_.job"
    module = importlib.import_module(module_name)
    conf_set_page_ = module.CONF
    synonyms = prepare_synonyms(conf_set_page_)
    
    for indices in ALL_INDEXS:
        for key, index_name in indices['index'].items():
            attempts = 0
            max_attempts = 4
            while attempts < max_attempts:
                try:
                    message(f"Attempting to create {key}")
                    message(index_name)
                    create_index_if_not_exits(es, index_name, indices['type'], synonyms)
                    break
                except Exception as e:
                    attempts += 1
                    message(f"WAITING - Failed to create {key}, attempt {attempts}. Error: {str(e)}")
                    if attempts < max_attempts:
                        time_sleep = 10 * (attempts + 2)
                        message(f"WAITING - {time_sleep} seconds before retrying...")
                        time.sleep(time_sleep)
                    else:
                        message("ERROR - Maximum retry attempts reached, moving to next index.")
                        exit(1)

def filter_recent_indices(indices: List[Dict[str, str]], days_threshold: int = 7) -> List[Dict[str, str]]:
    """
    Filters indices by date, returning only those more recent than the threshold.
    """
    current_date = datetime.now()
    filtered_indices = []
    
    for index in indices:
        date_str = index.get('date')
        try:
            index_date = datetime.strptime(date_str, '%d%m%Y')
            if (index_date < current_date - timedelta(days=days_threshold)):
                filtered_indices.append(index["name"])
        except ValueError:
            message(f"Invalid date format for index: {index}. Skipping this entry.")
    
    return filtered_indices
