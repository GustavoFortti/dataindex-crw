import argparse
import importlib
import sys
import traceback

from src.config.setup.display import configure_display
from src.lib.utils.log import message


def parse_arguments():
    """
    Configura e retorna os argumentos da linha de comando.
    """
    parser = argparse.ArgumentParser(description="Processa os argumentos do trabalho.")
    parser.add_argument("--job_type", type=str, help="")
    parser.add_argument("--job_name", type=str, help="Nome do trabalho a ser executado.")
    parser.add_argument("--page_name", type=str, help="Nome da página.")
    parser.add_argument("--exec_type", type=str, required=True, choices=["extract", "transform", "load", "false"], help="Tipo de trabalho.")
    parser.add_argument("--exec_flag", type=str, default="", help="Opções adicionais.")
    parser.add_argument("--page_type", type=str, help="Tipo de página.")
    parser.add_argument("--country", type=str, help="País de operação.")
    parser.add_argument("--mode", type=str, default="", help="Modo de execução.")
    
    args = parser.parse_args()
    
    message("PARSE ARGUMENTS")
    message(vars(args))
    
    return args

def configure_system(args):
    """
    Configura o sistema com base nos argumentos fornecidos.
    """
    message("CONFIGURE SYSTEM")

    # Configurações específicas para tipos de trabalho
    if args.exec_type in ["extract", "transform"]:
        configure_display()

def run_job(args):
    """
    Importa dinamicamente e executa o módulo de trabalho especificado.
    Mostra o caminho completo e a stack trace em caso de erro.
    """

    try:
        # Define o caminho do módulo do job
        module_path = f"src.jobs.{args.job_type}.{args.job_name}.job"
        # Importa o módulo dinamicamente
        job_module = importlib.import_module(module_path)
        # Executa a função 'run' do módulo do job
        job_module.run(args)
    except ModuleNotFoundError as e:
        message(f"Erro: Módulo para o job '{args.job_name}' não encontrado.")
        message(f"Caminho: {traceback.format_exc()}")
        sys.exit(1)
    except AttributeError as e:
        message(f"Erro: O módulo '{module_path}' não possui a função 'run'.")
        message(f"Caminho: {traceback.format_exc()}")
        sys.exit(1)
    except Exception as e:
        message(f"Erro ao executar o job '{args.job_name}': {e}")
        message(f"Caminho: {traceback.format_exc()}")
        sys.exit(1)

def main():
    message("START SYSTEM")
    # Analisa os argumentos da linha de comando
    args = parse_arguments()
    
    print(args)

    # Executa o job
    run_job(args)
    

if __name__ == "__main__":
    main()
