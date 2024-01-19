import importlib
from config.arg_parser import arg_parser

args = arg_parser()
job_name = args.job_name

module_name = f"pages.supplement.brazil.{job_name}.job"
module = importlib.import_module(module_name)

module.run(args)