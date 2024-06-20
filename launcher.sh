# /bin/bash

job_name=""
page_type=""
country=""
mode="prd"

job_type=false
page_name=false
option=false

local="/home/crw-system/dataindex-crw"

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  --job_name NAME      Set the job name to NAME"
    echo "  --job_type TYPE      Set the job type to TYPE"
    echo "  --option OPTION      Set the option to OPTION"
    echo "  --page_name NAME     Set the page name to NAME"
    echo "  --page_type TYPE     Set the page type to TYPE"
    echo "  --country COUNTRY    Set the country to COUNTRY"
    echo "  --mode MODE          Set the mode to MODE"
    echo "  --local LOCAL        Set the local to LOCAL"
    echo
    echo "Each option must be followed by its respective value."
}

while [ "$1" != "" ]; do
    case $1 in
        --job_name )    shift
                        job_name=$1
                        ;;
        --page_name )    shift
                        page_name=$1
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
                        exit 1
                        ;;
    esac
    shift
done


export LOCAL=$local

log_path=""
if [ "$page_name" = "false" ]; then
    log_path="$LOCAL/data/$page_type/$country/$job_name/logs"
else
    log_path="$LOCAL/data/$page_type/$country/$page_name/logs"
fi
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
echo "page_name: $page_name" >> "$log_file"
echo "job_type: $job_type" >> "$log_file"
echo "option: $option" >> "$log_file"
echo "page_type: $page_type" >> "$log_file"
echo "country: $country" >> "$log_file"
echo "mode: $mode" >> "$log_file"
echo "LOCAL: $LOCAL" >> "$log_file"
echo "Job start: $(date '+%Y-%m-%d %H:%M:%S')" >> "$log_file"

python3 "$LOCAL/main.py" --job_name "$job_name" \
                         --page_name "$page_name" \
                         --job_type "$job_type" \
                         --option "$option" \
                         --page_type "$page_type" \
                         --country "$country" \
                         --mode "$mode" >> "$log_file" 2>&1

if [ $? -ne 0 ]; then
  exit 1
fi

echo "Job end: $(date '+%Y-%m-%d %H:%M:%S')" >> "$log_file"