export LOCAL="/home/mage/main/dataindex-crw"
# export LOCAL="/home/crw-system/dataindex-crw"

bash $LOCAL/setup.sh $mode

python3 $LOCAL/main.py \
        --job_name darkness \
        --job_type extract \
        --option status_job \
        --page_type supplement \
        --country brazil \
        --local $LOCAL