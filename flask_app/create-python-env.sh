#!/bin/bash

if [[ -z "${HYMNUS_ROOT}" ]]; then
  HYMNUS_ROOT="$HOME/.hymnus_env"
fi

rm -fr ${HYMNUS_ROOT}
mkdir -p ${HYMNUS_ROOT}
cp requirements.txt ${HYMNUS_ROOT}
cp -r ../webapp ${HYMNUS_ROOT}

cd ${HYMNUS_ROOT}
python3 -m venv ./