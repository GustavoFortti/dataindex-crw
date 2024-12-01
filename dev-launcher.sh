#!/bin/bash

ARGS="$@"

# Ensure yq is installed
if ! command -v yq &> /dev/null
then
    echo "yq could not be found. Please install yq to proceed."
    exit 1
fi

# Set the current working directory
LOCAL=$(pwd)
export LOCAL="$LOCAL"
echo "Local directory set to: $LOCAL"

# Set environment variables
export USE_HEADLESS="false"
export CHECKPOINT_EXTRACT_DATA="true"

# Initialize default variables
page_type="supplement"
country="united_states"
mode="dev"

CONFIG_FILE="job_config.yaml"

# Function to select the job_type
select_job_type() {
    echo "Select the job type (job_type):"
    PS3="Choose an option: "
    options=("master_page" "data_intelligence" "data_shelf" "Exit")
    select opt in "${options[@]}"
    do
        case $opt in
            "master_page")
                JOB_TYPE="master_page"
                break
                ;;
            "data_intelligence")
                JOB_TYPE="data_intelligence"
                break
                ;;
            "data_shelf")
                JOB_TYPE="data_shelf"
                break
                ;;
            "Exit")
                echo "Exiting..."
                exit 0
                ;;
            *) echo "Invalid option $REPLY. Please try again.";;
        esac
    done
}

# Function to select the job_name based on job_type
select_job_name() {
    echo "Select the job name (job_name) for job type '$JOB_TYPE':"
    PS3="Choose an option: "
    case $JOB_TYPE in
        "master_page")
            options=("master" "Exit")
            ;;
        "data_intelligence")
            options=("product_description" "product_remeke_description" "product_class" "product_flavor" "Exit")
            ;;
        "data_shelf")
            options=("history_price" "load_master" "Exit")
            ;;
        *)
            echo "Invalid job_type."
            exit 1
            ;;
    esac

    select opt in "${options[@]}"
    do
        case $opt in
            "master"|"product_description"|"product_remeke_description"|"product_class"|"product_flavor"|"history_price"|"load_master")
                JOB_NAME=$opt
                break
                ;;
            "Exit")
                echo "Exiting..."
                exit 0
                ;;
            *) echo "Invalid option $REPLY. Please try again.";;
        esac
    done
}

# Function to select the exec_type based on job_name
select_exec_type() {
    echo "Select the execution type (exec_type) for job '$JOB_NAME':"
    PS3="Choose an option: "
    case $JOB_NAME in
        "master"|"product_description"|"product_remeke_description"|"product_class"|"product_flavor"|"history_price"|"load_master")
            options=("extract" "transform" "load" "Exit")
            ;;
        *)
            echo "Invalid job_name."
            exit 1
            ;;
    esac

    select opt in "${options[@]}"
    do
        case $opt in
            "extract"|"transform"|"load")
                EXEC_TYPE=$opt
                break
                ;;
            "Exit")
                echo "Exiting..."
                exit 0
                ;;
            *) echo "Invalid option $REPLY. Please try again.";;
        esac
    done
}

# Function to select the exec_flag based on exec_type
select_exec_flag() {
    echo "Select the execution flag (exec_flag) for exec_type '$EXEC_TYPE':"
    PS3="Choose an option: "
    case $EXEC_TYPE in
        "extract")
            options=("status_job" "new_page" "products_update" "products_metadata_create_pages_if_not_exist" "products_metadata_update_old_pages" "Exit")
            ;;
        "transform")
            options=("data_quality" "Exit")
            ;;
        "load")
            options=("data_load_flag1" "data_load_flag2" "Exit") # Replace with actual flags for 'load' if available
            ;;
        *)
            echo "Invalid exec_type."
            exit 1
            ;;
    esac

    select opt in "${options[@]}"
    do
        case $opt in
            "status_job"|"new_page"|"products_update"|"products_metadata_create_pages_if_not_exist"|"products_metadata_update_old_pages"|"data_quality"|"data_load_flag1"|"data_load_flag2")
                EXEC_FLAG=$opt
                break
                ;;
            "Exit")
                echo "Exiting..."
                exit 0
                ;;
            *) echo "Invalid option $REPLY. Please try again.";;
        esac
    done
}

# Function to configure page_names with numbered selections
configure_page_names() {
    AVAILABLE_PAGES=()

    case $JOB_TYPE in
        "master_page")
            if [ "$JOB_NAME" == "master" ]; then
                AVAILABLE_PAGES=("a1supplements" "b2vitamins" "c3minerals" "d4probiotics")
            fi
            ;;
        "data_intelligence")
            case $JOB_NAME in
                "product_description")
                    AVAILABLE_PAGES=("desc_page1" "desc_page2")
                    ;;
                "product_class")
                    AVAILABLE_PAGES=("class_page1" "class_page2")
                    ;;
                # Add more job_name cases if needed
                *)
                    AVAILABLE_PAGES=()
                    ;;
            esac
            ;;
        "data_shelf")
            case $JOB_NAME in
                "history_price")
                    AVAILABLE_PAGES=("price_page1" "price_page2")
                    ;;
                "load_master")
                    AVAILABLE_PAGES=("load_page1" "load_page2")
                    ;;
                # Add more job_name cases if needed
                *)
                    AVAILABLE_PAGES=()
                    ;;
            esac
            ;;
        *)
            AVAILABLE_PAGES=()
            ;;
    esac

    if [ ${#AVAILABLE_PAGES[@]} -gt 0 ]; then
        echo "Select the page names (page_names) by entering their numbers separated by space:"
        # Display available pages with numbering
        for i in "${!AVAILABLE_PAGES[@]}"; do
            echo "$((i+1))) ${AVAILABLE_PAGES[$i]}"
        done

        while true; do
            read -p "Enter the numbers of the pages to select (e.g., 1 3): " -a SELECTED_NUMBERS
            # Validate input
            VALID=true
            SELECTED_PAGES=()
            for num in "${SELECTED_NUMBERS[@]}"; do
                if ! [[ "$num" =~ ^[0-9]+$ ]] || [ "$num" -lt 1 ] || [ "$num" -gt "${#AVAILABLE_PAGES[@]}" ]; then
                    echo "Invalid selection: $num. Please enter numbers between 1 and ${#AVAILABLE_PAGES[@]}."
                    VALID=false
                    break
                fi
                # Avoid duplicates
                if [[ ! " ${SELECTED_PAGES[@]} " =~ " ${AVAILABLE_PAGES[$((num-1))]} " ]]; then
                    SELECTED_PAGES+=("${AVAILABLE_PAGES[$((num-1))]}")
                fi
            done
            if [ "$VALID" = true ]; then
                PAGE_NAMES=("${SELECTED_PAGES[@]}")
                break
            fi
        done
    else
        PAGE_NAMES=()
    fi
}

# Function to display the final configuration
display_configuration() {
    echo ""
    echo "===== Final Configuration ====="
    echo "job_type: \"$JOB_TYPE\""
    echo "job_name: \"$JOB_NAME\""
    echo "exec_type: \"$EXEC_TYPE\""
    echo "exec_flag: \"$EXEC_FLAG\""
    if [ ${#PAGE_NAMES[@]} -gt 0 ]; then
        echo "page_names:"
        for name in "${PAGE_NAMES[@]}"; do
            echo "  - \"$name\""
        done
    else
        echo "page_names: false"
    fi
    echo "=============================="
}

# Function to save the configuration to a YAML file
save_configuration() {
    echo "job_type: \"$JOB_TYPE\"" > "$CONFIG_FILE"
    echo "job_name: \"$JOB_NAME\"" >> "$CONFIG_FILE"
    echo "exec_type: \"$EXEC_TYPE\"" >> "$CONFIG_FILE"
    echo "exec_flag: \"$EXEC_FLAG\"" >> "$CONFIG_FILE"
    if [ ${#PAGE_NAMES[@]} -gt 0 ]; then
        echo "page_names:" >> "$CONFIG_FILE"
        for name in "${PAGE_NAMES[@]}"; do
            echo "  - \"$name\"" >> "$CONFIG_FILE"
        done
    else
        echo "page_names: false" >> "$CONFIG_FILE"
    fi

    echo "Configuration saved to $CONFIG_FILE"
}

# Function to execute the Python script
execute_python_script() {
    if [ ${#PAGE_NAMES[@]} -eq 0 ]; then
        # If page_names is empty or not set
        log_file="$LOCAL/logs/$(date +%Y-%m-%d).log"
        mkdir -p "$(dirname "$log_file")"

        python3 "$LOCAL/main.py" \
            --job_type "$JOB_TYPE" \
            --job_name "$JOB_NAME" \
            --exec_type "$EXEC_TYPE" \
            --exec_flag "$EXEC_FLAG" \
            --page_type "$page_type" \
            --country "$country" \
            --mode "$mode" >> "$log_file" 2>&1

        echo "Job executed and logged to $log_file"
    else
        # If page_names are provided
        for page_name in "${PAGE_NAMES[@]}"
        do
            log_path="$LOCAL/data/$page_type/$country/$page_name/logs"
            log_file="$log_path/$(date +%Y-%m-%d).log"

            mkdir -p "$log_path"

            python3 "$LOCAL/main.py" \
                --job_type "$JOB_TYPE" \
                --job_name "$JOB_NAME" \
                --page_name "$page_name" \
                --exec_type "$EXEC_TYPE" \
                --exec_flag "$EXEC_FLAG" \
                --page_type "$page_type" \
                --country "$country" \
                --mode "$mode" >> "$log_file" 2>&1
        done

        echo "All jobs executed and logged."
    fi
}

# Function to load configuration from job_config.yaml
load_configuration() {
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "Configuration file '$CONFIG_FILE' does not exist."
        exit 1
    fi

    # Extract variables using yq
    JOB_TYPE=$(yq e '.job_type' "$CONFIG_FILE")
    JOB_NAME=$(yq e '.job_name' "$CONFIG_FILE")
    EXEC_TYPE=$(yq e '.exec_type' "$CONFIG_FILE")
    EXEC_FLAG=$(yq e '.exec_flag' "$CONFIG_FILE")
    PAGE_NAMES_RAW=$(yq e '.page_names' "$CONFIG_FILE")

    # Initialize PAGE_NAMES array
    PAGE_NAMES=()

    if [ "$PAGE_NAMES_RAW" != "false" ]; then
        # Read each page name into the array
        while IFS= read -r line; do
            # Trim leading and trailing quotes and spaces
            page=$(echo "$line" | sed 's/- "//;s/"$//')
            PAGE_NAMES+=("$page")
        done <<< "$(echo "$PAGE_NAMES_RAW" | yq e '.[]' -)"
    fi

    # Check for mandatory parameters
    MISSING_PARAMS=()
    [ -z "$JOB_TYPE" ] && MISSING_PARAMS+=("job_type")
    [ -z "$JOB_NAME" ] && MISSING_PARAMS+=("job_name")
    [ -z "$EXEC_TYPE" ] && MISSING_PARAMS+=("exec_type")
    [ -z "$EXEC_FLAG" ] && MISSING_PARAMS+=("exec_flag")

    if [ ${#MISSING_PARAMS[@]} -ne 0 ]; then
        echo "Configuration file '$CONFIG_FILE' is missing the following required parameter(s): ${MISSING_PARAMS[@]}"
        exit 1
    fi

    echo "Configuration loaded from $CONFIG_FILE"
}

# Function to re-execute using the loaded configuration
reexecute_configuration() {
    load_configuration
    display_configuration
    execute_python_script
}

# Function to display the main menu
main_menu() {
    if [[ " $ARGS " == *" reexecute "* ]]; then
        echo "Re-executing configuration..."
        reexecute_configuration
        return
    fi

    echo "==================================="
    echo "        Job Execution Menu        "
    echo "==================================="

    PS3="Please enter your choice (1-3): "
    options=("Create New Configuration" "Re-execute from Configuration" "Exit")
    select opt in "${options[@]}"
    do
        case $opt in
            "Create New Configuration")
                create_new_configuration
                break
                ;;
            "Re-execute from Configuration")
                reexecute_configuration
                break
                ;;
            "Exit")
                echo "Exiting..."
                exit 0
                ;;
            *) echo "Invalid option $REPLY. Please try again.";;
        esac
    done
}

# Function to create a new configuration
create_new_configuration() {
    select_job_type
    select_job_name
    select_exec_type
    select_exec_flag
    configure_page_names
    display_configuration
    save_configuration
    execute_python_script
}

# Function to display the final configuration
display_configuration() {
    echo ""
    echo "===== Final Configuration ====="
    echo "job_type: \"$JOB_TYPE\""
    echo "job_name: \"$JOB_NAME\""
    echo "exec_type: \"$EXEC_TYPE\""
    echo "exec_flag: \"$EXEC_FLAG\""
    if [ ${#PAGE_NAMES[@]} -gt 0 ]; then
        echo "page_names:"
        for name in "${PAGE_NAMES[@]}"; do
            echo "  - \"$name\""
        done
    else
        echo "page_names: false"
    fi
    echo "=============================="
}

# Main function to orchestrate the selections and execution
main() {
    while true; do
        main_menu
        echo ""
    done
}

# Execute the main function
main