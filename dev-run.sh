# /bin/bash

local="/home/crw-system/dataindex-crw"
# local="/home/mage/main/dataindex-crw"

export LOCAL="$local"
echo $LOCAL

# job_name="adaptogen"
# job_type="extract"
# option="extract_new_pages"
# page_type="supplement"
# country="brazil"
# mode="prd"

# python3 "$LOCAL/main.py" \
#         --job_name $job_name \
#         --job_type $job_type \
#         --option "$option" \
#         --page_type $page_type \
#         --country $country \
#         --mode $mode

# Lista de job_names

job_names=(
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
job_type="extract"
option="create_pages"
page_type="supplement"
country="brazil"
mode="prd"

# Loop pela lista de job_names e execução do script para cada um
for job_name in "${job_names[@]}"
do
    echo "Executando job: $job_name"
    python3 "$LOCAL/main.py" \
        --job_name "$job_name" \
        --job_type "$job_type" \
        --option "$option" \
        --page_type "$page_type" \
        --country "$country" \
        --mode "$mode"
done

echo "Todos os jobs foram executados."