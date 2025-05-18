#/bin/bash

if [ -z "${DATAPATH}" ]; then
  DATAPATH="blob"
fi
DBFILE="${DATAPATH}/tables.db"
FSPATH="${DATAPATH}/files"

# Define functions
update_value_in_db() {
  COLLECTION_CODE="${1}"
  FIELD="${2}"
  VALUE="${3}"
  if [ ! -z "${VALUE}" ]; then
sqlite3 -csv "${DBFILE}" <<EOF
  UPDATE collections
  SET ${FIELD} = '${VALUE}'
  WHERE code = '${COLLECTION_CODE}';
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
    --composer-code)
      COMPOSER_CODE="${2}"
      shift # past argument
      shift # past value
      ;;
    --editor)
      EDITOR_NAME="${2}"
      shift # past argument
      shift # past value
      ;;
    --opus)
      OPUS="${2}"
      shift # past argument
      shift # past value
      ;;
    --volume)
      VOLUME="${2}"
      shift # past argument
      shift # past value
      ;;
    --instruments)
      INSTRUMENTS="${2}"
      shift # past argument
      shift # past value
      ;;
    --description)
      DESCRIPTION="${2}"
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


# Check input arguments
if [[ -z "${TITLE}" ]]; then
  echo "Must provide at least TITLE"
  exit 1
fi

if [[ -z "${COMPOSER_CODE}" ]]; then
  COMPOSER_CODE="zzz_unknown"
fi

if [[ -z "${VOLUME}" ]]; then
  VOLUME=" "
fi

if [[ -z "${EDITOR_NAME}" ]]; then
  EDITOR_NAME=" "
fi

if [[ -z "${OPUS}" ]]; then
  OPUS=" "
fi

# Check duplicity
FOUND="$(sqlite3 -readonly -csv "${DBFILE}" <<EOF
  SELECT * FROM collections WHERE
  composer_code = '${COMPOSER_CODE}' AND
  title = '${TITLE}' AND
  subtitle = '${SUBTITLE}' AND
  volume = '${VOLUME}' AND
  opus = '${OPUS}' AND
  editor = '${EDITOR_NAME}';
EOF
)"

if [[ ! -z "${FOUND}" ]]; then
  echo "Duplicated collection found:"
  echo "${FOUND}"
  exit 1
fi

# Check composer
if [ ! -z ${COMPOSER_CODE} ]; then
COMPOSER="$(sqlite3 -readonly -csv "${DBFILE}" <<EOF
  SELECT knownas_name FROM composers
  WHERE code = '${COMPOSER_CODE}';
EOF
)"
fi

# Exit if composer check failed
if [[ ! -z "${COMPOSER_CODE}" && -z "${COMPOSER}" ]]; then
  echo "${COMPOSER_CODE} is not a valid composer"
  exit 1
fi

# Calculate hash
MD5HASH="$(echo "${COMPOSER}-${TITLE}-${SUBTITLE}-${SUBSUBTITLE}-${OPUS}-${VOLUME}-${EDITOR_NAME}" | md5sum | cut -d ' ' -f 1 )"

# Check hash collision
EXISTING="$(sqlite3 -readonly -csv "${DBFILE}" <<EOF
  SELECT title FROM collections
  WHERE code = '${MD5HASH}';
EOF
)"

if [[ ! -z "${EXISTING}" ]]; then
  echo "MD5 collision detected!"
  echo "The hash was: ${MD5HASH}"
  exit 1;
fi

# Insert to DB
sqlite3 "${DBFILE}" <<EOF
  INSERT INTO collections
  (title, volume, composer_code, code)
  VALUES('${TITLE}','${VOLUME}','${COMPOSER_CODE}','${MD5HASH}');
EOF

# Insert other fields
update_value_in_db ${MD5HASH} subtitle "${SUBTITLE}"
update_value_in_db ${MD5HASH} subsubtitle "${SUBSUBTITLE}"
update_value_in_db ${MD5HASH} opus "${OPUS}"
update_value_in_db ${MD5HASH} composer_code "${COMPOSER_CODE}"
update_value_in_db ${MD5HASH} editor "${EDITOR_NAME}"
update_value_in_db ${MD5HASH} instruments "${INSTRUMENTS}"
update_value_in_db ${MD5HASH} description_text "${DESCRIPTION}"

# Echo
echo "Insertion result:"
echo ""
sqlite3 "${DBFILE}" -readonly -table <<EOF
SELECT * FROM collections WHERE code = '${MD5HASH}';
EOF
