import sqlite3
from flask import request
import math
from markupsafe import escape

DB_FILE = "/home/lizian/Projects/hymnus/blob/tables.db"

def queryDB(query: str):
  con = sqlite3.connect(DB_FILE)
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

def createHtmlTable(table_rows=[{}], table_head_filter=[], row_head_index="", linktype=""):
  html = """<table class="table">
            <thead><tr>
            <th scope="col"></th>"""
  head = []
  if table_head_filter:
    head = table_head_filter
  elif len(table_rows) > 0:
    head = table_rows[0].keys()
  else:
    pass

  for col_head in head:
    html += f'<th scope="col">{escape(col_head)}</th>'
  if linktype:
    html += f'<th scope="col"></th>'
  html += "</tr></thead><tbody>"

  for row in table_rows:
    html += "<tr>"
    if row_head_index and row_head_index in row.keys():
      html += f"<th scope=\"row\">{escape(row[row_head_index])}</th>"
    else:
      html += "<th scope=\"row\"></th>"
    for col_key in head:
      html += f"<td>{row[col_key]}</td>"
    if linktype == "c":
      code = row["code"]
      html += f"<th scope=\"row\"><a href=\"/works-by/{code}\">" \
              + "<i class=\"bi bi-arrow-up-right-square\"></i></a></th>"
    html += "</tr>"

  html += "</tbody></table>"
  return html

def createHtmlPagination(urlparent="", pagenumber=1, n_pages=1):
  if not str(pagenumber).isdigit():
    return f"Invalid page number: {pagenumber}"
  if not str(n_pages).isdigit():
    return f"Invalid total pages: {n_pages}"

  # page number as in array indexing
  i_pagenumber = int(pagenumber) - 1
  
  # generate html page list
  pagination_html = []
  if i_pagenumber >= 0 and i_pagenumber < n_pages:
    for i in range(n_pages):
      pagination_html.append("<a class=\"w3-button w3-hover-black\"" \
                             + f"href=\"/{escape(urlparent)}/{str(i+1)}\">{str(i+1)}</a>")
    pagination_html[i_pagenumber] = "<a class=\"w3-button w3-black\"" \
                                  + f"href=\"#\">{pagenumber}</a>"
    return " ".join(pagination_html)
  else:
    return "Page out of range"


def createComposerTableAndPagination(pagenumber=1, items_per_page=20):
  # Return dictionary with table html and pagination html
  html = {}
  html["Table"] = ""
  html["Pagination"] = ""
  
  # make sure page number is digit
  if not str(pagenumber).isdigit():
    html["Table"] = f"<h4>Invalid page number: {pagenumber}!!!</h4>"
    return html
  i_pagenumber = int(pagenumber) - 1
  
  QUERY_COUNT = """
    SELECT COUNT(lastname)
    FROM composers;
  """

  QUERY = """
    SELECT

      STRREV ( SUBSTR ( 
        STRREV(knownas_name), 1, INSTR( STRREV (knownas_name), ' ') 
      ) ) AS 'Name',

      code,
      knownas_name AS 'Full Name',
      bornyear AS 'Born',
      diedyear AS 'Died'
    FROM composers ORDER BY code ASC;
  """
  
  count = queryDB(QUERY_COUNT).fetchone()[0]
  n_pages = int(math.ceil(float(count / items_per_page)))
  # make sure pagenumber is within the range
  if i_pagenumber < 0 or i_pagenumber >= n_pages:
    html["Table"] = f"<h4>Page {pagenumber} is out of range !!!</h4>"
    return html

  res = queryDB(QUERY)
  composers = [{}]
  for i in range(pagenumber):
    composers = res.fetchmany(items_per_page)

  html["Table"] = createHtmlTable(table_rows=composers, \
                                  table_head_filter=["Full Name", "Born", "Died"], \
                                  row_head_index="Name", linktype="c")
  html["Pagination"] = createHtmlPagination(urlparent="composers",
                                            pagenumber=pagenumber, \
                                            n_pages=n_pages)
  return html


def createPieceTableAndPagination(composer_code="", pagenumber=1, items_per_page=50):
  # Return dictionary with table html and pagination html
  html = {}
  html["Table"] = ""
  html["Pagination"] = ""
  
  # make sure page number is digit
  if not str(pagenumber).isdigit():
    html["Table"] = f"<h4>Invalid page number: {pagenumber}!!!</h4>"
    return html
  i_pagenumber = int(pagenumber) - 1
  
  QUERY_COUNT = """
    SELECT COUNT(title)
    FROM pieces;
  """

  QUERY1 = """
    SELECT
      Pieces.title AS 'Title',
      Pieces.opus AS 'Opus',
      Pieces.arranged AS 'Arranged?',
      Pieces.instrument AS 'For',
      Pieces.folder_hash AS 'Hash',
      Pieces.composer_code,
      Composers.knownas_name AS 'Composer Name'
    FROM Pieces
    JOIN Composers ON Pieces.composer_code = Composers.code
    """
  
  QUERY2 = ""
  if composer_code:
    QUERY2 = f" WHERE Pieces.composer_code = '{composer_code}'"
  
  QUERY3 = """
    ORDER BY Pieces.title DESC;
  """

  count = queryDB(QUERY_COUNT).fetchone()[0]
  n_pages = int(math.ceil(float(count / items_per_page)))
  # make sure pagenumber is within the range
  if i_pagenumber < 0 or i_pagenumber >= n_pages:
    html["Table"] = f"<h4>Page {pagenumber} is out of range !!!</h4>"
    return html

  QUERY = QUERY1 + QUERY2 + QUERY3
  res = queryDB(QUERY)
  composers = [{}]
  for i in range(pagenumber):
    composers = res.fetchmany(items_per_page)

  html["Table"] = createHtmlTable(table_rows=composers, \
                                  table_head_filter=["Title", "Composer Name"], \
                                  row_head_index="composer_code")
  html["Pagination"] = createHtmlPagination(urlparent="all-pieces", \
                                            pagenumber=pagenumber, \
                                            n_pages=n_pages)
  return html


def createCollectionTableAndPagination(pagenumber=1, items_per_page=30):
  # Return dictionary with table html and pagination html
  html = {}
  html["Table"] = ""
  html["Pagination"] = ""
  
  # make sure page number is digit
  if not str(pagenumber).isdigit():
    html["Table"] = f"<h4>Invalid page number: {pagenumber}!!!</h4>"
    return html
  i_pagenumber = int(pagenumber) - 1
  
  QUERY_COUNT = """
    SELECT COUNT(title)
    FROM collections;
  """

  QUERY = """
    SELECT
      Collections.title AS 'Title',
      Collections.opus AS 'Opus',
      Collections.composer_code,
      Collections.editor,
      Composers.knownas_name AS 'Composer Name'
    FROM Collections
    JOIN Composers ON Collections.composer_code = Composers.code
    ORDER BY Collections.title DESC;
  """

  count = queryDB(QUERY_COUNT).fetchone()[0]
  n_pages = int(math.ceil(float(count / items_per_page)))
  # make sure pagenumber is within the range
  if i_pagenumber < 0 or i_pagenumber >= n_pages:
    html["Table"] = f"<h4>Page {pagenumber} is out of range !!!</h4>"
    return html

  res = queryDB(QUERY)
  collections = [{}]
  for i in range(pagenumber):
    collections = res.fetchmany(items_per_page)

  html["Table"] = createHtmlTable(table_rows=collections, \
                                  table_head_filter=["Title", "Opus", "Composer Name", "Editor"], \
                                  row_head_index="")
  html["Pagination"] = createHtmlPagination(urlparent="collections", \
                                            pagenumber=pagenumber, \
                                            n_pages=n_pages)
  return html

