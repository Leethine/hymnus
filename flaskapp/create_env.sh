#!/bin/bash
rm -fr hymnus_env
mkdir hymnus_env
mkdir hymnus_env/templates
cp *.py hymnus_env/
cp requirements.txt hymnus_env/
cp templates/*.html hymnus_env/templates

cd hymnus_env
python3 -m venv ./

echo "#!/bin/bash" > bin/start
echo "pip install -r requirements.txt" >> bin/start
echo "bin/flask --app hymnus run --debug --host=0.0.0.0" >> bin/start
chmod 777 bin/start
