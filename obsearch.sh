#!/bin/bash

# copy to /usr/local/bin/obsearch
# chmod +x /usr/local/bin/obsearch

# Assuming your virtual environment is in /home/chris/code/obsearch/venv
cd /home/chris/code/obsidiansearch
source dev/bin/activate
./dev/bin/python obsearch.py "$1" "$2"