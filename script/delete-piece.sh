#/bin/bash

DBFILE="blob/tables.db"
FOLDERHASH="${1}"
FORCE="${2}"
FSPATH="blob/files"

EXISTING="$(sqlite3 -readonly -csv "${DBFILE}" <<EOF
  SELECT id FROM pieces WHERE
  folder_hash = '${FOLDERHASH}';
EOF
)"

if [ ! -z "${EXISTING}" ]; then

  if [ -z "${FORCE}" ]; then 
    read -p "Delete from DB? [y/N]:" CONFIRMDB
  else
    CONFIRMDB="y"
  fi

  # Delete from DB
  if [[ ${CONFIRM} != "y" ]]; then
    echo "Abandoned."
    exit 0

  else

sqlite3 -csv "${DBFILE}" <<EOF
  DELETE FROM pieces WHERE
  folder_hash = '${FOLDERHASH}';
EOF
  echo "Deleted piece ${EXISTING} from DB."
  fi

  # Delete folder
  CONTENT_DIR="${FSPATH}/${FOLDERHASH:0:2}/${FOLDERHASH}"
  if [[ -z "${FORCE}" && -d ${CONTENT_DIR} ]]; then
    echo "Non-empty directory: ${CONTENT_DIR}" 
    read -p "Delete? [y/N]:" CONFIRM
    if [[ ${CONFIRM} != "y" ]]; then
      echo "Abandoned."
      exit 0;
    else
      rm -fr "${CONTENT_DIR}"
      echo "Deleted folder ${CONTENT_DIR}"
    fi
  else
    rm -fr "${CONTENT_DIR}"
    echo "Deleted folder ${CONTENT_DIR}"
  fi
else
  echo "No matching piece found: ${FOLDERHASH}"
fi
