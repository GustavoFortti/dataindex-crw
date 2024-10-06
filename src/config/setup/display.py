import os
import subprocess
import time
import re

from src.lib.utils.log import message



def get_used_displays():
    """
    Retorna um conjunto de números de display atualmente em uso.
    """
    try:
        # Executa o comando ps aux
        process = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
        # Filtra os processos que contêm 'Xvfb'
        grep_process = subprocess.Popen(['grep', 'Xvfb'], stdin=process.stdout, stdout=subprocess.PIPE)
        process.stdout.close()  # Fecha a entrada do pipe
        output, _ = grep_process.communicate()

        # Decodifica a saída e divide em linhas
        lines = output.decode('utf-8').splitlines()

        used_displays = set()
        for line in lines:
            if 'Xvfb' in line and 'grep' not in line:
                # Procura pelo padrão :<número>
                match = re.search(r':(\d+)', line)
                if match:
                    used_displays.add(int(match.group(1)))
        return used_displays
    except Exception as e:
        message(f"Erro ao obter displays em uso: {e}")
        return set()



def find_available_display(start=99, end=200):
    """
    Encontra um número de display disponível entre start e end.
    Retorna a string do display (por exemplo, ':99') ou None se não encontrar.
    """
    used_displays = get_used_displays()
    for display_num in range(start, end):
        if display_num not in used_displays:
            return f":{display_num}"
    return None



def start_xvfb(display):
    """
    Inicia o Xvfb no display especificado.
    Retorna o objeto subprocess.Popen ou None se falhar.
    """
    try:
        xvfb_command = ['Xvfb', display, '-screen', '0', '1280x720x24']
        xvfb_process = subprocess.Popen(xvfb_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Aguarda um pouco para garantir que o Xvfb inicie
        time.sleep(2)
        # Verifica se o Xvfb está em execução
        if xvfb_process.poll() is None:
            message(f"Xvfb iniciado em {display} com PID {xvfb_process.pid}")
            return xvfb_process
        else:
            message(f"Falha ao iniciar o Xvfb em {display}")
            return None
    except Exception as e:
        message(f"Erro ao iniciar o Xvfb em {display}: {e}")
        return None



def terminate_process(process):
    """
    Termina o processo fornecido de forma graciosa, forçando se necessário.
    """
    try:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
                message(f"Processo {process.pid} encerrado.")
            except subprocess.TimeoutExpired:
                message(f"Processo {process.pid} não encerrou em tempo, forçando encerramento.")
                process.kill()
    except Exception as e:
        message(f"Erro ao encerrar o processo {process.pid}: {e}")



def configure_display_and_test_chrome():
    """
    Encontra um display disponível, inicia o Xvfb, configura a variável DISPLAY,
    lança o Chrome em modo headless e verifica se funciona.
    Retorna True se bem-sucedido, False caso contrário.
    """
    # Encontra um display disponível
    display = find_available_display()
    if not display:
        message("Nenhum DISPLAY disponível encontrado.")
        return False
    
    # Inicia o Xvfb no display encontrado
    xvfb_process = start_xvfb(display)
    if not xvfb_process:
        message(f"Não foi possível iniciar o Xvfb em {display}")
        return False
    
    # Configura a variável de ambiente DISPLAY
    os.environ['DISPLAY'] = display
    message(f"DISPLAY configurado para {display}")
    
    # Define o caminho para o executável do Chrome
    chrome_command = "/usr/local/bin/chrome"  # Atualize este caminho se necessário
    
    # Inicia o Chrome em modo headless
    try:
        chrome_process = subprocess.Popen([
            chrome_command,
            "--headless",
            "--no-sandbox",
            "--disable-gpu",
            "--dump-dom",
            "about:blank"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Aguarda alguns segundos para o Chrome iniciar
        time.sleep(5)
        
        # Captura a saída e erros
        stdout, stderr = chrome_process.communicate(timeout=10)
        
        if chrome_process.returncode == 0:
            message(f"Chrome iniciado com sucesso com DISPLAY={display}")
            message(f"DOM: {stdout.decode()}")
            # Termina o Chrome
            chrome_process.terminate()
            try:
                chrome_process.wait(timeout=5)
                message("Chrome encerrado.")
            except subprocess.TimeoutExpired:
                message("Chrome não encerrou em tempo, forçando encerramento.")
                chrome_process.kill()
            # Limpa o Xvfb
            terminate_process(xvfb_process)
            return True
        else:
            message(f"Falha ao iniciar o Chrome com DISPLAY={display}")
            message(f"Chrome stderr: {stderr.decode().strip()}")
            # Limpa o Xvfb
            terminate_process(xvfb_process)
            return False
    except subprocess.TimeoutExpired:
        message("Timeout ao iniciar o Chrome.")
        chrome_process.kill()
        # Limpa o Xvfb
        terminate_process(xvfb_process)
        return False
    except Exception as e:
        message(f"Erro ao lançar o Chrome: {e}")
        # Limpa o Xvfb
        terminate_process(xvfb_process)
        return False



def configure_display():
    message("FUNCTION CONFIGURE DISPLAY")
    sucesso = configure_display_and_test_chrome()
    if sucesso:
        message("Configuração do DISPLAY e teste do Chrome concluídos com sucesso.")
    else:
        message("Falha na configuração do DISPLAY e/ou no teste do Chrome.")