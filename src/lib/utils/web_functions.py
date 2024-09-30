import requests
from fake_useragent import UserAgent

from src.lib.utils.log import message

def check_url_existence(url, timeout=5):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}

    try:
        # Primeiro, tenta com o método HEAD
        response = requests.head(url, headers=headers, timeout=timeout)
        if response.status_code == 405:  # Método não permitido
            # Tenta com GET se HEAD não for permitido
            response = requests.get(url, headers=headers, timeout=timeout)
        return 200 <= response.status_code < 400  # Inclui redirecionamentos
    except Exception as e:
        print(f"Erro: {e}")
        return False