#!/bin/bash

# Customize path to store the data
export DATAPATH="blob"

if [[ "${1}" == "--force" ]]; then
  installation/init-force.sh
else
  installation/init.sh
fi

script/batch-insert-composers.sh script/famous-composers.csv

echo ""
echo "Installation done."
