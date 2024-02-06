# /bin/bash

prd_path="/home/crw-system/dataindex-crw"
dev_path="/home/mage/main/dataindex-crw"

if [ -d $prd_path ]; then
    export LOCAL=$prd_path
elif [ -d $dev_path ]; then
    export LOCAL=$dev_path
else
    echo "None of the specified directories exist."
    exit 1
fi

python3 $LOCAL/main.py \
        --job_name adaptogen \
        --job_type extract \
        --option init \
        --page_type supplement \
        --country brazil \
        --mode dev