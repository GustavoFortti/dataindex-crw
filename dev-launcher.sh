# /bin/bash

LOCAL="$(pwd)"

job_name="data_extract"
options="create_products_metadata_if_not_exist"
page_name="a1supplements"
country="united_states"
mode="prd"

python3 "$LOCAL/main.py" \
        --job_name "$job_name" \
        --options "$options" \
        --page_name "$page_name" \
        --country "$country" \
        --mode "$mode" \
        --local "$LOCAL"