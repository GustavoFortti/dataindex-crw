# /bin/bash

local=$(pwd)
export LOCAL="$local"
echo $LOCAL

export USE_HEADLESS="false"
export CHECKPOINT_PRODUCTS_UPDATE="false"
# source $LOCAL/env/display.sh

page_names=(
    # "adaptogen"
    # "atlhetica_nutrition"
    # "black_skull"
    # "boldsnacks"
    # "dark_lab"
    # "darkness"
    # "dux_nutrition_lab"
    # "growth_supplements"
    # "integralmedica"
    # "iridium_labs"
    # "max_titanium"
    # "mercadolivre"
    # "new_millen"
    # "nutrata"
    # "oficialfarma"
    "probiotica"
    # "puravida"
    # "truesource"
    # "under_labz"
    # "vitafor"
)

job_type="master_page"
job_name="master"

exec_type="extract"
# exec_flag="status_job"
exec_flag="new_page"
# exec_flag="products_update"
# exec_flag="products_metadata_create_pages_if_not_exist"
# exec_flag="products_metadata_update_old_pages"

# exec_type="transform"
# exec_flag="false"

# exec_type="load"
# exec_flag="data_quality"
# exec_flag="false"

# job_type="data_intelligence"
# job_name="product_definition"

# job_type="data_shelf"
# job_name="history_price"

# exec_type="false"
# exec_flag="false"
# page_names="false"

page_type="supplement"
country="brazil"
mode="dev"


if [ -z "$page_names" ]; then
    python3 "$LOCAL/main.py" \
            --job_type "$job_type" \
            --job_name "$job_name" \
            --exec_type "$exec_type" \
            --exec_flag "$exec_flag" \
            --page_type "$page_type" \
            --country "$country" \
            --mode "$mode" >> "$log_file" 2>&1
else
    for page_name in "${page_names[@]}"
    do
        log_path="$LOCAL/data/$page_type/$country/$page_name/logs"
        log_file="$log_path/$(date +%Y-%m-%d).log"

        mkdir -p "$log_path"

        python3 "$LOCAL/main.py" \
            --job_type "$job_type" \
            --job_name "$job_name" \
            --page_name "$page_name" \
            --exec_type "$exec_type" \
            --exec_flag "$exec_flag" \
            --page_type "$page_type" \
            --country "$country" \
            --mode "$mode"
            #  >> "$log_file" 2>&1

        # if [ $? -ne 0 ]; then
        #     echo "Error executing job: $job_name. Stopping execution of remaining jobs."
        #     break
        # fi
    done

    echo "Todos os jobs foram executados."
fi

