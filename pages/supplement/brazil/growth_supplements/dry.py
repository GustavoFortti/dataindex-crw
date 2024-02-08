from shared.data_enrichment import process_data

def create_origin_dry():
    file_path = CONF['data_path']
    df = process_data(CONF)
    df['name'] = df['name'].str.replace('- growth supplements', '')
    
    df.to_csv(file_path + "/origin_dry.csv", index=False)
    print("Success in saving origin_csl")

def dry(conf):
    global CONF
    CONF = conf

    print("Data Dry")
    create_origin_dry()


   