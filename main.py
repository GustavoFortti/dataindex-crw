import importlib
from config.setup import configure_env
from config.arg_parser import arg_parser

args = arg_parser()
job_name = args.job_name
page_type = args.page_type
country = args.country

configure_env(args)

# module_name = f"pages.{page_type}.{country}.{job_name}.job"
# module = importlib.import_module(module_name)

# module.run(args)