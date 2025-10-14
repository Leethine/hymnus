#!/bin/bash

################################
# Export to static HTML pages  #
################################

if [[ "${1}" == "-h" ]] || [[ "${1}" == "--help" ]]; then
  echo "Usage:"
  echo "./export_static_pages.sh ABSPATH_OF_FLASK_ENV IPADDRESS_OF_FLASKAPP"
fi

if [[ -z "${1}" ]] || [[ ! -d "${1}" ]]; then
echo "You must provide the path to hymnus running environment!"
exit 1
fi

RUNNINGPATH="${1}"

cd "${RUNNINGPATH}"
if [[ -d "exported" ]] || [[ -f "exported" ]]; then
  rm --fr exported
fi

python3 export.py --ip "${2}"

## TODO move to /var/www/
