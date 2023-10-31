#!/bin/bash

if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi

if [ -f "/usr/local/bin/obsearch" ]; then
    rm /usr/local/bin/obsearch
fi

cp obsearch.py /usr/local/bin/obsearch
chmod 755 /usr/local/bin/obsearch

which obsearch
echo 'try running with `obsearch`'