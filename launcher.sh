#!/bin/bash

set -euo pipefail  # Exit on error, unset variable, or pipe failure

# Default variables
job_name=""
page_name=""
page_type=""
country=""
mode="prd"
local_dir="/home/crw-system/shape-data-shelf-crw"
options=""

# Load external scripts
source "$local_dir/env/display.sh"

# Display usage information
usage() {
    printf "Usage: %s [OPTIONS]\n" "$0"
    printf "  --job_name NAME       Set the job name\n"
    printf "  --options OPTIONS     Set the job options\n"
    printf "  --page_name NAME      Set the page name\n"
    printf "  --country COUNTRY     Set the country\n"
    printf "  --mode MODE           Set the mode (default: prd)\n"
    printf "  --local LOCAL_DIR     Set the local directory (default: %s)\n" "$local_dir"
    printf "  -h, --help            Display this help and exit\n"
}

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
    case "$1" in
        --job_name)
            shift
            job_name="$1"
            ;;
        --options)
            shift
            options="$1"
            ;;
        --page_name)
            shift
            page_name="$1"
            ;;
        --country)
            shift
            country="$1"
            ;;
        --mode)
            shift
            mode="$1"
            ;;
        --local)
            shift
            local_dir="$1"
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            printf "Error: Invalid option '%s'\n" "$1"
            usage
            exit 1
            ;;
    esac
    shift
done

# Validate required variables
if [ -n "$page_name" ]; then
    log_name="$page_name"
elif [ -n "$job_name" ]; then
    log_name="$job_name"
else
    printf "Error: Both page_name and job_name are empty.\n"
    exit 1
fi

# Set environment variables
export LOCAL_DIR="$local_dir"

# Create log directory
log_path="$LOCAL_DIR/data/$page_type/$country/$log_name/logs"
mkdir -p "$log_path"
log_file="$log_path/$(date +%Y-%m-%d).log"

# Log the execution details
{
    printf "Log file path: %s\n" "$log_file"
    printf "Running with the following parameters:\n"
    printf "  job_name: %s\n" "$job_name"
    printf "  options: %s\n" "$options"
    printf "  page_name: %s\n" "$page_name"
    printf "  country: %s\n" "$country"
    printf "  mode: %s\n" "$mode"
    printf "  local_dir: %s\n" "$local_dir"
    printf "Job started at: %s\n" "$(date '+%Y-%m-%d %H:%M:%S')"
} >> "$log_file"

# Execute the main Python script
if ! python3 "$LOCAL_DIR/main.py" \
    --job_name "$job_name" \
    --options "$options" \
    --page_name "$page_name" \
    --country "$country" \
    --mode "$mode" \
    --local "$local_dir" >> "$log_file" 2>&1; then
    printf "Error: Job execution failed.\n" >> "$log_file"
    exit 1
fi

# Log job completion
printf "Job completed at: %s\n" "$(date '+%Y-%m-%d %H:%M:%S')" >> "$log_file"
