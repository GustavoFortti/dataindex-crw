import logging
import importlib
from config.arg_parser import arg_parser

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

args = arg_parser()
job_name = args.job_name
page_type = args.page_type
country = args.country

module_name = f"pages.{page_type}.{country}.{job_name}.job"
module = importlib.import_module(module_name)
print(args)
module.run(args)