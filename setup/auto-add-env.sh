#!/bin/bash

HYMNUS_DATAPATH=$HOME/.hymnus_data

echo "" >> $HOME/.bashrc
echo "" >> $HOME/.bashrc
echo "export HYMNUS_DATAPATH=$HOME/.hymnus_data"   >> $HOME/.bashrc
echo "export HYMNUS_ROOT=$HOME/.hymnus_env"        >> $HOME/.bashrc
echo "export HYMNUS_DB=$HYMNUS_DATAPATH/tables.db" >> $HOME/.bashrc
echo "export HYMNUS_FS=$HYMNUS_DATAPATH/files"     >> $HOME/.bashrc
echo "export HYMNUS_USERS=$HYMNUS_DATAPATH/users"  >> $HOME/.bashrc