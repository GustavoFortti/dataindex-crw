import logging
import json
from typing import Union, Dict

def setup_logging(log_file: str = 'app.log') -> None:
    """
    Configura o sistema de logging para registrar mensagens em um arquivo e no console.
    
    Args:
        log_file (str): Caminho para o arquivo de log. Padrão é 'app.log'.
    """
    # Configuração básica para o arquivo de log
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    # Opcional: Configurações adicionais para handlers específicos podem ser adicionadas aqui
    # Por exemplo, definir diferentes níveis para arquivo e console
    # logger = logging.getLogger()
    # logger.handlers[0].setLevel(logging.DEBUG)  # Arquivo
    # logger.handlers[1].setLevel(logging.INFO)   # Console

def message(msg: Union[str, Dict], level: str = 'info') -> None:
    """
    Registra uma mensagem no log. Aceita strings ou dicionários.
    
    Args:
        msg (Union[str, Dict]): Mensagem a ser registrada. Pode ser uma string ou um dicionário.
        level (str): Nível de logging ('debug', 'info', 'warning', 'error', 'critical'). Padrão é 'info'.
    """
    logger = logging.getLogger()

    # Serializa dicionários para JSON
    if isinstance(msg, dict):
        try:
            msg = json.dumps(msg, ensure_ascii=False)
        except (TypeError, ValueError) as e:
            logger.error(f"Falha ao serializar o dicionário para JSON: {e}")
            msg = str(msg)  # Fallback para string caso a serialização falhe

    # Mapeia o nível de logging para os métodos correspondentes
    level = level.lower()
    if level == 'debug':
        logger.debug(msg)
    elif level == 'info':
        logger.info(msg)
    elif level == 'warning':
        logger.warning(msg)
    elif level == 'error':
        logger.error(msg)
    elif level == 'critical':
        logger.critical(msg)
    else:
        logger.info(msg)  # Fallback para 'info' se o nível for desconhecido

setup_logging()