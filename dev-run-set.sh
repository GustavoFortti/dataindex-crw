# /bin/bash

# local="/home/crw-system/dataindex-crw"
local="/home/mage/main/dataindex-crw"

export LOCAL="$local"
echo $LOCAL

page_names='false'

# Variáveis comuns para todos os jobs
# job_name="_set_coder_"
# job_name="_set_carousel_"
# job_name="_set_product_def_"
job_name="_set_search_def_"
# job_name="_set_elaticsearch_"
# job_name="_set_history_price_"

job_type="false"
option="false"

page_type="supplement"
country="brazil"
mode="prd"

echo "Executing job_name: $job_name"
echo "Executing page_name: $page_name"
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

echo "Todos os jobs foram executados."