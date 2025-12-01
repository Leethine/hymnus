#!/bin/bash

# Check env
if [ -z "${HYMNUS_DATAPATH}" ]; then
  echo "env variable HYMNUS_DATAPATH not defined"
  exit 1
fi
if [ -z "${HYMNUS_DB}" ]; then
  DBFILE="${HYMNUS_DATAPATH}/tables.db"
else
  DBFILE="${HYMNUS_DB}"
fi
if [ -z "${HYMNUS_FS}" ]; then
  FSPATH="${HYMNUS_DATAPATH}/files"
else
  FSPATH="${HYMNUS_FS}"
fi

OPTION="${1}"

if [ "${OPTION}" == "--backup" ]; then
BKUPDATE="$(echo $(date) | tr ' ' '-')"
sqlite3 -json "${DBFILE}" "SELECT * FROM Composers;"   > "${BKUPDATE}_Composers.json"
sqlite3 -json "${DBFILE}" "SELECT * FROM Pieces;"      > "${BKUPDATE}_Pieces.json"
sqlite3 -json "${DBFILE}" "SELECT * FROM Collections;" > "${BKUPDATE}_Collections.json"

elif [ "${OPTION}" == "--restore" ]; then
if [[ ! -z "$(echo "${2}" | grep "Composers")" ]] && [[ ! -z "$(echo "${2}" | grep ".json")" ]]; then
FILENAME="${2}" \
FILETYPE="Composers" \
DBFILE="${DBFILE}" \
python3 recover.py
elif [[ ! -z "$(echo "${2}" | grep "Pieces")" ]] && [[ ! -z "$(echo "${2}" | grep ".json")" ]]; then
FILENAME="${2}" \
FILETYPE="Pieces" \
DBFILE="${DBFILE}" \
python3 recover.py
elif [[ ! -z "$(echo "${2}" | grep "Collections")" ]] && [[ ! -z "$(echo "${2}" | grep ".json")" ]]; then
FILENAME="${2}" \
FILETYPE="Collections" \
DBFILE="${DBFILE}" \
python3 recover.py
else
echo "Recover file name is invalid: ${2}"
exit 1
fi


elif [[ "${OPTION}" == "--help" ]] || [[ "${OPTION}" == "-h" ]]; then
echo "${0} [--backup|--restore] FILE.json"

else
echo "Invalid input."
exit 1
fi
