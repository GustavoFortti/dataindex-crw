# /bin/bash

LOCAL="$(pwd)"

job_name="data_load"
options="false"
page_name="a1supplements"
country="united_states"
mode="dev"

python3 "$LOCAL/main.py" \
        --job_name "$job_name" \
        --options "$options" \
        --page_name "$page_name" \
        --country "$country" \
        --mode "$mode" \
        --local "$LOCAL"