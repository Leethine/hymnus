from jinja2 import Environment, FileSystemLoader

import os, sys
from metadata import Metadata
from database import Database
from piece_io import PieceIO
import hymnus_config, math

class ToggleHtmlMenu():
  """This class returns a dictionary controls the html page
     content and toggles the links for tabs and menu."""

  def __init__(self):
    self.PAGE_AND_MENU_CONTENT = {
      "library": hymnus_config.LINRARY_NAME,
      "headline": "",
      "description": "",
      "toggle_menu_search"      : "", "url_search"     : "search.html",
      "toggle_menu_allpieces"   : "", "url_allpieces"  : "pieces.html",
      "toggle_menu_collections" : "", "url_collections": "collections.html",
      "toggle_menu_composers"   : "", "url_composers"  : "composers.html"
    }

  def getPageAndMenuContent(self, page_type: str):
    """Get the contect dictionary for main pages."""
    content = self.PAGE_AND_MENU_CONTENT.copy()
    if page_type == "p" or page_type == "pieces" or \
      page_type == "w" or page_type == "works":
      content["headline"] = "Pieces"
      content["description"] = "Browse all work pieces in this library."
      content["toggle_menu_allpieces"] = " w3-theme-l3 "
      content["url_allpieces"] = "#"
    elif page_type == "c" or page_type == "composers":
      content["headline"] = "Composers"
      content["description"] = "Browse the works of composers"
      content["toggle_menu_composers"] = " w3-theme-l3 "
      content["url_composers"] = "#"
    elif page_type == "col" or page_type == "collections":
      content["headline"] = "Collections"
      content["description"] = "Browse the list of collections"
      content["toggle_menu_collections"] = " w3-theme-l3 "
      content["url_collections"] = "#"
    elif page_type == "s" or page_type == "search":
      # TODO
      content["headline"] = "Search (WIP)"
      content["description"] = "Type to search..."
      content["toggle_menu_search"] = " w3-theme-l3 "
      content["url_search"] = "#"
    else:
      pass
    return content

  def getComposerPageAndMenuContent(self, composer_name: str, composer_info: str):
    """Get the contect dictionary for composer pages."""
    content = self.PAGE_AND_MENU_CONTENT.copy()
    content["headline"] = f"List of works by {composer_name}"
    content["description"] = f"<h4>{composer_info}</h4>"
    return content


class ItemListExport:
  def __init__(self):
    self.__meta = Metadata()
    self.__toggle = ToggleHtmlMenu()

  def calculateTotalPages(self, items_per_page: int, query_count: str):
    item_count = Database().countRows(query_count)
    return int(math.ceil(float(item_count) / float(items_per_page)))
  
  def calculateTotalPiecePages(self, items_per_page: int):
    QUERY_COUNT = """
      SELECT COUNT(*)
      FROM pieces;
    """
    return self.calculateTotalPages(items_per_page, QUERY_COUNT)

  def calculateComposerPiecePages(self, items_per_page: int, composer_code: str):
    QUERY_COUNT = """
      SELECT COUNT(*) FROM pieces
      WHERE composer_code = '{composer_code}'
    """
    return self.calculateTotalPages(items_per_page, QUERY_COUNT)
  
  def calculateTotalCollectionPages(self, items_per_page: int):
    QUERY_COUNT = """
      SELECT COUNT(*)
      FROM collections;
    """
    return self.calculateTotalPages(items_per_page, QUERY_COUNT)
  
  def calculateTotalComposerPages(self, items_per_page: int):
    QUERY_COUNT = """
      SELECT COUNT(*)
      FROM composers
      WHERE code != 'zzz_unknown';
    """
    return self.calculateTotalPages(items_per_page, QUERY_COUNT)
  
  def getListOfComposers(self) -> list:
    QUERY = """
      SELECT code FROM composers
      WHERE code != 'zzz_unknown'
      ORDER BY code ASC;
    """
    res = Database().selectAllRows(QUERY)
    composers = []
    for item in res:
      if 'code' in item.keys():
        composers.append(item['code'])
    return composers
  
  def getListOfCollections(self) -> list:
    QUERY = """
      SELECT code FROM collections
      ORDER BY code ASC;
    """
    res = Database().selectAllRows(QUERY)
    col = []
    for item in res:
      if 'code' in item.keys():
        col.append(item['code'])
    return col

  def getListOfPieces(self) -> list:
    QUERY = """
      SELECT folder_hash FROM pieces
      ORDER BY folder_hash ASC;
    """
    res = Database().selectAllRows(QUERY)
    pieces = []
    for item in res:
      if 'folder_hash' in item.keys():
        pieces.append(item['folder_hash'])
    return pieces
  
  def getListOfComposerPieces(self, composer_code='') -> list:
    QUERY = " SELECT folder_hash FROM pieces WHERE composer_code = "
    QUERY += f"'{composer_code}' ORDER BY folder_hash ASC;"
    res = Database().selectAllRows(QUERY)
    pieces = []
    for item in res:
      if 'folder_hash' in item.keys():
        pieces.append(item['folder_hash'])
    return pieces

  def getComposerContent(self, pagenumber=1, items_per_page=20) -> dict:
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
        '<a href=\"' || code ||
        '.html"><i class=\"bi bi-arrow-up-right-square\"></i></a>'
        AS '   '
      FROM composers WHERE code != 'zzz_unknown'
      AND listed > 0
      ORDER BY code ASC;
    """

    content = {}
    content["total_number_of_pages"] = self.calculateTotalPages(items_per_page, QUERY_COUNT)
    content["current_page_number"] = pagenumber
    content["table_data_list"] = Database().selectPartialRows(QUERY, items_per_page, pagenumber)
    content["table_head_list"] = ["Name", "Full Name", "Years", "   "]
    content["parent_url"] = "composers.html"
    return content

  def getCollectionContent(self, pagenumber=1, items_per_page=50) -> dict:
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
    content["total_number_of_pages"] = self.calculateTotalPages(items_per_page, QUERY_COUNT)
    content["current_page_number"] = pagenumber
    content["table_data_list"] = Database().selectPartialRows(QUERY, items_per_page, pagenumber)
    content["table_head_list"] = ["Title", "Opus", "Editor", "Composer", "   "]
    content["parent_url"] = "collections.html"
    return content

  def getPieceContent(self, pagenumber=1, items_per_page=100, composer_code="") -> dict:
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
        '<a href=\"' || Pieces.folder_hash || 
        '.html\"><i class=\"bi bi-arrow-up-right-square\"></i></a>'
        AS '   '
        FROM Pieces
        JOIN Composers ON Pieces.composer_code = Composers.code
    """

    header = ["Title", "Opus", "Composer", "   "]
    parent_url = "pieces.html"

    if composer_code:
      QUERY += f" WHERE Pieces.composer_code = '{composer_code}'"
      QUERY_COUNT += f" WHERE composer_code = '{composer_code}'"
      header = ["Title", "Opus", "   "]
      parent_url = f"{composer_code}.html"

    QUERY += " ORDER BY Pieces.title ASC;"
    QUERY_COUNT += ";"

    table_header = header
    parent_url=parent_url
    content = {}
    content["total_number_of_pages"] = self.calculateTotalPages(items_per_page, QUERY_COUNT)
    content["current_page_number"] = pagenumber
    content["table_data_list"] = Database().selectPartialRows(QUERY, items_per_page, pagenumber)
    content["table_head_list"] = header
    content["parent_url"] = parent_url
    return content

  def browsePageAtPageNumber(self, pagetype: str, currentpage: str, composercode: str) -> str:
    if currentpage.isdigit() and int(currentpage) > 0:    
      title = ""
      pagemenu = []
      content = []
      if pagetype == "c":
        title = "Composers"
        pagemenu = self.__toggle.getPageAndMenuContent("c")
        if int(currentpage) > 1:
          pagemenu["url_composers"] = "composers.html"
        content = self.getComposerContent(pagenumber=int(currentpage),
                                    items_per_page=hymnus_config.COMPOSERS_PER_PAGE)
      elif pagetype == "col":
        title = "Collections"
        pagemenu = self.__toggle.getPageAndMenuContent("col")
        if int(currentpage) > 1:
          pagemenu["url_collections"] = "collections.html"
        content = self.getCollectionContent(pagenumber=int(currentpage),
                                      items_per_page=hymnus_config.COLLECTIONS_PER_PAGE)
      elif pagetype == "a":
        title = "All Pieces"
        pagemenu = self.__toggle.getPageAndMenuContent("p")
        if int(currentpage) > 1:
          pagemenu["url_pieces"] = "pieces.html"
        content = self.getPieceContent(pagenumber=int(currentpage),
                                  items_per_page=hymnus_config.PIECES_PER_PAGE_ALL)
      elif pagetype == "w" and composercode != "":
        composer = self.__meta.getComposerMetadata(composercode)
        title = composer["AbbrName"]
        pagemenu = self.__toggle.getComposerPageAndMenuContent(composer["AbbrName"], \
                                                        composer["LongName"] + " (" + composer["Year"] + ")")
        content = self.getPieceContent(pagenumber=int(currentpage),
                                  items_per_page=hymnus_config.PIECES_PER_PAGE_COMPOSER,
                                  composer_code=composercode)
      else:
        return "<title>Error 2</title><h1>Page does not exist.</h1>"

      if int(currentpage) <= int(content["total_number_of_pages"]):
        env = Environment(loader = FileSystemLoader('templates_static'))
        template = env.get_template('000static_item_list.html')
        output = template.render(page_title=f"{title} • Hymnus Library", \
          page_and_menu_content=pagemenu, \
          total_number_of_pages=content["total_number_of_pages"], \
          current_page_number=content["current_page_number"], \
          table_data_list=content["table_data_list"], \
          table_head_list=content["table_head_list"], \
          parent_url=content["parent_url"])
        return output

    return "<title>Error 1</title><h1>Page does not exist.</h1>"

  def browseCollectionAtCode(self, collection_code: str) -> str:
    collection_info = self.__meta.getCollectionMetadata(collection_code)
    piece_list = self.__meta.getCollectionPieces(collection_code)
    for piece in piece_list:
      if collection_info["composer_code"]:
        piece["popup_title"] = ""
        piece["popup_content"] = ""
      elif piece["composer_code"]:
        composer = self.__meta.getComposerMetadata(piece["composer_code"])
        piece["popup_title"] = "Composer"
        piece["popup_content"] = composer["ShortName"]
      else:
        piece["popup_title"] = ""
        piece["popup_content"] = ""
    
    env = Environment(loader = FileSystemLoader('templates_static'))
    template = env.get_template('000static_collection_pieces.html')
    output = template.render(collection_metadata=collection_info, \
                            piece_metadata_list=piece_list)
    return output


class FilePageExport:
  def __init__(self):
    self.__metadata = Metadata()
    self.__pieceio  = PieceIO()
  
  def openPiecePage(self, folderhash):
    pieceinfo = self.__metadata.getPieceMetadata(folderhash)
    filesinfo = self.__pieceio.getPiecePageFileList(folderhash)
    for i in filesinfo:
      #i["filelink"] = IP_ADDRESS + i["filelink"]
      absfilepath = self.__pieceio.getSavedFilePath(folderhash, i["filelink"].replace(f"/download/{folderhash}/",""))
      i["filelink"] = IP_ADDRESS + absfilepath.replace(os.environ['HYMNUS_FS'], 'files')
      
    if pieceinfo and filesinfo:
      env = Environment(loader = FileSystemLoader('templates_static'))
      template = env.get_template('000static_piece_files.html')
      output = template.render(piece_metadata=pieceinfo, \
                               file_metadata_list=filesinfo, \
                               has_footer="N")
      return output
    else:
      return "<h1>Page does not exist!!!</h1>"


if __name__ == '__main__':
  IP_ADDRESS="http://192.168.50.222:5000"

  if len(sys.argv) == 3 and sys.argv[1] == "--ip":
    IP_ADDRESS = str(sys.argv[2])
  
  items_export = ItemListExport()
  files_export = FilePageExport()

  # Front pages
  n_pages_piece_all  = items_export.calculateTotalPiecePages(hymnus_config.PIECES_PER_PAGE_ALL)
  n_pages_piece_comp = items_export.calculateTotalPiecePages(hymnus_config.PIECES_PER_PAGE_COMPOSER)
  n_pages_coll       = items_export.calculateTotalCollectionPages(hymnus_config.COLLECTIONS_PER_PAGE)
  n_pages_comp       = items_export.calculateTotalComposerPages(hymnus_config.COMPOSERS_PER_PAGE)

  os.mkdir("exported")
  # Composer Pages
  for i in range(n_pages_comp):
    with open("exported/composers_" + str(i+1) + ".html", 'w+') as f:
      f.write(items_export.browsePageAtPageNumber('c', str(i+1), ''))
    if i == 0:
      with open("exported/composers.html", 'w+') as f:
        f.write(items_export.browsePageAtPageNumber('c', str(i+1), ''))

  # Piece Pages
  for i in range(n_pages_piece_all):
    with open("exported/pieces_" + str(i+1) + ".html", 'w+') as f:
      f.write(items_export.browsePageAtPageNumber('a', str(i+1), ''))
    if i == 0:
      with open("exported/pieces.html", 'w+') as f:
        f.write(items_export.browsePageAtPageNumber('a', str(i+1), ''))
  
  # Collection Pages
  for i in range(n_pages_coll):
    with open("exported/collections_" + str(i+1) + ".html", 'w+') as f:
      f.write(items_export.browsePageAtPageNumber('col', str(i+1), ''))
    if i == 0:
      with open("exported/collections.html", 'w+') as f:
        f.write(items_export.browsePageAtPageNumber('col', str(i+1), ''))
    
  # Export piece pages
  for piece in items_export.getListOfPieces():
    with open("exported/" + piece + ".html", 'w+') as f:
      f.write(files_export.openPiecePage(piece))
  
  # Export collection pages
  for coll in items_export.getListOfCollections():
    with open("exported/" + coll + ".html", 'w+') as f:
      f.write(items_export.browseCollectionAtCode(coll))
  
  # Export composer pages
  for composer in items_export.getListOfComposers():
    for piece in items_export.getListOfComposerPieces(composer):
      for i in range(n_pages_piece_comp):
        with open("exported/" + composer + "_" + str(i+1) + ".html", 'w+') as f:
          f.write(items_export.browsePageAtPageNumber('a', str(i+1), composer))
        if i == 0:
          with open("exported/" + composer + ".html", 'w+') as f:
            f.write(items_export.browsePageAtPageNumber('a', str(i+1), composer))

  # Export index, about, contact pages
  env = Environment(loader = FileSystemLoader('templates_static'))
  template = env.get_template('000static_index.html')
  with open("exported/index.html", 'w+') as f:
    f.write(template.render())
  template = env.get_template('000static_about.html')
  with open("exported/about.html", 'w+') as f:
    f.write(template.render())
  template = env.get_template('000static_contact.html')
  with open("exported/contact.html", 'w+') as f:
    f.write(template.render())
  
  # TODO export search.html