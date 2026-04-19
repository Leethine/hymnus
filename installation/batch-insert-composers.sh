#!/bin/bash

if [[ -z "${HYMNUS_DB}" ]] || [[ ! -f "${HYMNUS_DB}" ]]; then
  printf "Error: \n Env variable HYMNUS_DB not correctly set."
  exit 1;
fi
#if [[ -z "${HYMNUS_FS}" ]] || [[ ! -d "${HYMNUS_FS}" ]]; then
#  printf "Error: \n Env variable HYMNUS_FS not correctly set."
#  exit 1;
#fi
DBFILE="${HYMNUS_DB}"
#FSPATH="${HYMNUS_FS}"

CSVFILE=${1}

if [[ -z ${CSVFILE} && ! -f ${CSVFILE} ]]; then
  echo "Invalid filename: ${CSVFILE}"
  exit 1
fi

while read -r line; do
  ENABLED="$(echo ${line}      | cut -d ',' -f1)"
  FIRSTNAME="$(echo ${line}    | cut -d ',' -f2)"
  LASTNAME="$(echo ${line}     | cut -d ',' -f3)"
  KNOWNASNAME="$(echo ${line}  | cut -d ',' -f4)"
  BORNYEAR="$(echo ${line}     | cut -d ',' -f5)"
  DIEDYEAR="$(echo ${line}     | cut -d ',' -f6)"
  COMPOSERCODE="$(echo ${line} | cut -d ',' -f7)"

  if [[ ! -z "${FIRSTNAME}" && ! -z "${LASTNAME}" &&
        ! -z "${KNOWNASNAME}" && ! -z "${BORNYEAR}" &&
        ! -z "${DIEDYEAR}" && ! -z "${COMPOSERCODE}" ]]; then

    BOOL_ENABLED="0"
    if [[ "${ENABLED}" == "Y" ]]; then
      BOOL_ENABLED="1"
    fi

# RUN insertion
sqlite3 "${DBFILE}" <<EOF
INSERT INTO composers (code,firstname, lastname, knownas_name, bornyear, diedyear, listed)
VALUES('${COMPOSERCODE}','${FIRSTNAME}','${LASTNAME}','${KNOWNASNAME}','${BORNYEAR}','${DIEDYEAR}', ${BOOL_ENABLED});
EOF

  else
    echo "Ignore line:"
    printf "${FIRSTNAME},${LASTNAME},${KNOWNASNAME},${BORNYEAR},${DIEDYEAR},${COMPOSERCODE}"
  fi

done < ${CSVFILE}

# Delete header
sqlite3 "${DBFILE}" <<EOF
DELETE FROM composers WHERE
code = 'code';
EOF

echo "Done batch insert composers."
