#!/usr/bin/bash

# Temporary solution
TEMPFILE=${1}
DBPATH="/var/sanctus_db"
CONTENTPATH="${DBPATH}/collection"

if [ -z ${TEMPFILE} ]; then
  exit 0;
fi

cd ${CONTENTPATH}

HASH=$(sha1sum ${TEMPFILE} | cut -d ' ' -f 1)
SHORTHASH=$(sha1sum ${TEMPFILE} | cut -d ' ' -f 1 | cut -c 1-6)
TITLE=$(head -n 1 ${TEMPFILE} | cut -d ' ' -f 1 | tr '[:upper:]' '[:lower:]')

TITLECODE="${TITLE}_${SHORTHASH}"
echo ${HASH} >> ${TEMPFILE};

mv ${TEMPFILE} "${TITLECODE}.cat"
