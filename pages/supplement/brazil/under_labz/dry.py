from shared.enrich_data import init

def create_origin_csl():
    file_path = CONF['data_path']
    locations = CONF['location_type_product']
    df = init(CONF, locations)
    
    df.to_csv(file_path + "/origin_csl.csv", index=False)
    print("Success in saving origin_csl")

def dry(conf):
    global CONF
    CONF = conf

    option = CONF["option"]

    if (option == "default"):
        print("DRY: default")
        create_origin_csl()
