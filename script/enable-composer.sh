#!/bin/bash

if [ -z "${DATAPATH}" ]; then
  DATAPATH="blob"
fi
DBFILE="${DATAPATH}/tables.db"

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


HIDE="N"
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
    --unlist)
      HIDE="Y"
      shift # past argument
      ;;
    --disable)
      HIDE="Y"
      shift # past argument
      ;;
    --hide)
      HIDE="Y"
      shift # past argument
      ;;
    --enable)
      HIDE="N"
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

if [[ "${HIDE}" == "Y" ]]; then
sqlite3 "${DBFILE}" <<EOF
UPDATE composers
SET listed = 0
WHERE code = '${CODE}';
EOF

else

sqlite3 "${DBFILE}" <<EOF
UPDATE composers
SET listed = 1
WHERE code = '${CODE}';
EOF

fi