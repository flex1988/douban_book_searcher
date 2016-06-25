#!/usr/bin/sh

chmod u+x ./search.py
search="$PWD""/search.py"
cd /usr/local/bin
ln -s $search douban



