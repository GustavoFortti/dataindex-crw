from config.env import LOCAL

CONF = {
    "name": "_set_purge_",
    "data_path": f"{LOCAL}/data/supplement/brazil/_set_purge_",
    "src_data_path": f"{LOCAL}/data/supplement/brazil",
    "pages_path": f"{LOCAL}/jobs/supplement/brazil/pages",
}

def run(args):
    print("JOB_NAME: " + CONF["name"], end="")
    CONF.update(vars(args))

    job_type = CONF["job_type"]
    print(" - EXEC: " + job_type)