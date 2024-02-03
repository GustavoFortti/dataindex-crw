# /bin/bash

# export LOCAL="/home/mage/main/dataindex-crw"
export LOCAL="/home/crw-system/dataindex-crw"
export DISPLAY=:1
bash $LOCAL/setup.sh

job_name=""
job_type=""
option=""
page_type=""
country=""

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
        * )             usage
                        ;;
    esac
    shift
done

echo "Running with the following parameters:"
echo "job_name: $job_name"
echo "job_type: $job_type"
echo "option: $option"
echo "page_type: $page_type"
echo "country: $country"

echo "Command: ./launcher.sh --job_name $job_name --job_type $job_type --option $option --page_type $page_type --country $country"
python3 main.py --job_name $job_name --job_type $job_type --option $option --page_type $page_type --country $country --local $LOCAL