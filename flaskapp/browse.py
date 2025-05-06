from html_table import createTable, createPagination
import database
import math

def createTableAndPagination(query_count: str, query_select: str,
                             page_number: int, items_per_page: int,
                             table_header: list, parent_url: str) -> dict:
  # Return dictionary with table html and pagination html
  html = {}
  html["Table"] = ""
  html["Pagination"] = ""

  # make sure page number is digit
  if not str(page_number).isdigit():
    html["Table"] = f"<h4>Invalid page number: {page_number}!!!</h4>"
    return html
  i_pagenumber = int(page_number) - 1
  
  count = database.queryDB(query_count).fetchone()[0]
  n_pages = int(math.ceil(float(count / items_per_page)))
  # make sure pagenumber is within the range
  if i_pagenumber < 0 or i_pagenumber >= n_pages:
    html["Table"] = f"<h4>Page {page_number} is out of range !!!</h4>"
    return html

  res = database.queryDB(query_select)
  rows = [{}]
  for i in range(int(page_number)):
    rows = res.fetchmany(items_per_page)

  html["Table"] = createTable(table_rows=rows, 
                              header_filter=table_header)
  html["Pagination"] = createPagination(page_number=page_number,
                                        total_pages=n_pages,
                                        parent_url=parent_url)
  return html


def browseComposers(pagenumber=1, items_per_page=20):
  QUERY_COUNT = """
    SELECT COUNT(lastname)
    FROM composers
    WHERE code != 'zzz_unknown'
    AND code != 'zzz_various';
  """

  QUERY = """
    SELECT
      STRREV ( SUBSTR ( 
        STRREV(knownas_name), 1, INSTR( STRREV (knownas_name), ' ') 
      ) ) AS 'Name',
      knownas_name AS 'FullName',
      bornyear || ' - ' || diedyear AS 'Years',
      '<a href=\"/works-by/' || code ||
      '"><i class=\"bi bi-arrow-up-right-square\"></i></a>'
      AS '   '
    FROM composers WHERE code != 'zzz_unknown'
    AND code != 'zzz_various'
    ORDER BY code ASC;
  """

  html = createTableAndPagination(query_count=QUERY_COUNT,
                                  query_select=QUERY,
                                  page_number=pagenumber,
                                  items_per_page=items_per_page,
                                  table_header=["Name", "FullName", "Years", "   "],
                                  parent_url="browse/composers")
  return html

def browseCollections(pagenumber=1, items_per_page=50):
  QUERY_COUNT = """
    SELECT COUNT(title)
    FROM collections;
  """

  QUERY = """
    SELECT
      ' ' AS 'Empty',
      Collections.title AS 'Title',
      Collections.opus AS 'Opus',
      Collections.editor AS 'Editor',
      Composers.knownas_name AS 'Composer',

      '<a href=\"/collection-at/' ||
      Collections.code ||
      '"><i class=\"bi bi-arrow-up-right-square\"></i></a>'
      AS '   '

    FROM Collections
    JOIN Composers ON Collections.composer_code = Composers.code
    ORDER BY Collections.title ASC;
  """

  html = createTableAndPagination(query_count=QUERY_COUNT,
                                  query_select=QUERY,
                                  page_number=pagenumber,
                                  items_per_page=items_per_page,
                                  table_header=["Empty", "Title", "Opus", "Editor", "Composer", "   "],
                                  parent_url="browse/collections")
  return html


def browseWorks(pagenumber=1, items_per_page=100, composer_code=""):
  QUERY_COUNT = """
    SELECT COUNT(title)
    FROM pieces;
  """

  QUERY = """
    SELECT
      ' ' AS 'Empty',
      Pieces.title AS 'Title',
      Pieces.opus AS 'Opus',
      IIF(Pieces.arranged,'Y','') AS 'Arranged?',
      Pieces.instruments AS 'For',
      Composers.knownas_name AS 'Composer',
      '<a href=\"/file/' || 
      Pieces.folder_hash || 
      '\"><i class=\"bi bi-arrow-up-right-square\"></i></a>'
      AS '   '
      FROM Pieces
      JOIN Composers ON Pieces.composer_code = Composers.code
  """

  header = ["Empty", "Title", "Opus", "Composer", "   "]
  parent_url="browse/all-pieces"
  if composer_code:
    QUERY += f" WHERE Pieces.composer_code = '{composer_code}'"
    header = ["Empty", "Title", "Opus", "   "]
    parent_url="works-by"

  QUERY += " ORDER BY Pieces.title ASC;"

  html = createTableAndPagination(query_count=QUERY_COUNT,
                                  query_select=QUERY,
                                  page_number=pagenumber,
                                  items_per_page=items_per_page,
                                  table_header=header,
                                  parent_url=parent_url)

  return html
