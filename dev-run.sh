# export LOCAL="/home/crw-system/dataindex-crw"
export LOCAL="/home/mage/main/dataindex-crw"

python3 $LOCAL/main.py \
        --job_name darkness \
        --job_type dry \
        --option default \
        --page_type supplement \
        --country brazil \
        --mode dev