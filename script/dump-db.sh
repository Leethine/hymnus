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
echo "var ascii_converted = 0; var composerlistdata = " > ${OUT_DIR}/composer-data2.js

echo "$(sqlite3 ${DBFILE} -json <<EOF
SELECT 
  id,
  code,
  firstname,
  lastname,
  knownas_name,
  knownas_name as fullname_ascii,
  bornyear,
  diedyear
FROM composers;
EOF
)" | sed -e 's/{/\n{/g' | sed -e 's/}/\n}/g' | tee -a ${OUT_DIR}/composer-data2.js &> /dev/null

echo ";" | tee -a ${OUT_DIR}/composer-data2.js &> /dev/null
#LASTCHAR=$(cat ${OUT_DIR}/composer-data2.js | tr -d '[:blank:]' | tr -d '\n' | tail -c 1)
if [ -f ${OUT_DIR}/composer-data.js ]; then
  rm ${OUT_DIR}/composer-data.js
fi
mv ${OUT_DIR}/composer-data2.js ${OUT_DIR}/composer-data.js


# Dump works
echo "var ascii_converted = 0; var piecelistdata = " > ${OUT_DIR}/piece-data2.js
echo "$(sqlite3 ${DBFILE} -json  <<EOF
SELECT
  id,
  composer_id,
  composer_code,
  arranged,
  arranger_id,
  arranger_code,
  collection_id,
  collection_code,
  title,
  title as title_ascii,
  subtitle,
  subsubtitle,
  dedicated_to,
  opus,
  instrument,
  folder_hash,
  comment
FROM pieces;
EOF
)" | sed -e 's/{/\n{/g' | sed -e 's/}/\n}/g' | tee -a ${OUT_DIR}/piece-data2.js &> /dev/null

echo ";" | tee -a ${OUT_DIR}/piece-data2.js &> /dev/null
if [ -f ${OUT_DIR}/piece-data.js ]; then
  rm ${OUT_DIR}/piece-data.js
fi
mv ${OUT_DIR}/piece-data2.js ${OUT_DIR}/piece-data.js

# Dump collections
echo "var ascii_converted = 0;  var collectionlistdata = " > ${OUT_DIR}/collection-data2.js
echo "$(sqlite3 ${DBFILE} -json  <<EOF
SELECT
  id,
  code,
  title,
  subtitle,
  subsubtitle,
  opus,
  description_text,
  volume,
  composer_id,
  composer_code,
  instruments,
  editor
FROM collections;
EOF
)" | sed -e 's/{/\n{/g' | sed -e 's/}/\n}/g' | tee -a ${OUT_DIR}/collection-data2.js &> /dev/null

echo ";" | tee -a ${OUT_DIR}/collection-data2.js &> /dev/null
if [ -f ${OUT_DIR}/collection-data.js ]; then
  rm ${OUT_DIR}/collection-data.js
fi
mv ${OUT_DIR}/collection-data2.js ${OUT_DIR}/collection-data.js
