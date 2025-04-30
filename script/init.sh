#!/bin/bash

DBPATH="blob"
DBFILE="${DBPATH}/tables.db"
FSPATH="${DBPATH}/files"
SQL_SCRIPT="script/schema.sql"

# Check if parent path exists
if [ ! -d "${DBPATH}" ]; then
  printf "Error: \n Parent directory does not exist: ${DBPATH}\n"
  exit 1;
fi

# Check if file or directory already exists
if [[ -f "${FSPATH}" || -d "${FSPATH}" ]]; then
  printf "Filesystem path already exists:\n ${FSPATH}\n"
  read -p "Override? [y/N]: " CONFIRM
  if [[ ${CONFIRM} != "y" ]]; then
    echo "Abandoned."
    exit 0;
  else
    rm -fr "${FSPATH}"
    mkdir -p "${FSPATH}"
  fi
fi

if [[ -f "${DBFILE}" || -d "${DBFILE}" ]]; then
  printf "DB already exists:\n ${DBFILE}\n"
  read -p "Override? [y/N]: " CONFIRM
  if [[ ${CONFIRM} != "y" ]]; then
    echo "Abandoned."
    exit 0;
  else
    rm ${DBFILE}
  fi
fi

# Create SQL schema
sqlite3 "${DBFILE}" <<EOF
$(cat ${SQL_SCRIPT})
EOF

# Create filesystem's subdirectories by sha-1 hash
chmod --recursive a+rwx ${FSPATH}
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
