#!/bin/bash

calculate_hash() {
    find . -type f -name '*.conf' -exec md5sum {} + | md5sum | cut -d" " -f1
}

HASH_FILE="./.env/requirements_hash.txt"

CURRENT_HASH=$(calculate_hash)

if [ -f "$HASH_FILE" ]; then
    PREVIOUS_HASH=$(cat "$HASH_FILE")
    if [ "$CURRENT_HASH" == "$PREVIOUS_HASH" ]; then
        echo "No changes detected. Leaving..."
        exit 0
    fi
fi

main() {
    if ! command -v python3 &> /dev/null; then
        echo "Python3 is not installed. Installing..."
        sudo apt update
        sudo apt install python3 -y
    else
        echo "Python3 is already installed."
    fi

    if ! command -v pip3 &> /dev/null; then
        echo "Pip3 is not installed. Installing..."
        sudo apt install python3-pip -y
    else
        echo "Pip3 is already installed."
    fi

    REQUIREMENTS=./.env/requirements.txt

    if [ ! -f "$REQUIREMENTS" ]; then
        echo "Requirements.txt file not found at $REQUIREMENTS"
        exit 1
    fi

    while read -r package; do
        if pip3 freeze | grep -F "$package" > /dev/null; then
            echo "Package $package is already installed. Skipping..."
        else
            echo "Installing $package..."
            pip3 install "$package"
        fi
    done < "$REQUIREMENTS"
}

main

echo "$CURRENT_HASH" > "$HASH_FILE"
