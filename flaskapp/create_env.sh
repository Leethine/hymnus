#!/bin/bash

BACKEND_DIR=hymnus_env
if [ ! -z ${1} ]; then 
  BACKEND_DIR=${1}
fi

rm -fr ${BACKEND_DIR}
mkdir ${BACKEND_DIR} ${BACKEND_DIR}/templates ${BACKEND_DIR}/static
cp *.py ${BACKEND_DIR}/
cp config.env ${BACKEND_DIR}/
cp requirements.txt ${BACKEND_DIR}/
cp templates/*.html ${BACKEND_DIR}/templates
cp static/*.js ${BACKEND_DIR}/static

cd ${BACKEND_DIR}
python3 -m venv ./
#cp ../start bin
#chmod 777 bin/start

# cd hymnus_env && source bin/activate && bin/start