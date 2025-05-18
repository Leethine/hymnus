#!/bin/bash

# Customize path to store the data
if [ -z ${DATAPATH} ]; then
  export DATAPATH="blob"
fi

if [[ "${1}" == "--force" ]]; then
  installation/init-force.sh
else
  installation/init.sh
fi

echo ""
echo "Installation done."
