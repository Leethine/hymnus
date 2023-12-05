#!/usr/bin/bash

DBPATH="/var/sanctus_db"

mkdir ${DBPATH}
cd ${DBPATH}
mkdir -p "${DBPATH}/composer"
mkdir -p "${DBPATH}/collection"
mkdir -p "${DBPATH}/score"

# Create subdirectories for score sha-1 hash
cd "${DBPATH}/score"

for i in {0..9}{a..f}; do
  mkdir ${i}
done

for i in {a..f}{0..9}; do
  mkdir ${i}
done

cd ${DBPATH}
chmod --recursive a+rwx ${DBPATH}
