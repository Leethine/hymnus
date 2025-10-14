#!/bin/bash

if [ -z "${DATAPATH}" ]; then
  DATAPATH="blob"
fi
DBFILE="${DATAPATH}/tables.db"
FSPATH="${DATAPATH}/files"


while [[ $# -gt 0 ]]; do
  case ${1} in
    --piece)
      PIECE_HASH="${2}"
      shift # past argument
      shift # past value
      ;;
    --collection)
      COLLECTION_CODE="${2}"
      shift # past argument
      shift # past value
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

if [ -z ${PIECE_HASH} ]; then
  echo "Must provide --piece HASH"
  exit 1
fi

if [ -z ${COLLECTION_CODE} ]; then
  echo "Must provide --collection CODE"
  exit 1
fi

COLLECTION_EXIST="$(sqlite3 -readonly -csv "${DBFILE}" <<EOF
  SELECT code FROM collections
  WHERE code = '${COLLECTION_CODE}';
EOF
)"

PIECE_EXIST="$(sqlite3 -readonly -csv "${DBFILE}" <<EOF
  SELECT folder_hash FROM pieces
  WHERE folder_hash = '${PIECE_HASH}';
EOF
)"

if [ -z ${COLLECTION_EXIST} ]; then
  echo "Collection does not exist: ${COLLECTION_EXIST}"
  exit 1
fi

if [ -z ${PIECE_EXIST} ]; then
  echo "Piece does not exist: ${PIECE_EXIST}"
  exit 1
fi

PIECE_BELONGS_TO_COLLECTIONS="$(sqlite3 -readonly -csv "${DBFILE}" <<EOF
  SELECT collection_code FROM pieces
  WHERE folder_hash = '${PIECE_HASH}';
EOF
)"

if [[ -z "${PIECE_BELONGS_TO_COLLECTIONS}" ]]; then
  PIECE_BELONGS_TO_COLLECTIONS=${COLLECTION_CODE}
else
  PIECE_BELONGS_TO_COLLECTIONS="${PIECE_BELONGS_TO_COLLECTIONS}"" ""${COLLECTION_CODE}"
fi

sqlite3 -csv "${DBFILE}" <<EOF
  UPDATE pieces
  SET collection_code = '${PIECE_BELONGS_TO_COLLECTIONS}'
  WHERE folder_hash = '${PIECE_HASH}';
EOF

echo "Update result:"
sqlite3 -readonly -table "${DBFILE}" <<EOF
  select * from pieces
  WHERE folder_hash = '${PIECE_HASH}';
EOF
