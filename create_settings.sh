#!/bin/bash

# Create the config directory if it doesn't exist
mkdir -p ~/.config/obsidiansearch

# Check if the first argument is empty
if [ -z "$1" ]
then
    echo "Please provide the path to your Obsidian vault as the first argument."
    exit 1
fi

# Create the config file and set the obsidian_vault key to the first argument value
echo "[DEFAULT]" > ~/.config/obsidiansearch/config.ini
echo "obsidian_vault=$1" >> ~/.config/obsidiansearch/config.ini
# Print out the file path and file contents
echo "File path: ~/.config/obsidiansearch/config.ini"
cat ~/.config/obsidiansearch/config.ini