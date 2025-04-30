#/bin/bash

if [ -z "${DATAPATH}" ]; then
  DATAPATH="blob"
fi

DBFILE="${DATAPATH}/tables.db"
CSVFILE=${1}

if [[ -z ${CSVFILE} && ! -f ${CSVFILE} ]]; then
  echo "Invalid filename: ${CSVFILE}"
  exit 1
fi

while read -r line; do

  FIRSTNAME="$(echo ${line}    | cut -d ',' -f1)"
  LASTNAME="$(echo ${line}     | cut -d ',' -f2)"
  KNOWNASNAME="$(echo ${line}  | cut -d ',' -f3)"
  BORNYEAR="$(echo ${line}     | cut -d ',' -f4)"
  DIEDYEAR="$(echo ${line}     | cut -d ',' -f5)"
  COMPOSERCODE="$(echo ${line} | cut -d ',' -f6)"

  if [[ ! -z "${FIRSTNAME}" && ! -z "${LASTNAME}" &&
        ! -z "${KNOWNASNAME}" && ! -z "${BORNYEAR}" &&
        ! -z "${DIEDYEAR}" && ! -z "${COMPOSERCODE}" ]]; then
sqlite3 "${DBFILE}" <<EOF
INSERT INTO composers (code,firstname, lastname, knownas_name, bornyear, diedyear)
VALUES('${COMPOSERCODE}','${FIRSTNAME}','${LASTNAME}','${KNOWNASNAME}','${BORNYEAR}','${DIEDYEAR}');
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