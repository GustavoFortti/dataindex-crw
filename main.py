import importlib
from config.setup import configure_env
from config.arg_parser import arg_parser

args = arg_parser()
job_name = args.job_name
job_sub_name = args.job_sub_name

configure_env(args)

module_name = f"jobs.{job_name}.{job_sub_name}.job"
module = importlib.import_module(module_name)

module.run(args)