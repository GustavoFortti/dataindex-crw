import os

GIT_CONF = {
    "username": "Gustavo Fortti",
    "email": "gustavofortti@gmail.com",
    "remote_name": "origin",
    "remote_url": "https://github.com/GustavoFortti/dataindex-img.git",
    "dataindex_img_url": "https://raw.githubusercontent.com/GustavoFortti/dataindex-img/master/imgs/"
}

ELASTICSEARCH_CONF = {
    "hosts_prd": "https://dataindex-elk-1.ngrok.app/",
    "user_prd": "elastic",
    "password_prd": "RJ6XXwfjHzYICKfGRTSn",
    "hosts_dev": "http://192.168.0.102:9200",
    "user_dev": "elastic",
    "password_dev": "123456",
}

LOCAL = os.getenv("LOCAL")
DATA_PATH = LOCAL