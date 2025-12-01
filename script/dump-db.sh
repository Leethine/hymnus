#!/bin/bash

if [[ -z "${HYMNUS_DATAPATH}" ]] || [[ -f "${HYMNUS_DATAPATH}" ]]; then
  printf "Error: \n Env variable HYMNUS_DATAPATH not correctly set."
  exit 1;
fi
DBFILE="${HYMNUS_DATAPATH}/tables.db"
FSPATH="${HYMNUS_DATAPATH}/files"

OUT_DIR="${HYMNUS_DATAPATH}/datadump"

if [[ ! -z "${1}" && -d "${1}" ]]; then
  OUT_DIR="${1}"
elif [[ ! -z "${1}" && ! -d "${1}" ]]; then
  echo "Invalid directory: ${1}"
fi

if [ ! -d ${OUT_DIR} ]; then
  mkdir -p ${OUT_DIR}
fi


# Dump composer list
#echo "var ascii_converted = 0; var composerlistdata = " > ${OUT_DIR}/composer-data2.js

echo "$(sqlite3 ${DBFILE} -json <<EOF
SELECT * FROM composers;
EOF
)" | sed -e 's/{/\n{/g' | sed -e 's/}/\n}/g' | tee -a ${OUT_DIR}/composerdata2.js &> /dev/null

#echo ";" | tee -a ${OUT_DIR}/composer-data2.js &> /dev/null
#LASTCHAR=$(cat ${OUT_DIR}/composer-data2.js | tr -d '[:blank:]' | tr -d '\n' | tail -c 1)
if [ -f ${OUT_DIR}/composerdata.js ]; then
  rm ${OUT_DIR}/composerdata.json
fi
mv ${OUT_DIR}/composerdata2.json ${OUT_DIR}/composerdata.json


# Dump works
#echo "var ascii_converted = 0; var piecelistdata = " > ${OUT_DIR}/piece-data2.js
echo "$(sqlite3 ${DBFILE} -json  <<EOF
SELECT * FROM pieces;
EOF
)" | sed -e 's/{/\n{/g' | sed -e 's/}/\n}/g' | tee -a ${OUT_DIR}/piecedata2.js &> /dev/null

#echo ";" | tee -a ${OUT_DIR}/piece-data2.js &> /dev/null
if [ -f ${OUT_DIR}/piecedata.js ]; then
  rm ${OUT_DIR}/piecedata.js
fi
mv ${OUT_DIR}/piecedata2.js ${OUT_DIR}/piecedata.js

# Dump collections
#echo "var ascii_converted = 0;  var collectionlistdata = " > ${OUT_DIR}/collection-data2.js
echo "$(sqlite3 ${DBFILE} -json  <<EOF
SELECT * FROM collections;
EOF
)" | sed -e 's/{/\n{/g' | sed -e 's/}/\n}/g' | tee -a ${OUT_DIR}/collection-data2.js &> /dev/null

#echo ";" | tee -a ${OUT_DIR}/collection-data2.js &> /dev/null
if [ -f ${OUT_DIR}/collectiondata.js ]; then
  rm ${OUT_DIR}/collectiondata.js
fi
mv ${OUT_DIR}/collectiondata2.js ${OUT_DIR}/collectiondata.js
