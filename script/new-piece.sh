#/bin/bash

if [ -z "${DATAPATH}" ]; then
  DATAPATH="blob"
fi
DBFILE="${DATAPATH}/tables.db"
FSPATH="${DATAPATH}/files"

# Define functions
create_path_with_hash() {
  FOLDERHASH="${1}"
  INITIAL=${FOLDERHASH:0:2}
  FOLDERPATH="${FSPATH}/${INITIAL}/${FOLDERHASH}"
  mkdir -p "${FOLDERPATH}"
}

update_value_in_db() {
  FOLDERHASH="${1}"
  FIELD="${2}"
  VALUE="${3}"
  if [ ! -z "${VALUE}" ]; then
sqlite3 -csv "${DBFILE}" <<EOF
  UPDATE pieces
  SET ${FIELD} = '${VALUE}'
  WHERE folder_hash = '${FOLDERHASH}';
EOF
  fi
}

# Process arguments
ARRANGED=0
while [[ $# -gt 0 ]]; do
  case ${1} in
    --title)
      TITLE="${2}"
      shift # past argument
      shift # past value
      ;;
    --subtitle)
      SUBTITLE="${2}"
      shift # past argument
      shift # past value
      ;;
    --subsubtitle)
      SUBSUBTITLE="${2}"
      shift # past argument
      shift # past value
      ;;
    --dedicated)
      DECICATED="${2}"
      shift # past argument
      shift # past value
      ;;
    --composer-code)
      COMPOSER_CODE="${2}"
      shift # past argument
      shift # past value
      ;;
    --arranger-code)
      ARRANGER_CODE="${2}"
      shift # past argument
      shift # past value
      ;;
    --collection-code)
      COLLECTION_CODE="${2}"
      shift # past argument
      shift # past value
      ;;
    --opus)
      OPUS="${2}"
      shift # past argument
      shift # past value
      ;;
    --instruments)
      INSTRUMENTS="${2}"
      shift # past argument
      shift # past value
      ;;
    --comment)
      COMMENT="${2}"
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


# Check input arguments, only one argument should be used
if [[ -z "${TITLE}" || -z "${COMPOSER_CODE}" ]]; then
  echo "Must provide at least TITLE and COMPOSER_CODE"
  exit 1
fi

if [ ! -z "${ARRANGER_CODE}" ]; then
  ARRANGED=1
fi

# Check duplicity
FOUND="$(sqlite3 -readonly -csv "${DBFILE}" <<EOF
  SELECT * FROM pieces WHERE
  composer_code = '${COMPOSER_CODE}' AND
  title = '${TITLE}' AND
  subtitle = '${SUBTITLE}' AND
  opus = '${OPUS}' ;
EOF
)"
if [[ ! -z "${FOUND}" ]]; then
  echo "Duplicated piece found:"
  echo "${FOUND}"
  exit 1
fi

# Check composer
COMPOSER="$(sqlite3 -readonly -csv "${DBFILE}" <<EOF
  SELECT knownas_name FROM composers
  WHERE code = '${COMPOSER_CODE}';
EOF
)"

if [ ! -z ${ARRANGER_CODE} ]; then
ARRANGER="$(sqlite3 -readonly -csv "${DBFILE}" <<EOF
  SELECT knownas_name FROM composers
  WHERE code = '${ARRANGER_CODE}';
EOF
)"
fi

if [ ! -z ${COLLECTION_CODE} ]; then
COLLECTION="$(sqlite3 -readonly -csv "${DBFILE}" <<EOF
  SELECT title FROM collections
  WHERE code = '${COLLECTION_CODE}';
EOF
)"
fi

# Exit if composer check failed
if [ -z "${COMPOSER}" ]; then
  echo "${COMPOSER_CODE} is not a valid composer"
  exit 1
elif [[ ${ARRANGED} -eq 1 && -z "${ARRANGER}" ]]; then
  echo "${ARRANGER_CODE} is not a valid arranger"
  exit 1
elif [[ ! -z "${COLLECTION_CODE}" && -z "${COLLECTION}" ]]; then
  echo "${COLLECTION_CODE} is not a valid collection"
  exit 1
fi

# Calculate hash
SHA1HASH="$(echo "${COMPOSER}-${TITLE}-${SUBTITLE}-${SUBSUBTITLE}-${OPUS}-${ARRANGED}-${COLLECTION}" | sha1sum | cut -d ' ' -f 1 )"

# Check hash collision
EXISTING="$(sqlite3 -readonly -csv "${DBFILE}" <<EOF
  SELECT id FROM pieces
  WHERE folder_hash = '${SHA1HASH}';
EOF
)"

if [[ ! -z "${EXISTING}" ]]; then
  echo "MD5 collision detected!"
  echo "The hash was: ${SHA1HASH}"
  exit 1;
fi

# Insert to DB
sqlite3 "${DBFILE}" <<EOF
  INSERT INTO pieces
  (title,arranged,composer_code,folder_hash)
  VALUES('${TITLE}',${ARRANGED},'${COMPOSER_CODE}','${SHA1HASH}');
EOF

# Insert other fields
update_value_in_db ${SHA1HASH} subtitle "${SUBTITLE}"
update_value_in_db ${SHA1HASH} subsubtitle "${SUBSUBTITLE}"
update_value_in_db ${SHA1HASH} opus "${OPUS}"
update_value_in_db ${SHA1HASH} arranger_code "${ARRANGER_CODE}"
update_value_in_db ${SHA1HASH} collection_code "${COLLECTION_CODE}"
update_value_in_db ${SHA1HASH} instrument "${INSTRUMENTS}"
update_value_in_db ${SHA1HASH} dedicated_to "${DEDICATED}"
update_value_in_db ${SHA1HASH} comment "${COMMENT}"

# Create path
create_path_with_hash "${SHA1HASH}"
chmod --recursive a+rwx ${FSPATH}

# Echo
echo "Insertion result:"
echo ""
sqlite3 "${DBFILE}" -readonly -table <<EOF
SELECT * FROM pieces WHERE folder_hash = '${SHA1HASH}';
EOF
