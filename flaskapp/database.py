import sqlite3, os, json
from singleton import SingletonMeta

class Database(metaclass=SingletonMeta):
  """SQLITE database interface and file system operations."""

  def __getDBPath(self, dbpath="") -> str:
    """If no input provided, return DB path in 'HYMNUS_DB' env variable."""
    if dbpath == "" and 'HYMNUS_DB' in os.environ.keys():
      return os.environ['HYMNUS_DB']
    return dbpath

  def __getFSPath(self, fspath="") -> str:
    """If no input provided, return filesystem path in 'HYMNUS_FS' env variable."""
    if fspath == "" and 'HYMNUS_FS' in os.environ.keys():
      return os.environ['HYMNUS_FS']
    return fspath
  
  def getDBPath(self) -> str:
    """Return database path in 'HYMNUS_DB' env variable."""
    if 'HYMNUS_DB' in os.environ.keys():
      return os.environ['HYMNUS_DB']
    return ""
  
  def getFSPath(self) -> str:
    """Return filesystem path in 'HYMNUS_FS' env variable."""
    if 'HYMNUS_FS' in os.environ.keys():
      return os.environ['HYMNUS_FS']
    return ""

  def __basicQueryDB(self, query: str, dbpath=""):
    """Execute SQLITE DB query."""
    con = sqlite3.connect(self.__getDBPath(dbpath))
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    res = cur.execute(query)
    return res

  def __queryDB(self, query: str, dbpath=""):
    """Execute SQLITE DB query with built-in functions."""
    con = sqlite3.connect(self.__getDBPath(dbpath))
    # Add built-in functions
    con.create_function("strrev", 1, lambda s: s[::-1])

    con.row_factory = sqlite3.Row
    cur = con.cursor()
    res = cur.execute(query)
    return res

  def countRows(self, query_count: str) -> int:
    """Execute count query in SQLITE DB and get count result."""
    res = self.__basicQueryDB(query_count).fetchone()
    if len(res) > 0 and str(res[0]).isdigit():
      return int(res[0])
    else:
      return 0

  def selectOneRow(self, query_select: str) -> dict:
    """Execute select query from SQLITE DB and return the result as Python list."""
    selected_data = {}
    for row in self.__queryDB(query_select).fetchone():
      for key in row.keys():
        selected_data[key] = row[key]
    return selected_data

  def selectAllRows(self, query_select: str) -> list:
    """Execute select query from SQLITE DB and return the result as Python list."""
    selected_rows = []
    for row in self.__queryDB(query_select).fetchall():
      data = {}
      for key in row.keys():
        data[key] = row[key]
      selected_rows.append(data)
    return selected_rows

  def selectPartialRows(self, query_select: str, n_rows: int, n_select=1) -> list:
    """Execute select query from SQLITE DB and return the result as Python list.
      (Only select N rows from the N-th part.)"""
    query_rows = []
    res = self.__queryDB(query_select)
    for i in range(n_select):
      query_rows = res.fetchmany(n_rows)
    
    selected_rows = []
    for row in query_rows:
      data = {}
      for key in row.keys():
        data[key] = row[key]
      selected_rows.append(data)

    return selected_rows

  def dumpTable(self, tablename: str, jsonpath="") -> None:
    """Dump a DB table into a json file."""
    if jsonpath:
      tabledata = []
      QUERY = ""
      if tablename.lower() == "composer" or tablename.lower() == "composers":
        QUERY = "SELECT * FROM Composers;"
      elif tablename.lower() == "piece" or tablename.lower() == "pieces":
        QUERY = "SELECT * FROM Pieces;"
      elif tablename.lower() == "collection" or tablename.lower() == "collections":
        QUERY = "SELECT * FROM Collections;"
      else:
        return None
      for row in self.__queryDB(QUERY).fetchall():
        data = {}
        for key in row.keys():
          data[key] = row[key]
        tabledata.append(data)
      with open(jsonpath) as j:
        json.dump(tabledata, j)

  def dumpDB(self, folderpath="") -> None:
    """Dump the entire DB into a json file."""
    if folderpath and os.path.isdir(folderpath):
      composers   = []
      collections = []
      pieces      = []
      QUERY_COMPOSER   = "SELECT * FROM Composers;"
      QUERY_COLLECTION = "SELECT * FROM Collections;"
      QUERY_PIECES     = "SELECT * FROM Pieces;"
      for row in self.__queryDB(QUERY_COMPOSER).fetchall():
        data = {}
        for key in row.keys():
          data[key] = row[key]
        composers.append(data)
      for row in self.__queryDB(QUERY_COLLECTION).fetchall():
        data = {}
        for key in row.keys():
          data[key] = row[key]
        collections.append(data)
      for row in self.__queryDB(QUERY_PIECES).fetchall():
        data = {}
        for key in row.keys():
          data[key] = row[key]
        collections.append(data)
        
      with open(f'{folderpath}/composers.json') as j:
        json.dump(composers, j)
      with open(f'{folderpath}/collections.json') as j:
        json.dump(collections, j)
      with open(f'{folderpath}/pieces.json') as j:
        json.dump(pieces, j)

# Test
if __name__ == '__main__':
  d = Database()
  print("CountRows test on composers: {}".format(d.countRows("SELECT COUNT(*) FROM Composers;")))
  print("CountRows test on pieces: {}".format(d.countRows("SELECT COUNT(*) FROM Pieces;")))
  print("SelectRows test on pieces: {}".format(d.selectRows("SELECT * FROM Pieces;")))
