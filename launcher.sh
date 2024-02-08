# /bin/bash

job_name=""
job_type=""
option="false"
page_type=""
country=""
mode="prd"
local="/home/crw-system/dataindex-crw"

usage() {
  echo "Usage: $0 --job_name NAME --job_type TYPE --option OPTION --page_type PAGE_TYPE --country COUNTRY"
  exit 1
}

if [ "$#" -eq 0 ]; then
    usage
fi

while [ "$1" != "" ]; do
    case $1 in
        --job_name )    shift
                        job_name=$1
                        ;;
        --job_type )    shift
                        job_type=$1
                        ;;
        --option )      shift
                        option=$1
                        ;;
        --page_type )   shift
                        page_type=$1
                        ;;
        --country )     shift
                        country=$1
                        ;;
        --mode )        shift
                        mode=$1
                        ;;
        --local )       shift
                        local=$1
                        ;;
        * )             usage
                        ;;
    esac
    shift
done

export LOCAL=$local
log_path="$LOCAL/data/$page_type/$country/$job_name/logs"
log_file="$log_path/$(date +%Y-%m-%d).log"

if [ ! -d "$log_path" ]; then
    mkdir -p "$log_path"
fi

if [ -z "$log_file" ]; then
    echo "The log_file variable is not set or is empty. Cannot proceed with logging."
    exit 1
else
    touch "$log_file"
fi

echo "Running with the following parameters:" >> "$log_file"
echo "job_name: $job_name" >> "$log_file"
echo "job_type: $job_type" >> "$log_file"
echo "option: $option" >> "$log_file"
echo "page_type: $page_type" >> "$log_file"
echo "country: $country" >> "$log_file"
echo "mode: $mode" >> "$log_file"
echo "LOCAL: $LOCAL" >> "$log_file"
echo "Job start: $(date '+%Y-%m-%d %H:%M:%S')" >> "$log_file"

python3 "$LOCAL/main.py" --job_name "$job_name" \
                         --job_type "$job_type" \
                         --option "$option" \
                         --page_type "$page_type" \
                         --country "$country" \
                         --mode "$mode" >> "$log_file" 2>&1

if [ $? -ne 0 ]; then
  exit 1
fi

echo "Job end: $(date '+%Y-%m-%d %H:%M:%S')" >> "$log_file"