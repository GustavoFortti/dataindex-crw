# /bin/bash

# local="/home/crw-system/dataindex-crw"
local="/home/mage/main/dataindex-crw"

export LOCAL="$local"
echo $LOCAL

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
    # "new_millen"
    # "nutrata"
    # "probiotica"
    # "truesource"
    # "under_labz"
    "vitafor"
)

# Variáveis comuns para todos os jobs
# job_name="_set_coder_"
job_name="_set_page_"
# job_name="_set_carousel_"
# job_name="_set_product_def_"
# job_name="_set_search_def_"
# job_name="_set_elaticsearch_"
# job_name="_set_history_price_"

job_type="extract"
option="update_products"

# job_type="extract"
    # --option status_job
    # --option update_products
    # --option create_pages
    # --option update_old_pages
# --job_type dry
# --job_type ingestion
    # --option data_quality
    # --option 

page_type="supplement"
country="brazil"
mode="prd"

for page_name in "${page_names[@]}"
do
    echo "Executing job: $page_name"
    python3 "$LOCAL/main.py" \
        --job_name "$job_name" \
        --page_name "$page_name" \
        --job_type "$job_type" \
        --option "$option" \
        --page_type "$page_type" \
        --country "$country" \
        --mode "$mode"
    
    if [ $? -ne 0 ]; then
        echo "Error executing job: $job_name. Stopping execution of remaining jobs."
        break
    fi
done

echo "Todos os jobs foram executados."