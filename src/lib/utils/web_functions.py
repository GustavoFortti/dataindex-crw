import requests
from fake_useragent import UserAgent

from src.lib.utils.log import message


def check_url_existence(url, timeout=5):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}

    try:
        response = requests.head(url, headers=headers, timeout=timeout)
        return 200 <= response.status_code < 300
    except Exception as e:
        message(e)
        return False
