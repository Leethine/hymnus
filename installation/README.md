# Installation Guide

## 1. Create environment variables
You need to add the env variables in your `.bashrc` by running 
```
cat config.env >> $HOME/.bashrc
cd && . .bashrc && cd -
```
This will add the following enironment variables that are needed by the system.
```
HYMNUS_DATAPATH=$HOME/.hymnus_data
HYMNUS_ROOT=$HOME/.hymnus_env
HYMNUS_DB=$HYMNUS_DATAPATH/tables.db
HYMNUS_FS=$HYMNUS_DATAPATH/files
HYMNUS_USERS=$HYMNUS_DATAPATH/users
```

## 2. Run the installation script
In `installation` directory, run
```
./init.sh

# Or, if you don't want user prompt, run
./init-force.sh
```

## 3. Create Python3 virtual env
First run `./create-python-env.sh`, then
```
cd $HYMNUS_ROOT
source bin/activate
pip3 install -r requirements.txt
```
Alternatively, you can customize the root path where your app is running by creating the virtual env manually.

You can start the server to test if everything went well, but before that, you should also make sure all the environment variables as shown above are assigned with the correct value.
```
bin/flask --app hymnus run --debug --host=0.0.0.0
```
You can also run the app in the background:
```
nohup bin/flask --app hymnus run --debug --host=0.0.0.0 > log.txt 2>&1 &
```
