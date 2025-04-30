#/bin/bash

if [ -z "${DATAPATH}" ]; then
  DATAPATH="blob"
fi
DBFILE="${DATAPATH}/tables.db"

find_composer_id_by() {
  FIELD=${1}
  VALUE=${2}
EXISTING="$(sqlite3 -readonly -csv "${DBFILE}" <<EOF
SELECT id FROM composers
WHERE ${FIELD} = '${VALUE}';
EOF
)"
  echo ${EXISTING}
}

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
    --id)
      COMPOSER_ID="${2}"
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

if [[ -z "${COMPOSERCODE}" && -z "${KNOWNAS_NAME}" && -z "${COMPOSER_ID}" ]]; then
  echo "Please provide at least composer's id, code or full name."
  exit 1
fi

# Check if exists
if [ ! -z "${COMPOSER_ID}" ]; then
  ID=$(find_composer_id_by id "${COMPOSER_ID}")
  CODE=$(find_composer_code_by id "${COMPOSER_ID}")
elif [ ! -z "${COMPOSERCODE}" ]; then
  ID=$(find_composer_id_by code "${COMPOSERCODE}")
  CODE=$(find_composer_code_by code "${COMPOSERCODE}")
elif [ ! -z "${KNOWNAS_NAME}" ]; then
  ID=$(find_composer_id_by knownas_name "${KNOWNAS_NAME}")
  CODE=$(find_composer_code_by knownas_name "${KNOWNAS_NAME}")
fi

if [ -z "${ID}" ]; then
  echo "Composer does not exist:"
  echo "ID:${COMPOSER_ID}, CODE: ${COMPOSERCODE}, Full Name: ${KNOWNAS_NAME}"
  exit 1
fi

FULLNAME="$(sqlite3 -readonly -csv "${DBFILE}" <<EOF
SELECT knownas_name FROM composers
WHERE id = '${ID}';
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
WHERE composer_id = '${ID}' OR composer_code = '${CODE}';
EOF
)"

for FOLDERHASH in ${PIECES//,/ }; do
  script/delete-piece.sh ${FOLDERHASH} --force
done

# Delete collections from DB
sqlite3 -csv "${DBFILE}" <<EOF
DELETE FROM collections
WHERE composer_id = '${ID}' OR composer_code = '${CODE}';
EOF

# Delete composer from DB
sqlite3 -csv "${DBFILE}" <<EOF
DELETE FROM composers
WHERE id = '${ID}' OR code = '${CODE}';
EOF

echo "Composer deleted: ${FULLNAME},${ID},${CODE}"
fi
