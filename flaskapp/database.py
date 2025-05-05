import sqlite3

DB_FILE = "/home/lizian/Projects/hymnus/blob/tables.db"

def queryDB(query: str, dbpath=DB_FILE):
  con = sqlite3.connect(dbpath)
  con.create_function("strrev", 1, lambda s: s[::-1])
  con.row_factory = sqlite3.Row

  cur = con.cursor()
  res = cur.execute(query)
  return res

def getComposerDataFromCode(composer_code: str):
  QUERY_COUNT = f"SELECT count(*) FROM Composers WHERE code = '{composer_code}';"
  QUERY = f"SELECT * FROM Composers WHERE code = '{composer_code}'"
  count = queryDB(QUERY_COUNT).fetchone()[0]
  if count == 0:
    return f"<b><i>{composer_code} does not exist!!!!</i></b>"
  else:
    res = queryDB(QUERY).fetchone()
    composer = {}
    composer["id"] = res["id"]
    composer["code"] = res["code"]
    composer["firstname"] = res["firstname"]
    composer["lastname"] = res["lastname"]
    composer["knownas_name"] = res["knownas_name"]
    composer["bornyear"] = res["bornyear"]
    composer["diedyear"] = res["diedyear"]
    return composer
