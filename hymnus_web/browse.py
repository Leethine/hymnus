from flask import render_template
from metadata import Metadata
from database import Database
from toggle_menu import ToggleHtmlMenu
import hymnus_config, math

def calculateTotalPages(items_per_page: int, query_count: str):
  item_count = Database().countRows(query_count)
  return int(math.ceil(float(item_count) / float(items_per_page)))

#def getTableDataList(page_number: int, items_per_page: int, query_select: str):

def getComposerContent(pagenumber=1, items_per_page=20) -> dict:
  QUERY_COUNT = """
    SELECT COUNT(*)
    FROM composers
    WHERE code != 'zzz_unknown' 
    AND listed > 0;
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
    AND listed > 0 
    ORDER BY code ASC;
  """

  content = {}
  content["total_number_of_pages"] = calculateTotalPages(items_per_page, QUERY_COUNT)
  content["current_page_number"] = pagenumber
  content["table_data_list"] = Database().selectPartialRows(QUERY, items_per_page, pagenumber)
  content["table_head_list"] = ["Name", "Full Name", "Years", "   "]
  content["parent_url"] = "/browse/composers"
  return content

def getCollectionContent(pagenumber=1, items_per_page=50) -> dict:
  QUERY_COUNT = """
    SELECT COUNT(*)
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
  content["table_data_list"] = Database().selectPartialRows(QUERY, items_per_page, pagenumber)
  content["table_head_list"] = ["Title", "Opus", "Editor", "Composer", "   "]
  content["parent_url"] = "/browse/collections"
  return content


def getPieceContent(pagenumber=1, items_per_page=100, composer_code="") -> dict:
  QUERY_COUNT = """
    SELECT COUNT(*)
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

  table_head = ["Title", "Opus", "Composer", "   "]
  parent_url = "/browse/all-pieces"

  if composer_code:
    QUERY += f" WHERE Pieces.composer_code = '{composer_code}'"
    QUERY_COUNT += f" WHERE composer_code = '{composer_code}'"
    table_head = ["Title", "Opus", "   "]
    parent_url = f"/browse/works-by/{composer_code}"

  QUERY += " ORDER BY Pieces.title ASC;"
  QUERY_COUNT += ";"

  if Database().countRows(QUERY_COUNT) == 0:
    return getEmptyComposerContent(composer_code)
  else:
    content = {}
    content["total_number_of_pages"] = calculateTotalPages(items_per_page, QUERY_COUNT)
    content["current_page_number"] = pagenumber
    content["table_data_list"] = Database().selectPartialRows(QUERY, items_per_page, pagenumber)
    content["table_head_list"] = table_head
    content["parent_url"] = parent_url
    return content


def getEmptyComposerContent(composer_code) -> dict:
  content = {}
  content["total_number_of_pages"] = 1
  content["current_page_number"] = 1
  content["table_head_list"] = ["Title", "Opus", "   "]
  content["table_data_list"] = [" ", " ", " "]
  content["parent_url"] = f"/browse/works-by/{composer_code}"
  return content


def browsePageAtPageNumber(pagetype: str, currentpage: str, composercode: str) -> str:
  toggle = ToggleHtmlMenu()
  meta = Metadata()
  
  if currentpage.isdigit() and int(currentpage) > 0:    
    title = ""
    pagemenu = []
    content = []
    if pagetype == "c":
      title = "Composers"
      pagemenu = toggle.getPageAndMenuContent("c")
      if int(currentpage) > 1:
        pagemenu["url_composers"] = "/browse/composers"
      content = getComposerContent(pagenumber=int(currentpage),
                                   items_per_page=hymnus_config.COMPOSERS_PER_PAGE)
    elif pagetype == "col":
      title = "Collections"
      pagemenu = toggle.getPageAndMenuContent("col")
      if int(currentpage) > 1:
        pagemenu["url_collections"] = "/browse/collections"
      content = getCollectionContent(pagenumber=int(currentpage),
                                     items_per_page=hymnus_config.COLLECTIONS_PER_PAGE)
    elif pagetype == "a":
      title = "All Pieces"
      pagemenu = toggle.getPageAndMenuContent("p")
      if int(currentpage) > 1:
        pagemenu["url_pieces"] = "/browse/pieces"
      content = getPieceContent(pagenumber=int(currentpage),
                                items_per_page=hymnus_config.PIECES_PER_PAGE_ALL)
    elif pagetype == "w" and composercode != "":
      composer = meta.getComposerMetadata(composercode)
      title = composer["AbbrName"]
      pagemenu = toggle.getComposerPageAndMenuContent(composer["AbbrName"], \
                                                      composer["LongName"] + " (" + composer["Year"] + ")" \
                                                      + f' <a href="/delete-composer/{composercode}"> \
                                                        <i class="bi bi-pencil" style="font-size:70%"></i></a>')
      content = getPieceContent(pagenumber=int(currentpage),
                                items_per_page=hymnus_config.PIECES_PER_PAGE_COMPOSER,
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

def browseCollectionAtCode(collection_code: str) -> str:
  toggle = ToggleHtmlMenu()
  meta = Metadata()
  
  collection_info = meta.getCollectionMetadata(collection_code)
  piece_list = meta.getCollectionPieces(collection_code)
  for piece in piece_list:
    if collection_info["composer_code"]:
      piece["popup_title"] = ""
      piece["popup_content"] = ""
    elif piece["composer_code"]:
      composer = meta.getComposerMetadata(piece["composer_code"])
      piece["popup_title"] = "Composer"
      piece["popup_content"] = composer["ShortName"]
    else:
      piece["popup_title"] = ""
      piece["popup_content"] = ""
  
  return render_template("collection_pieces.html", \
                  collection_metadata=collection_info, \
                  piece_metadata_list=piece_list)
