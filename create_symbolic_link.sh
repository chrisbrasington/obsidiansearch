#!/bin/bash
if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi

echo 'Creating symbolic link from here to /usr/local/bin/obsearch'
echo "If you don't want to keep this local folder, run create_exec.sh instead"

if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi

# Get current working directory
cwd=$(pwd)

# Create symbolic link to obsearch.py in /usr/local/bin
ln -s "$cwd/obsearch.py" /usr/local/bin/obsearch

ls -al /usr/local/bin/obsearch