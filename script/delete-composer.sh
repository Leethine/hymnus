#!/bin/bash

if [[ -z "${HYMNUS_DATAPATH}" ]] || [[ -f "${HYMNUS_DATAPATH}" ]]; then
  printf "Error: \n Env variable HYMNUS_DATAPATH not correctly set."
  exit 1;
fi
DBFILE="${HYMNUS_DATAPATH}/tables.db"
FSPATH="${HYMNUS_DATAPATH}/files"

find_composer_code_by() {
  FIELD=${1}
  VALUE=${2}
EXISTING="$(sqlite3 -readonly -csv "${DBFILE}" <<EOF
SELECT code FROM composers
WHERE ${FIELD} = '${VALUE}';
EOF
)"
  echo ${EXISTING}
}

while [[ $# -gt 0 ]]; do
  case ${1} in
    --code)
      COMPOSERCODE="${2}"
      shift # past argument
      shift # past value
      ;;
    --full-name)
      KNOWNAS_NAME="${2}"
      shift # past argument
      shift # past value
      ;;
    --force)
      FORCE="Y"
      shift # past argument
      ;;
    -*|--*)
      echo "Unknown option ${1}"
      exit 1
      ;;
    *)
      POSITIONAL_ARGS+=("${1}") # save positional arg
      shift # past argument
      ;;
  esac
done

set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters

if [[ -z "${COMPOSERCODE}" && -z "${KNOWNAS_NAME}" ]]; then
  echo "Please provide at least composer's code or full name."
  exit 1
fi

# Check if exists
if [ ! -z "${COMPOSERCODE}" ]; then
  CODE=$(find_composer_code_by code "${COMPOSERCODE}")
elif [ ! -z "${KNOWNAS_NAME}" ]; then
  CODE=$(find_composer_code_by knownas_name "${KNOWNAS_NAME}")
fi

if [ -z "${CODE}" ]; then
  echo "Composer does not exist:"
  echo "CODE: ${COMPOSERCODE}, Full Name: ${KNOWNAS_NAME}"
  exit 1
fi

FULLNAME="$(sqlite3 -readonly -csv "${DBFILE}" <<EOF
SELECT knownas_name FROM composers
WHERE code = '${CODE}';
EOF
)"

# Confirm with user
if [ -z ${FORCE} ]; then
  echo "To be deleted: ${FULLNAME}"
  read -p "Delete? [y/N]:" CONFIRM
else
  CONFIRM="y"
fi

# Delete after confirmation
if [[ ${CONFIRM} != "y" ]]; then
  echo "Abandoned."
  exit 0
else

# Delete folders related to composer
PIECES="$(sqlite3 -readonly -csv "${DBFILE}" <<EOF
.separator , ,
SELECT folder_hash FROM pieces
WHERE composer_code = '${CODE}';
EOF
)"

for FOLDERHASH in ${PIECES//,/ }; do
  script/delete-piece.sh ${FOLDERHASH} --force
done

COLLECTIONS="$(sqlite3 -csv "${DBFILE}" <<EOF
SELECT title FROM collections
WHERE composer_code = '${CODE}';
EOF
)"

# Delete collections from DB
sqlite3 -csv "${DBFILE}" <<EOF
DELETE FROM collections
WHERE composer_code = '${CODE}';
EOF

echo "Deleted collections: ${COLLECTIONS}"

# Delete composer from DB
sqlite3 -csv "${DBFILE}" <<EOF
DELETE FROM composers
WHERE code = '${CODE}';
EOF

echo "Composer deleted: ${FULLNAME},${CODE}"
fi
