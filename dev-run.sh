# /bin/bash

prd_path="/home/crw-system/dataindex-crw"
dev_path="/home/mage/main/dataindex-crw"

local=""

if [ -d $prd_path ]; then
    echo "prd_path"
    local="$prd_path"
elif [ -d $dev_path ]; then
    echo "dev_path"
    local="$dev_path"
else
    echo "None of the specified directories exist."
    exit 1
fi

export LOCAL="$local"
echo $LOCAL

job_name="max_titanium"
job_type="extract"
option="status_job"
page_type="supplement"
country="brazil"
mode="prd"

python3 $LOCAL/main.py \
        --job_name $job_name \
        --job_type $job_type \
        --option "$option" \
        --page_type $page_type \
        --country $country \
        --mode $mode
