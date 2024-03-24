# /bin/bash

# local="/home/crw-system/dataindex-crw"
local="/home/mage/main/dataindex-crw"

export LOCAL="$local"
echo $LOCAL

job_names=(
    # "adaptogen"
    # "atlhetica_nutrition"
    # "black_skull"
    # "boldsnacks"
    # "dark_lab"
    # "darkness"
    # "dux_nutrition_lab"
    # "growth_supplements"
        "integralmedica"
    # "iridium_labs"
    # "max_titanium"
    # "new_millen"
        # "nutrata"
    # "probiotica"
    # "truesource"
    # "under_labz"
    # "vitafor"
    # "_set_carousel_"
    # "_set_product_def_"
)

# Variáveis comuns para todos os jobs
job_type="dry"
option="false"
page_type="supplement"
country="brazil"
mode="prd"

for job_name in "${job_names[@]}"
do
    echo "Executing job: $job_name"
    python3 "$LOCAL/main.py" \
        --job_name "$job_name" \
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