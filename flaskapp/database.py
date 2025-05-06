import sqlite3
from unidecode import unidecode
import json

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

def getComposerCodeNameMap(jsonpath="tempdata.js"):
  QUERY_COUNT = "SELECT count(*) FROM Composers;"
  QUERY = """
    SELECT code, knownas_name FROM Composers
    WHERE code != 'zzz_unknown' AND code != 'zzz_various'
    ORDER BY code ASC;
  """
  count = queryDB(QUERY_COUNT).fetchone()[0]
  if count == 0:
    return {}
  else:
    composers = []
    for row in queryDB(QUERY).fetchall():
      c = {}
      c["code"] = row["code"]
      c["name"] = unidecode(row["knownas_name"])
      composers.append(c)
    return json.dumps(composers)
