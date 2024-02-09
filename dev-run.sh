# /bin/bash

# local="/home/crw-system/dataindex-crw"
local="/home/mage/main/dataindex-crw"

export LOCAL="$local"
echo $LOCAL

job_name="growth_supplements"
job_type="extract"
option="update_products"
page_type="supplement"
country="brazil"
mode="dev"

python3 "$LOCAL/main.py" \
        --job_name $job_name \
        --job_type $job_type \
        --option "$option" \
        --page_type $page_type \
        --country $country \
        --mode $mode
