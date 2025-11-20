#!/bin/bash

if [[ -z "${HYMNUS_DATAPATH}" ]] || [[ -f "${HYMNUS_DATAPATH}" ]]; then
  printf "Error: \n Env variable HYMNUS_DATAPATH not correctly set."
  exit 1;
fi
DBFILE="${HYMNUS_DATAPATH}/tables.db"
FSPATH="${HYMNUS_DATAPATH}/files"


COLLECTION_CODE="${1}"
FORCE="${2}"

EXISTING="$(sqlite3 -readonly -csv "${DBFILE}" <<EOF
  SELECT code FROM collections WHERE
  code = '${COLLECTION_CODE}';
EOF
)"

if [ ! -z "${EXISTING}" ]; then

  if [ -z "${FORCE}" ]; then 
    read -p "Delete collection from DB? [y/N]:" CONFIRM
  else
    CONFIRM="y"
  fi

  # Delete from DB
  if [[ ${CONFIRM} != "y" ]]; then
    echo "Abandoned."
    exit 0

  else

sqlite3 -csv "${DBFILE}" <<EOF
  DELETE FROM collections WHERE
  code = '${COLLECTION_CODE}';
EOF
  echo "Deleted collection ${COLLECTION_CODE} from DB."
  fi

else
  echo "No matching piece found: ${COLLECTION_CODE}"
fi
