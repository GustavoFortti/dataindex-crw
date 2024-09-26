import os
from datetime import datetime

ES_CONF = {
    "hosts_prd": "https://dataindex-elk-node-1.ngrok.app/",
    "user_prd": "elastic",
    "password_prd": "RJ6XXwfjHzYICKfGRTSn",
    "hosts_dev": "http://192.168.0.102:9200",
    "user_dev": "elastic",
    "password_dev": "123456",
}


def configure_elasticsearch(env):
    if env == "dev":
        os.environ['ES_HOSTS'] = ES_CONF["hosts_dev"]
        os.environ['ES_USER'] = ES_CONF["user_dev"]
        os.environ['ES_PASS'] = ES_CONF["password_dev"]
    else:
        os.environ['ES_HOSTS'] = ES_CONF["hosts_prd"]
        os.environ['ES_USER'] = ES_CONF["user_prd"]
        os.environ['ES_PASS'] = ES_CONF["password_prd"]
        
    data_atual = datetime.now()
    INDEX_DATE = data_atual.strftime("%d%m%Y")
    
    os.environ['INDEX_DATE'] = INDEX_DATE