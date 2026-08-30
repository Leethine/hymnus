#!/bin/sh

rm -f test.db

SQL_SCRIPT="../setup/schema.sql"

sqlite3 test.db <<EOF
$(cat ${SQL_SCRIPT})
EOF

rm -fr test_fs
mkdir test_fs