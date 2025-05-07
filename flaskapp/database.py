import sqlite3, os
from unidecode import unidecode
import json

HYMNUS_DB = ""
HYMNUS_FS = ""

if 'HYMNUS_DB' in os.environ.keys():
  HYMNUS_DB = os.environ['HYMNUS_DB']

if 'HYMNUS_FS' in os.environ.keys():
  HYMNUS_FS = os.environ['HYMNUS_FS']

def queryDB(query: str, dbpath=HYMNUS_DB):
  con = sqlite3.connect(dbpath)
  con.create_function("strrev", 1, lambda s: s[::-1])
  con.row_factory = sqlite3.Row

  cur = con.cursor()
  res = cur.execute(query)
  return res

def getComposerDataFromCode(composer_code: str):
  QUERY_COUNT = f"SELECT COUNT(*) FROM Composers WHERE code = '{composer_code}';"
  QUERY = f"SELECT * FROM Composers WHERE code = '{composer_code}'"
  count = queryDB(QUERY_COUNT).fetchone()[0]
  if count == 0:
    return f"<b><i>{composer_code} does not exist!!!!</i></b>"
  else:
    res = queryDB(QUERY).fetchone()
    composer = {}
    composer["code"] = res["code"]
    composer["firstname"] = res["firstname"]
    composer["lastname"] = res["lastname"]
    composer["knownas_name"] = res["knownas_name"]
    composer["bornyear"] = str(res["bornyear"])
    composer["diedyear"] = str(res["diedyear"])
    composer["wiki"] = res["wikipedia_url"]
    composer["imslp"] = res["imslp_url"]
    return composer


def composerHasWorks(composer_code: str):
  QUERY = f"SELECT COUNT(*) FROM Composers WHERE code = '{composer_code}';"
  count = queryDB(QUERY).fetchone()[0]
  if count == 0:
    return False
  else:
    QUERY = f"SELECT count(*) FROM Pieces WHERE composer_code = '{composer_code}';"
    count = queryDB(QUERY).fetchone()[0]
    if count > 0:
      return True
    else:
      return False
  return False

def getComposerCodeNameMap(jsonpath="tempdata.js"):
  QUERY_COUNT = "SELECT COUNT(*) FROM Composers;"
  QUERY = """
    SELECT code, knownas_name FROM Composers
    WHERE code != 'zzz_unknown'
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

def pieceExists(folder_hash: str):
  QUERY = f"SELECT COUNT(*) FROM Pieces WHERE folder_hash = '{folder_hash}';"
  count = queryDB(QUERY).fetchone()[0]
  if count == 1:
    return True
  else:
    return False

def getPieceDataFromHash(folder_hash: str):
  if not pieceExists(folder_hash):
    return {}
  else:
    QUERY = f"SELECT * FROM Pieces WHERE folder_hash = '{folder_hash}'"
    row = queryDB(QUERY).fetchone()
    piece = {}
    piece["composer_code"] = row["composer_code"]
    piece["arranged"] = str(int(row["arranged"]))
    piece["arranger_code"] = row["arranger_code"]
    piece["collection_code"] = row["collection_code"]
    piece["title"] = row["title"]
    piece["subtitle"] = row["subtitle"]
    piece["subsubtitle"] = row["subsubtitle"]
    piece["dedicated_to"] = row["dedicated_to"]
    piece["opus"] = row["opus"]
    piece["instruments"] = row["instruments"]
    piece["hash"] = row["folder_hash"]
    piece["comment"] = row["comment"]
    return piece