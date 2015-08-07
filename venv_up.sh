#!/bin/bash

if [[ $1 == "clean"  ]]; then
    rm -r venv shorter.egg-info
    rm activate
    exit 0
fi

if [[ `which pyvenv-3.4 | wc -l` > 0 ]]; then
    pyvenv-3.4 venv
else
    pvers=`which python3.4`
    virtualenv -p $pvers venv
fi

ln -sf venv/bin/activate .
source activate

python setup.py develop
