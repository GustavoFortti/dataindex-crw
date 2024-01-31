from shared.data_enrichment import process_data

def create_origin_dry():
    file_path = CONF['data_path']
    locations = CONF['location_type_product']
    df = process_data(CONF, locations)
    
    df.to_csv(file_path + "/origin_dry.csv", index=False)
    print("Success in saving origin_csl")

def dry(conf):
    global CONF
    CONF = conf

    option = CONF["option"]

    if (option == "default"):
        print("DRY: default")
        create_origin_dry()
