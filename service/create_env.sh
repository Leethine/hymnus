#!/bin/bash
mkdir hymnus_env
mkdir hymnus_env/templates
cp *.py hymnus_env/
cp requirements.txt hymnus_env/
cp templates/*.html hymnus_env/templates

cd hymnus_env
python3 -m venv ./

#flask --app hymnus_app run --debug --host=0.0.0.0