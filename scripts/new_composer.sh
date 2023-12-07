#!/usr/bin/bash

# Temporary solution
TEMPFILE=${1}
DBPATH="/var/sanctus_db"
CONTENTPATH="${DBPATH}/composer"

if [ -z ${TEMPFILE} ]; then
  exit 0;
fi

cd ${CONTENTPATH}

HASH=$(sha1sum ${TEMPFILE} | cut -d ' ' -f 1)
SHORTHASH=$(sha1sum ${TEMPFILE} | cut -d ' ' -f 1 | cut -c 1-6)
LASTNAME=$(head -n 1 ${TEMPFILE} | grep -o '[^ ]*$' | sed 's/\ //g' | tr '[:upper:]' '[:lower:]')

echo ${HASH} >> ${TEMPFILE};
NAMECODE="${LASTNAME}_${SHORTHASH}"

mv ${TEMPFILE} "${NAMECODE}.cat"
mkdir "${NAMECODE}"
