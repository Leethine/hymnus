#!/bin/bash

if [[ -z "${HYMNUS_DATAPATH}" ]] || [[ -f "${HYMNUS_DATAPATH}" ]]; then
  printf "Error: \n Env variable HYMNUS_DATAPATH not correctly set."
  exit 1;
fi
DBFILE="${HYMNUS_DATAPATH}/tables.db"

convert_to_ascii() {
  RES="$(echo "${1}" | iconv -f UTF8 -t ASCII//TRANSLIT)"
  echo "$RES"
}

ALL_PIECES="$(sqlite3 -csv "${DBFILE}" <<EOF
  SELECT folder_hash FROM pieces;
EOF
)"

for p in $(echo ${ALL_PIECES} | sed 's/ /\n/g'); do
  FOLDER=$(sqlite3 -csv "${DBFILE}" <<EOF
  SELECT folder_hash FROM piece_search WHERE folder_hash = '$p';
EOF
)

if [[ ! -z ${FOLDER} ]]; then
  CONTEXT="$(sqlite3 -csv "${DBFILE}" <<EOF
  SELECT title,subtitle,subsubtitle,dedicated_to FROM pieces WHERE folder_hash = '$p';
EOF
)"
  YEAR="$(sqlite3 -csv "${DBFILE}" <<EOF
  SELECT composed_year FROM pieces WHERE folder_hash = '$p';
EOF
)"
  OPUS="$(sqlite3 -csv "${DBFILE}" <<EOF
  SELECT opus FROM pieces WHERE folder_hash = '$p';
EOF
)"
  INSTRUMENTS="$(sqlite3 -csv "${DBFILE}" <<EOF
  SELECT instruments FROM pieces WHERE folder_hash = '$p';
EOF
)"
  ARRANGERINFO="$(sqlite3 -csv "${DBFILE}" <<EOF
  SELECT arranger_code,arranger_name FROM pieces WHERE folder_hash = '$p';
EOF
)"
  COMPOSER="$(sqlite3 -csv "${DBFILE}" <<EOF
  SELECT firstname || ' ' || lastname || ' ' || knownas_name FROM composers
  INNER JOIN pieces ON pieces.composer_code = composers.code AND pieces.folder_hash = '$p';
EOF
)"

# Insert

sqlite3 "${DBFILE}" <<EOF
  DELETE FROM piece_search WHERE folder_hash = '${p}';
  INSERT INTO piece_search (folder_hash) VALUES ('${p}');
EOF
sqlite3 "${DBFILE}" <<EOF
  UPDATE piece_search
    SET context = '${CONTEXT} ${COMPOSER} $(convert_to_ascii "${CONTEXT} ${COMPOSER}")',
        author  = '${COMPOSER} ${ARRANGERINFO} $(convert_to_ascii "${COMPOSER} ${ARRANGERINFO}")',
        opus    = '${OPUS}',
        composed_year = '${YEAR}',
        instruments   = '${INSTRUMENTS} $(convert_to_ascii "${INSTRUMENTS}")'
    WHERE folder_hash = '${p}';
EOF

fi

done
