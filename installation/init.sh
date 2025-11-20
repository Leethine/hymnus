#!/bin/bash

if [ -z "${HYMNUS_DATAPATH}" ]; then
  HYMNUS_DATAPATH="$HOME/.hymnus_data"
fi
DBFILE="${HYMNUS_DATAPATH}/tables.db"
FSPATH="${HYMNUS_DATAPATH}/files"
USRPATH="${HYMNUS_DATAPATH}/users"
SQL_SCRIPT="schema.sql"

# Check if parent path exists
if [[ -z "${HYMNUS_DATAPATH}" ]] || [[ -f "${HYMNUS_DATAPATH}" ]]; then
  printf "Error: \n Env variable HYMNUS_DATAPATH not set, or invalid path."
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
else
  mkdir -p "${FSPATH}"
fi

# Check if file or directory already exists
if [[ -f "${USRPATH}" || -d "${USRPATH}" ]]; then
  printf "User path already exists:\n ${USRPATH}\n"
  read -p "Override? [y/N]: " CONFIRM
  if [[ ${CONFIRM} != "y" ]]; then
    echo "Abandoned."
    exit 0;
  else
    rm -fr "${USRPATH}"
    mkdir -p "${USRPATH}"
  fi
else
  mkdir -p "${USRPATH}"
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
