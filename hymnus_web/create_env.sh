#!/bin/bash

if [[ -z "${HYMNUS_ROOT}" ]]; then
  HYMNUS_ROOT="$HOME/.hymnus_env"
fi

rm -fr ${HYMNUS_ROOT}
cp -r hymnus_web ${HYMNUS_ROOT}

cd ${HYMNUS_ROOT}
python3 -m venv ./
#cp ../start bin
#chmod 777 bin/start

# cd hymnus_env && source bin/activate && bin/start