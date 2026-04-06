import sqlite3, os, time
from utilities import SingletonMeta
from config import SQLITE_MAX_RETRY, SQLITE_WAIT_TIME

class DB_SQLITE(metaclass=SingletonMeta):
  """Low-level SQLite database interface."""
  

  def getDBPath(self) -> str:
    """Return database path in 'HYMNUS_DB' env variable."""
    if 'HYMNUS_DB' in os.environ.keys():
      return os.environ['HYMNUS_DB']
    return ":memory:"


  def updateRows(self, query: str) -> str:
    """Execute SQLITE DB WRITE query.
       Return error message if any, otherwise return empty string."""
    err = ""
    retry_count = 0
    con = sqlite3.connect(self.getDBPath())
    for i in range(SQLITE_MAX_RETRY):
      try:
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        break
      except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
          time.sleep(SQLITE_WAIT_TIME)
          retry_count += 1
      except sqlite3.DatabaseError as e:
        err = str(e)
        break
    
    if retry_count >= SQLITE_MAX_RETRY:
      err = f"SQLite database is locked after {retry_count} retries."
    
    con.close()
    return err


  def countRows(self, query_count: str) -> int:
    """Execute count query in SQLITE DB and get count result."""
    count = -1
    con = sqlite3.connect(self.getDBPath())
    con.row_factory = sqlite3.Row
    for i in range(SQLITE_MAX_RETRY):
      try:
        cur = con.cursor()
        res = cur.execute(query_count).fetchone()
        if len(res) > 0 and type(res[0]) == int:
          count = res[0]
        break
      except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
          time.sleep(SQLITE_WAIT_TIME)
      except sqlite3.DatabaseError as e:
        break
    con.close()
    return count


  def selectRows(self, query: str) -> list:
    """Execute SQLITE DB query."""
    selected_rows = []
    con = sqlite3.connect(self.getDBPath())
    con.row_factory = sqlite3.Row
    for i in range(SQLITE_MAX_RETRY):
      try:
        cur = con.cursor()
        res = cur.execute(query).fetchall()
        for r in res:
          row = {}
          for k in r.keys():
            row[k] = r[k]
          selected_rows.append(row)
        break
      except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
          time.sleep(SQLITE_WAIT_TIME)
      except sqlite3.DatabaseError as e:
        break
    con.close()
    return selected_rows


  def selectPartialRows(self, query_select: str, n_rows: int, part=1) -> list:
    """Execute select query from SQLITE DB and return the result as Python list.
      (Only select N rows from the N-th part.)"""

    selected_rows = []
    con = sqlite3.connect(self.getDBPath())
    con.row_factory = sqlite3.Row
    for i in range(SQLITE_MAX_RETRY):
      try:
        cur = con.cursor()
        query_res = cur.execute(query_select)
        res = None
        for i in range(part):
          res = query_res.fetchmany(n_rows)
        if res:
          for r in res:
            row = {}
            for k in r.keys():
              row[k] = r[k]
            selected_rows.append(row)
        break
      except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
          time.sleep(SQLITE_WAIT_TIME)
      except sqlite3.DatabaseError as e:
        break
    con.close()
    return selected_rows


  def verifySQLiteSyntax(self, query: str) -> bool:
    """Verify if the query is a valid SQLITE query."""
    con = sqlite3.connect(self.getDBPath())
    try:
      cur = con.cursor()
      cur.execute("EXPLAIN QUERY PLAN " + query)
      con.close()
      return True
    except sqlite3.DatabaseError as e:
      con.close()
      return False
  