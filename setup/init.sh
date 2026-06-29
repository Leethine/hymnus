#!/bin/bash

SQL_SCRIPT="schema_sqlite3.sql"

if [[ "${1}" == "--force" ]] || [[ "${1}" == "-f" ]] ; then
  FORCE="y"
fi

# Check if path exists
if [[ -z "${HYMNUS_DB}" ]] ; then
  printf "Error: \n Env variable HYMNUS_DB not set."
  exit 1;
fi

if [[ -z "${HYMNUS_FS}" ]] ; then
  printf "Error: \n Env variable HYMNUS_FS not set."
  exit 1;
fi

if [[ -z "${HYMNUS_USERS}" ]] ; then
  printf "Error: \n Env variable HYMNUS_USERS not set."
  exit 1;
fi

# Check if file or directory already exists
if [[ -f "${HYMNUS_FS}" || -d "${HYMNUS_FS}" ]]; then
  if [[ "${FORCE}" != "y" ]] ; then
    printf "Path already exists:\n ${FSPATH}\n"
    read -p "Override? [y/N]: " CONFIRM
  else
    CONFIRM="y"
  fi
  if [[ "${CONFIRM}" != "y" ]]; then
    echo "Abandoned."
    exit 0;
  else
    rm -fr "${HYMNUS_FS}"
    mkdir -p "${HYMNUS_FS}"
  fi
else
  mkdir -p "${HYMNUS_FS}"
fi
CONFIRM="n"

# Check if file or directory already exists
if [[ -f "${HYMNUS_USERS}" || -d "${HYMNUS_USERS}" ]]; then
  if [[ "${FORCE}" != "y" ]] ; then
    printf "Path already exists:\n ${HYMNUS_USERS}\n"
    read -p "Override? [y/N]: " CONFIRM
  else
    CONFIRM="y"
  fi
  if [[ "${CONFIRM}" != "y" ]]; then
    echo "Abandoned."
    exit 0;
  else
    rm -fr "${HYMNUS_USERS}"
    mkdir -p "${HYMNUS_USERS}"
  fi
else
  mkdir -p "${HYMNUS_USERS}"
fi
CONFIRM="n"

if [[ -f "${HYMNUS_DB}" || -d "${HYMNUS_DB}" ]]; then
  if [[ "${FORCE}" != "y" ]] ; then
    printf "Path already exists:\n ${HYMNUS_DB}\n"
    read -p "Override? [y/N]: " CONFIRM
  else
    CONFIRM="y"
  fi
  if [[ "${CONFIRM}" != "y" ]]; then
    echo "Abandoned."
    exit 0;
  else
    rm -fr ${HYMNUS_DB}
  fi
fi

# Create SQL schema
sqlite3 "${HYMNUS_DB}" <<EOF
$(cat ${SQL_SCRIPT})
EOF

# Create filesystem's subdirectories by sha-1 hash
chmod --recursive a+rwx ${HYMNUS_FS}
_='mkdir -p "${FSPATH}"
for i in {0..9}{a..f}; do
  mkdir "${FSPATH}/${i}"
done
for i in {a..f}{0..9}; do
  mkdir "${FSPATH}/${i}"
done
chmod --recursive a+rwx ${FSPATH}
'

echo "DB created at: ${HYMNUS_DB}"
echo "File storage created at: ${HYMNUS_FS}"
echo "User auth created at: ${HYMNUS_USERS}"