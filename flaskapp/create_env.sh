#!/bin/bash
rm -fr hymnus_env
mkdir hymnus_env hymnus_env/templates hymnus_env/static
cp *.py hymnus_env/
cp config.env hymnus_env/
cp requirements.txt hymnus_env/
cp templates/*.html hymnus_env/templates
cp static/*.js hymnus_env/static

cd hymnus_env
python3 -m venv ./
cp ../start bin

chmod 777 bin/start

cd hymnus_env && source bin/activate && bin/start