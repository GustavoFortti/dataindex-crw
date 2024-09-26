import argparse

def arg_parser():
    parser = argparse.ArgumentParser(description="Processa os argumentos do trabalho.")
    parser.add_argument("--job_name", type=str)
    parser.add_argument("--job_sub_name", type=str)
    parser.add_argument("--page_name", type=str)
    parser.add_argument("--job_type", type=str)
    parser.add_argument("--option", type=str, default="")
    parser.add_argument("--page_type", type=str)
    parser.add_argument("--country", type=str)
    parser.add_argument("--mode", type=str, default="")

    return parser.parse_args()