# Installation Guide

## 1. Create environment variables
You will need the following env variables before running the app.
```
# The root directory of Flask web app
HYMNUS_ROOT
# The database location (e.g. sqlite3 db file path)
HYMNUS_DB
# File system path where the score files are located
HYMNUS_FS
# Directory where user auth files are stored
HYMNUS_USERS=$HOME/.hymnus_data/users
```
You can add the following lines to `.bashrc`
```
HYMNUS_ROOT=$HOME/.hymnus_env
HYMNUS_DB=$HOME/.hymnus_data/tables.db
HYMNUS_FS=$HOME/.hymnus_data/files
HYMNUS_USERS=$HOME/.hymnus_data/users
```

## 2. Run the installation script
In `setup` directory, run
```
./init.sh

# Or, if you want to override existing files, run
./init.sh -f
```

## 3. Create Python3 virtual env
In this directory, run `./create-python-env.sh`, then
```
cd $HYMNUS_ROOT
source bin/activate
pip3 install -r requirements.txt
```
Alternatively, you can customize the root path where your app is running by creating the virtual env manually.

You can start the server to test if everything went well, just make sure all the environment variables mentioned above are assigned with the correct value.
```
bin/flask --app hymnus run --debug --host=0.0.0.0
```
You can also run the app in the background:
```
nohup bin/flask --app hymnus run --debug --host=0.0.0.0 > log.txt 2>&1 &
```
