#!/bin/bash

if [ -z "${DATAPATH}" ]; then
  DATAPATH="blob"
fi
DBFILE="${DATAPATH}/tables.db"
FSPATH="${DATAPATH}/files"
SQL_SCRIPT="installation/schema.sql"

# Check if parent path exists
if [ ! -d "${DATAPATH}" ]; then
  printf "Error: \n Parent directory does not exist: ${DATAPATH}\n"
  exit 1;
fi

# Check if file or directory already exists
if [[ -f "${FSPATH}" || -d "${FSPATH}" ]]; then
  rm -fr "${FSPATH}"
  mkdir -p "${FSPATH}"
  chmod --recursive a+rwx ${FSPATH}
else
  mkdir -p "${FSPATH}"
fi

if [[ -f "${DBFILE}" || -d "${DBFILE}" ]]; then
  rm ${DBFILE}
fi

# Create SQL schema
sqlite3 "${DBFILE}" <<EOF
  $(cat ${SQL_SCRIPT})
EOF

# Create filesystem's subdirectories by sha-1 hash
IGNORE='mkdir -p "${FSPATH}"
for i in {0..9}{a..f}; do
  mkdir "${FSPATH}/${i}"
done
for i in {a..f}{0..9}; do
  mkdir "${FSPATH}/${i}"
done
chmod --recursive a+rwx ${FSPATH}
'

echo "DB created at: ${DBFILE}"
echo "File storage created at: ${FSPATH}"
