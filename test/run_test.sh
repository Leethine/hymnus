#!/bin/bash

# Customize path to store the data
export DATAPATH="blob"

installation/init-force.sh

script/batch-insert-composers.sh script/famous-composers.csv

bash test/test_insert.sh

bash test/test_delete.sh
