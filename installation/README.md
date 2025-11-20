# Installation Guide

## 1. Create environment variables
You need to add the following env variables in your `.bashrc`
```
HYMNUS_DATAPATH
# Default ~/.hymnus_data

HYMNUS_ROOT
# Default ~/.hymnus_env

HYMNUS_DB
# Default ~/.hymnus_data/tables.db

HYMNUS_FS
# Default ~/.hymnus_data/files

HYMNUS_USERS
# Default ~/.hymnus_data/users
```

If you want to be "lazy", then just run `./auto-add-env.sh` before running the installation script.

## 2. Run the installation script
In `installation` directory, run
```
./init.sh

# Or, if you don't need user prompt
./init-force.sh
```

## 3. Create Python3 virtual env
First run `./create-python-env.sh`, then `cd $HYMNUS_ROOT`. In this directory, run
```
source bin/activate
pip3 install -r requirements.txt
```
You can start the server to test if everything went well, but before that, you should also make sure all the environment variables as shown above are assigned with the correct value.
```
bin/flask --app hymnus run --debug --host=0.0.0.0
```
You can also run the app in the background:
```
nohup bin/flask --app hymnus run --debug --host=0.0.0.0 > log.txt 2>&1 &
```