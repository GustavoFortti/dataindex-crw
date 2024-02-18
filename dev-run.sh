# /bin/bash

# local="/home/crw-system/dataindex-crw"
local="/home/mage/main/dataindex-crw"

export LOCAL="$local"
echo $LOCAL

job_name="atlhetica_nutrition"
job_type="ingestion"
option="data_quality"
page_type="supplement"
country="brazil"
mode="prd"

python3 "$LOCAL/main.py" \
        --job_name $job_name \
        --job_type $job_type \
        --option "$option" \
        --page_type $page_type \
        --country $country \
        --mode $mode
