from shared.enrich_data import init

def dry_origin():
    file_path = CONF['data_path']
    location = CONF['location_type_product']
    df = init(CONF, location)

    df.to_csv(file_path + "/origin_csl.csv", index=False)
    print("Success in saving origin_csl")

def update():
    pass

def dry(conf):
    global CONF
    CONF = conf

    option = CONF["option"]

    if (option == "init"):
        print("DRY: init")
        dry_origin()
    elif (option == "update"):
        print("DRY: init")
        update()
   