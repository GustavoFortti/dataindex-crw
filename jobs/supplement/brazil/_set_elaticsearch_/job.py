import importlib
import time

from config.env import LOCAL
from lib.elasticsearch.elasticsearch_functions import (
    check_elasticsearch_health, create_connection, create_index_if_not_exits,
    list_all_indices, prepare_synonyms)
from lib.elasticsearch.elasticsearch_index import ALL_INDEXS
from utils.general_functions import create_directory_if_not_exists
from utils.log import message

CONF = {
    "name": "_set_elaticsearch_",
    "data_path": f"{LOCAL}/data/supplement/brazil/_set_elaticsearch_",
}

def run(args):
    print("JOB_NAME: " + CONF["name"], end="")
    CONF.update(vars(args))

    job_type = CONF["job_type"]
    print(" - job_type: " + job_type)
    
    data_path = CONF["data_path"]
    create_directory_if_not_exists(data_path)
    
    es = create_connection()
    
    message("check_elasticsearch_health")
    check_elasticsearch_health(es)
    
    message("list_all_indices")
    list_all_indices(es)
    
    message("prepare_indices")
    prepare_indices(es)
    
def prepare_indices(es):
    module_name = f"jobs.supplement.brazil._set_page_.job"
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