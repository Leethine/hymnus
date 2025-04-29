#!/bin/bash

DBFILE="blob/tables.db"
OUT_DIR="datadump"

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
) | sed -e 's/{/\n{/g' | sed -e 's/}/\n}/g' | tee -a ${OUT_DIR}/composer-data2.js

if [ -f ${OUT_DIR}/composer-data.js ]; then
  rm ${OUT_DIR}/composer-data.js
fi
mv ${OUT_DIR}/composer-data2.js ${OUT_DIR}/composer-data.js

# Dump composer list