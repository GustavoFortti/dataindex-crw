import importlib
from config.env import configure_env
from config.arg_parser import arg_parser

configure_env()

args = arg_parser()
job_name = args.job_name
page_type = args.page_type
country = args.country

module_name = f"pages.{page_type}.{country}.{job_name}.job"
module = importlib.import_module(module_name)

module.run(args)