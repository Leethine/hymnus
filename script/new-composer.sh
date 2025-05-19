#!/bin/bash

if [ -z "${DATAPATH}" ]; then
  DATAPATH="blob"
fi
DBFILE="${DATAPATH}/tables.db"

firstname="${1}"
lastname="${2}"
knownas_name="${3}"
bornyear="${4}"
diedyear="${5}"
composercode="${6}"

if [[ -z "${firstname}"    || -z "${lastname}" || 
      -z "${knownas_name}" || -z "${bornyear}" || 
      -z "${diedyear}"     || -z "${composercode}" ]]; then
  echo "Missing info, usage:"
  echo '${0} "first name" "last name" "known-as name" bornyear diedyear code'
  exit 1
else

EXISTING="$(sqlite3 -readonly -csv "${DBFILE}" <<EOF
SELECT code FROM composers
WHERE knownas_name = '${knownas_name}'
OR code = '${composercode}';
EOF
)"

if [ ! -z "${EXISTING}" ]; then
  echo "${knownas_name} or ${composercode} already exists in DB."
  exit 1
fi

sqlite3 "${DBFILE}" <<EOF
INSERT INTO composers (code, firstname, lastname, knownas_name, bornyear, diedyear)
VALUES('${composercode}','${firstname}','${lastname}','${knownas_name}','${bornyear}','${diedyear}');
EOF

echo "Insertion result:"
echo ""
sqlite3 "${DBFILE}" -readonly -table <<EOF
SELECT * FROM composers WHERE code = '${composercode}';
EOF

fi
