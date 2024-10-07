#!/bin/bash

job_name=""
page_type=""
country=""
mode="prd"
exec_type=false
page_name=false
exec_flag=false
local="/home/crw-system/shape-data-shelf-crw"

export USE_HEADLESS="false"
export CHECKPOINT_EXTRACT="true"

if [[ "$exec_type" == "extract" || "$exec_type" == "transform" ]]; then
    source $local/env/display.sh
fi

usage() {
    echo "Usage: $0"
    echo "flags:"
    echo "  --job_type NAME      Set the job type to TYPE"
    echo "  --job_name NAME      Set the job name to NAME"
    echo "  --exec_type TYPE     Set the exec type to exec"
    echo "  --exec_flag FLAG     Set the exec_flag to FLAG"
    echo "  --page_name NAME     Set the page name to NAME"
    echo "  --page_type TYPE     Set the page type to TYPE"
    echo "  --country COUNTRY    Set the country to COUNTRY"
    echo "  --mode MODE          Set the mode to MODE"
    echo "  --local LOCAL        Set the local to LOCAL"
    echo
    echo "Each exec_flag must be followed by its respective value."
}

while [ "$1" != "" ]; do
    case $1 in
        --job_type )    shift
                        job_type=$1
                        ;;
        --job_name )    shift
                        job_name=$1
                        ;;
        --page_name )   shift
                        page_name=$1
                        ;;
        --exec_type )   shift
                        exec_type=$1
                        ;;
        --exec_flag )   shift
                        exec_flag=$1
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

if [ "$page_name" != "false" ] && [ ! -z "$page_name" ]; then
    log_name="$page_name"
elif [ "$job_name" != "false" ] && [ ! -z "$job_name" ]; then
    log_name="$job_name"
else
    echo "Error: both page_name and job_name are empty or false."
    exit 1
fi

export LOCAL=$local

log_path="$LOCAL/data/$page_type/$country/$log_name/logs"
mkdir -p "$log_path"
log_file="$log_path/$(date +%Y-%m-%d).log"
echo "Log file path: $log_file"

echo "Running with the following parameters:" >> "$log_file"
echo "job_type: $job_type" >> "$log_file"
echo "job_name: $job_name" >> "$log_file"
echo "exec_type: $exec_type" >> "$log_file"
echo "exec_flag: $exec_flag" >> "$log_file"
echo "page_name: $page_name" >> "$log_file"
echo "page_type: $page_type" >> "$log_file"
echo "country: $country" >> "$log_file"
echo "mode: $mode" >> "$log_file"
echo "LOCAL: $LOCAL" >> "$log_file"
echo "Job start: $(date '+%Y-%m-%d %H:%M:%S')" >> "$log_file"

python3 "$LOCAL/main.py" --job_type "$job_type" \
                            --job_name "$job_name" \
                            --exec_type "$exec_type" \
                            --exec_flag "$exec_flag" \
                            --page_name "$page_name" \
                            --page_type "$page_type" \
                            --country "$country" \
                            --mode "$mode" >> "$log_file" 2>&1

if [ $? -ne 0 ]; then
    exit 1
fi

echo "Job end: $(date '+%Y-%m-%d %H:%M:%S')" >> "$log_file"
