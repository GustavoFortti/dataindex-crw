import argparse
import importlib
import sys
import traceback
from datetime import datetime

from src.lib.utils.log import message
from src.jobs.job_manager import job_manager


def parse_arguments():
    """
    Configures and returns command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Processes job arguments.")
    parser.add_argument("--job_name", type=str, required=True, help="Name of the job to execute.")
    parser.add_argument("--options", type=str, required=True, help="Job execution options.")
    parser.add_argument("--page_name", type=str, required=True, help="Page that will be executed.")
    parser.add_argument("--country", type=str, required=True, help="Country of operation.")
    parser.add_argument("--mode", type=str, default=True, help="Execution mode.")
    parser.add_argument("--local", type=str, required=True, help="Execution path.")
    
    args = parser.parse_args()
    
    message("parse arguments")
    message(vars(args))
    
    return args


def main():
    start = datetime.now()
    message(f"start - {start}")

    args = parse_arguments()
    
    try:
        job_manager(args)
    except ModuleNotFoundError:
        message(f"Error: Module for job '{args.job_name}' not found.")
        message(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)
    except AttributeError:
        message(f"Error: The module does not contain the required 'run' function.")
        message(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)
    except Exception as e:
        message(f"Error executing job '{args.job_name}': {e}")
        message(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)
    
    message(f"execution time: {datetime.now() - start} | end: {datetime.now()}")


if __name__ == "__main__":
    main()
