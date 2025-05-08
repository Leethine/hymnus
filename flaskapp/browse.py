from flask import render_template
from html_table import createTable, createPagination
import config, toggle_menu, metadata, database
import math

def calculateTotalPages(items_per_page: int, query_count: str):
  item_count = database.queryDB(query_count).fetchone()[0]
  return int(math.ceil(float(item_count) / float(items_per_page)))

def getTableDataList(page_number: int, items_per_page: int, query_select: str):
  res = database.queryDB(query_select)
  rows = []
  for i in range(page_number):
    rows = res.fetchmany(items_per_page)
  items = []
  if len(rows) > 0:
    for row in rows:
      d = {}
      for k in row.keys():
        d[k] = row[k]
      items.append(d)
  return items


def getComposerContent(pagenumber=1, items_per_page=20):
  QUERY_COUNT = """
    SELECT COUNT(lastname)
    FROM composers
    WHERE code != 'zzz_unknown';
  """

  QUERY = """
    SELECT
      STRREV ( SUBSTR ( 
        STRREV(knownas_name), 1, INSTR( STRREV (knownas_name), ' ') 
      ) ) AS 'Name',
      knownas_name AS 'Full Name',
      bornyear || ' - ' || diedyear AS 'Years',
      '<a href=\"/browse/works-by/' || code ||
      '"><i class=\"bi bi-arrow-up-right-square\"></i></a>'
      AS '   '
    FROM composers WHERE code != 'zzz_unknown'
    ORDER BY code ASC;
  """

  content = {}
  content["total_number_of_pages"] = calculateTotalPages(items_per_page, QUERY_COUNT)
  content["current_page_number"] = pagenumber
  content["table_data_list"] = getTableDataList(pagenumber, items_per_page, QUERY)
  content["table_head_list"] = ["Name", "Full Name", "Years", "   "]
  content["parent_url"] = "/browse/composers"
  return content

def getCollectionContent(pagenumber=1, items_per_page=50):
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
  
  content = {}
  content["total_number_of_pages"] = calculateTotalPages(items_per_page, QUERY_COUNT)
  content["current_page_number"] = pagenumber
  content["table_data_list"] = getTableDataList(pagenumber, items_per_page, QUERY)
  content["table_head_list"] = ["Title", "Opus", "Editor", "Composer", "   "]
  content["parent_url"] = "/browse/collections"
  return content


def getPieceContent(pagenumber=1, items_per_page=100, composer_code=""):
  QUERY_COUNT = """
    SELECT COUNT(title)
    FROM pieces
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

  header = ["Title", "Opus", "Composer", "   "]
  parent_url = "/browse/all-pieces"

  if composer_code:
    QUERY += f" WHERE Pieces.composer_code = '{composer_code}'"
    QUERY_COUNT += f" WHERE composer_code = '{composer_code}'"
    header = ["Title", "Opus", "   "]
    parent_url = f"/browse/works-by/{composer_code}"

  QUERY += " ORDER BY Pieces.title ASC;"
  QUERY_COUNT += ";"

  table_header = header
  parent_url=parent_url
  content = {}
  content["total_number_of_pages"] = calculateTotalPages(items_per_page, QUERY_COUNT)
  content["current_page_number"] = pagenumber
  content["table_data_list"] = getTableDataList(pagenumber, items_per_page, QUERY)
  content["table_head_list"] = header
  content["parent_url"] = parent_url
  return content


def browsePageAtPageNumber(pagetype: str, currentpage: str, composercode: str):
  if currentpage.isdigit() and int(currentpage) > 0:
    title = ""
    pagemenu = []
    content = []
    if pagetype == "c":
      title = "Composers"
      pagemenu = toggle_menu.getPageAndMenuContent("c")
      if int(currentpage) > 1:
        pagemenu["url_composers"] = "/browse/composers"
      content = getComposerContent(pagenumber=int(currentpage),
                                  items_per_page=config.COMPOSERS_PER_PAGE)
    elif pagetype == "col":
      title = "Collections"
      pagemenu = toggle_menu.getPageAndMenuContent("col")
      if int(currentpage) > 1:
        pagemenu["url_collections"] = "/browse/collections"
      content = getCollectionContent(pagenumber=int(currentpage),
                                     items_per_page=config.COLLECTIONS_PER_PAGE)
    elif pagetype == "a":
      title = "All Pieces"
      pagemenu = toggle_menu.getPageAndMenuContent("p")
      if int(currentpage) > 1:
        pagemenu["url_pieces"] = "/browse/pieces"
      content = getPieceContent(pagenumber=int(currentpage),
                                items_per_page=config.PIECES_PER_PAGE_ALL)
    elif pagetype == "w" and composercode != "":
      composer = metadata.getComposerMetadata(composercode)
      title = composer["AbbrName"]
      pagemenu = toggle_menu.getComposerPageAndMenuContent(composer["AbbrName"], \
                                                           composer["LongName"] + " (" + composer["Year"] + ")")
      content = getPieceContent(pagenumber=int(currentpage),
                                items_per_page=config.PIECES_PER_PAGE_COMPOSER,
                                composer_code=composercode)
    else:
      return "<title>Error 2</title><h1>Page does not exist.</h1>"

    if int(currentpage) <= int(content["total_number_of_pages"]):
      return render_template("item_list.html", \
        page_title=f"{title} • Hymnus Library", \
        page_and_menu_content=pagemenu, \
        total_number_of_pages=content["total_number_of_pages"], \
        current_page_number=content["current_page_number"], \
        table_data_list=content["table_data_list"], \
        table_head_list=content["table_head_list"], \
        parent_url=content["parent_url"])

  return "<title>Error 1</title><h1>Page does not exist.</h1>"

def browseCollectionAtCode(collection_code: str):
  collection_info = metadata.getCollectionMetadata(collection_code)
  piece_list = database.getCollectionPieces(collection_code)
  for piece in piece_list:
    if collection_info["composer_code"]:
      piece["popup_title"] = ""
      piece["popup_content"] = ""
    elif piece["composer_code"]:
      composer = metadata.getComposerMetadata(piece["composer_code"])
      piece["popup_title"] = "Composer"
      piece["popup_content"] = composer["ShortName"]
    else:
      piece["popup_title"] = ""
      piece["popup_content"] = ""
  
  return render_template("collection_pieces.html", \
                  collection_metadata=collection_info, \
                  piece_metadata_list=piece_list)
