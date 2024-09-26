import logging
import json

# Configuração do logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logging.getLogger('').addHandler(console_handler)

def message(message, is_json=False):
    """Loga uma mensagem ou JSON"""
    if is_json:
        # Se for JSON, formata de maneira legível
        formatted_json = json.dumps(message, indent=4)
        logging.info(f'\n{formatted_json}')
    else:
        # Se for uma mensagem normal, loga diretamente
        logging.info(message)
