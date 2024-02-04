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

configure_display() {
    local display_values=":0 :1 :0.0"
    local chrome_command="/usr/local/bin/chrome"

    for display in $display_values; do
        echo "Testing DISPLAY=$display"
        export DISPLAY=$display
        $chrome_command --no-sandbox --disable-gpu --dump-dom about:blank &> /dev/null &
        chrome_pid=$!

        sleep 2

        if kill -0 $chrome_pid &> /dev/null; then
            echo "Chrome started successfully with DISPLAY=$display"
            kill $chrome_pid
            return 0
        else
            echo "Failed to start Chrome with DISPLAY=$display"
        fi
    done

    echo "Failed to configure DISPLAY for Chrome"
    return 1
}

configure_display