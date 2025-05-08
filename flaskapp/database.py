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

def getComposerRowFromCode(composer_code: str):
  QUERY_COUNT = f"SELECT COUNT(*) FROM Composers WHERE code = '{composer_code}';"
  QUERY = f"SELECT * FROM Composers WHERE code = '{composer_code}'"
  count = queryDB(QUERY_COUNT).fetchone()[0]
  if count == 0:
    return f"<b><i>{composer_code} does not exist!!!!</i></b>"
  else:
    res = queryDB(QUERY).fetchone()
    composer = {}
    for k in res.keys():
      composer[k] = str(res[k])  
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

def getComposerCodeNameMap(jsonpath=""):
  QUERY_COUNT = "SELECT COUNT(*) FROM Composers;"
  QUERY = """
    SELECT code, knownas_name FROM Composers
    WHERE code != 'zzz_unknown'
    ORDER BY code ASC;
  """
  count = queryDB(QUERY_COUNT).fetchone()[0]
  composers = []
  if count > 0:
    for row in queryDB(QUERY).fetchall():
      c = {}
      c["code"] = row["code"]
      c["name"] = unidecode(row["knownas_name"])
      composers.append(c)
  if jsonpath == "":
    return composers
  else:
    with open(jsonpath) as j:
      json.dump(composers)
    return json.dumps(composers)

def pieceExists(folder_hash: str):
  QUERY = f"SELECT COUNT(*) FROM Pieces WHERE folder_hash = '{folder_hash}';"
  count = queryDB(QUERY).fetchone()[0]
  if count == 1:
    return True
  else:
    return False

def getPieceRowFromHash(folder_hash: str):
  if not pieceExists(folder_hash):
    return {}
  else:
    QUERY = f"SELECT * FROM Pieces WHERE folder_hash = '{folder_hash}';"
    row = queryDB(QUERY).fetchone()
    piece = {}
    for k in row.keys():
      piece[k] = row[k]
    return piece

def collectionExists(collection_code: str):
  QUERY = f"SELECT COUNT(*) FROM Collections WHERE code = '{collection_code}';"
  count = queryDB(QUERY).fetchone()[0]
  if count == 1:
    return True
  else:
    return False

def getCollectionRowFromCode(collection_code: str):
  if not collectionExists(collection_code):
    return {}
  else:
    QUERY = f"SELECT * FROM Collections WHERE code = '{collection_code}';"
    row = queryDB(QUERY).fetchone()
    collection = {}
    for k in row.keys():
      collection[k] = row[k]
    return collection

def getCollectionPieces(collection_code: str):
  if not collectionExists(collection_code):
    return []
  else:
    QUERY = f"SELECT * FROM Pieces WHERE collection_code = '{collection_code}'"
    QUERY += " ORDER by Title;"
    collection = []
    for row in queryDB(QUERY).fetchall():
      piece = {}
      for k in row.keys():
        piece[k] = row[k]
      collection.append(piece)
    return collection
