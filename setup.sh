#!/bin/bash

if [ "$1" == "dev" ]; then
    export ES_HOSTS="http://192.168.0.102/"
    export ES_USER="elastic"
    export ES_PASS="123456"
else
    export ES_HOSTS="https://dataindex-elk-1.ngrok.app/"
    export ES_USER="elastic"
    export ES_PASS="RJ6XXwfjHzYICKfGRTSn"
fi

export DATAINDEX_IMG_PATH="$LOCAL/../dataindex-img"
export DATAINDEX_IMG_URL="https://raw.githubusercontent.com/GustavoFortti/dataindex-img/master/imgs/"

if [ -d $DATAINDEX_IMG_PATH ]; then
  echo "$DATAINDEX_IMG_PATH Ok"
else
  echo "Error: path does not exist $DATAINDEX_IMG_PATH"
fi