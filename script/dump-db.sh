#!/bin/bash

if [ -z "${DATAPATH}" ]; then
  DATAPATH="blob"
fi
DBFILE="${DATAPATH}/tables.db"
OUT_DIR="${DATAPATH}/datadump"

if [[ ! -z "${1}" && -d "${1}" ]]; then
  OUT_DIR="${1}"
elif [[ ! -z "${1}" && ! -d "${1}" ]]; then
  echo "Invalid directory: ${1}"
fi

if [ ! -d ${OUT_DIR} ]; then
  mkdir -p ${OUT_DIR}
fi

# Dump composer list
echo "var composerlistdata = " > ${OUT_DIR}/composer-data2.js

echo $(sqlite3 ${DBFILE} -json  <<EOF
SELECT 
id,code,firstname,lastname,knownas_name,knownas_name as fullname_ascii,bornyear,diedyear
FROM composers;
EOF
) | sed -e 's/{/\n{/g' | sed -e 's/}/\n}/g' | tee -a ${OUT_DIR}/composer-data2.js &> /dev/null

if [ -f ${OUT_DIR}/composer-data.js ]; then
  rm ${OUT_DIR}/composer-data.js
fi
mv ${OUT_DIR}/composer-data2.js ${OUT_DIR}/composer-data.js

# Dump works
#TODO

# Dump collections
#TODO