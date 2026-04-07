import sys
sys.path.append('../migrate/')

import random, os
from multiprocessing import Process
from db_sqlite import DB_SQLITE

SAMPLE = 1000

os.environ['HYMNUS_DB'] = "test.db"

def makerandomhash():
  digits = []
  for i in range(40):
    digits.append(str(int(random.random() * 10)))
  return ''.join(digits)

# Prepare hashes
hashes1 = []
for i in range(SAMPLE):
  hashes1.append(makerandomhash())

hashes2 = []
for i in range(SAMPLE):
  hashes2.append(makerandomhash())

hashes3 = []
for i in range(SAMPLE):
  hashes3.append(makerandomhash())

def runQuery(folder_hash_list) -> str:
  err = ""
  for folder_hash in folder_hash_list:
    insert_query = f"INSERT INTO Pieces (folder_hash, title) VALUES ('{folder_hash}', 'title');"
    err += DB_SQLITE().updateRows(insert_query)
  return err

def countDBRows():
  count = DB_SQLITE().countRows("SELECT COUNT(*) FROM Pieces;")
  return count

def eraseDB():
  DB_SQLITE().updateRows("DELETE FROM Pieces;")

if __name__ == "__main__":

  eraseDB()

  t1 = Process(target=runQuery, args=(hashes1,))
  t2 = Process(target=runQuery, args=(hashes2,))
  t3 = Process(target=runQuery, args=(hashes3,))

  t1.start()
  t2.start()
  t3.start()
  t1.join()
  t2.join()
  t3.join()

  assert countDBRows() == SAMPLE * 3, f"Expected {SAMPLE * 3} rows, but got {countDBRows()} rows."
  print(f"Test passed: {countDBRows()} rows inserted successfully.")
  eraseDB()
