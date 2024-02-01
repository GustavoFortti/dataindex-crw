#!/bin/bash

export ES_HOSTS="https://dataindex-elk-1.ngrok.app/"
export ES_USER="elastic"
export ES_PASS="RJ6XXwfjHzYICKfGRTSn"

export DATAINDEX_IMG_PATH="$(pwd)/../dataindex-img"
export DATAINDEX_IMG_URL="https://raw.githubusercontent.com/GustavoFortti/dataindex-img/master/imgs/"

if [ -d $DATAINDEX_IMG_PATH ]; then
  echo "$DATAINDEX_IMG_PATH Ok"
else
  echo "Error: path does not exist $DATAINDEX_IMG_PATH"
fi