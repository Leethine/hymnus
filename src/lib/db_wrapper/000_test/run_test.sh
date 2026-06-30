#!/bin/bash

assert() {
  local condition="[[ ${1} ]]"
  if ! eval "$condition"; then
    echo "[ERROR] Assertion failed!" >&2
    echo "[DBG] Failed on condition: $condition" >&2
    exit 1
  else
    echo "[PASSED]"
  fi
}

g++ -std=c++17 test_count.cpp ../sqlite3_interface.o -lsqlite3 -o test_count
g++ -std=c++17 test_read.cpp ../sqlite3_interface.o -lsqlite3 -o test_read
g++ -std=c++17 test_write.cpp ../sqlite3_interface.o -lsqlite3 -o test_write
g++ -std=c++17 test_concurrency.cpp ../sqlite3_interface.o -lsqlite3 -o test_concurrency

rm -f test.db
sqlite3 test.db < test_table.sql

# Run the test
export HYMNUS_DB="$PWD/test.db"

echo "TEST CASE 1"
./test_write 1
./test_write 2
COUNT=$(./test_count)
assert "$COUNT == 2"
./test_write del

echo ""
echo "TEST CASE 2"
echo ">> Inserting rows ranging from 1 to 9..."
for i in {1..9}; do
  ./test_write $i
done
echo ">> Displaying all rows:"
./test_read all
echo ">> Displaying rows first page (3 rows per page):"
./test_read all 0 3
echo ">> Displaying rows second page (3 rows per page):"
./test_read all 1 3
echo ">> Displaying rows third page (3 rows per page):"
./test_read all 2 3
echo "[MSG] CHECK WITH YOUR EYES."

echo ""
echo "TEST CASE 3"
echo "Simulating multi-user activities..."
./test_write del
./test_concurrency
COUNT=$(./test_count)
assert "$COUNT == 1000"
./test_write del

# Clean up
rm test_count test_write test_read test_concurrency test.db