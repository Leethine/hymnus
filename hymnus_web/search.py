from database import Database
from metadata import Metadata
from flask import request, render_template
from rapidfuzz.process import extract

class Search():
  def __init__(self):
    self.__selection = {}
    self.__selection["substring"] = "checked"
    self.__selection["opus"] = ""
    self.__selection["fuzzy"] = ""
    self.__method = "substring"
    
  def __clearSelection(self):
    self.__selection["substring"] = ""
    self.__selection["opus"] = ""
    self.__selection["fuzzy"] = ""
  
  def getMethod(self):
    return self.__method
  
  def setMethod(self, method):
    self.__method = method
    self.__clearSelection()
    self.__selection[self.__method] = "checked"
  
  def setMethodFromHtml(self, req_form):
    if 'radio-select' in req_form and req_form['radio-select']:
      self.setMethod(req_form['radio-select'])
    else:
      self.setMethod("substring")


  def render_substring_search_result(self, keyword : str) -> str:
    kwd = keyword.lower()
    QUERY = """
      SELECT ' ' AS 'Empty', Pieces.title AS 'Title', 
      Pieces.opus AS 'Opus', Composers.knownas_name AS 'Composer', 
      '<a href=\"/file/' || Pieces.folder_hash || 
      '\"><i class=\"bi bi-arrow-up-right-square\"></i></a>' 
      AS '   ' FROM Pieces
      
      JOIN Composers ON Pieces.composer_code = Composers.code 
      JOIN Piece_search ON Piece_search.folder_hash = Pieces.folder_hash
      WHERE 
    """
    QUERY += f"Piece_search.context LIKE '%{keyword}%' OR "
    QUERY += f"Piece_search.author LIKE '%{keyword}%' OR "
    QUERY += f"Piece_search.opus LIKE '%{keyword}%';"
    
    QUERY_COUNT = """
      SELECT COUNT(*)
      FROM Piece_search WHERE 
    """
    QUERY_COUNT += f"Piece_search.context LIKE '%{keyword}%' OR "
    QUERY_COUNT += f"Piece_search.author LIKE '%{keyword}%' OR "
    QUERY_COUNT += f"Piece_search.opus LIKE '%{keyword}%';"
    
    table_head = ["Title", "Opus", "Composer", "   "]
    table_data = [" ", " ", " ", " "]
    
    if Database().countRows(QUERY_COUNT) != 0:
      table_data = Database().selectAllRows(QUERY)
    
    return render_template("search.html", \
                           search_selection=self.__selection, \
                           table_head_list=table_head, \
                           table_data_list=table_data)

  def render_instrument_search_result(self, keyword):
    kwd = keyword.lower()
    
    QUERY = """
      SELECT ' ' AS 'Empty', Pieces.title AS 'Title', 
      Pieces.opus AS 'Opus', Composers.knownas_name AS 'Composer', 
      '<a href=\"/file/' || Pieces.folder_hash || 
      '\"><i class=\"bi bi-arrow-up-right-square\"></i></a>' 
      AS '   ' FROM Pieces
      JOIN Composers ON Pieces.composer_code = Composers.code 
      JOIN Piece_search ON Piece_search.folder_hash = Pieces.folder_hash
      WHERE 
    """
    QUERY += f"Piece_search.instruments LIKE '%{keyword}%';"
    
    QUERY_COUNT = """
      SELECT COUNT(*)
      FROM Piece_search WHERE 
    """
    QUERY_COUNT += f"instruments LIKE '%{keyword}%';"
    
    table_head = ["Title", "Opus", "Composer", "   "]
    table_data = [" ", " ", " ", " "]
    
    if Database().countRows(QUERY_COUNT) != 0:
      table_data = Database().selectAllRows(QUERY)
    
    return render_template("search.html", \
                           search_selection=self.__selection, \
                           table_head_list=table_head, \
                           table_data_list=table_data)
  
  def render_search(self, keyword, method="substring"):
    self.setMethod(method)
    if method == "substring":
      return self.render_substring_search_result(keyword)
    elif method == "instrument":
      return self.render_instrument_search_result(keyword)
    elif method == "fuzzy":
      #TODO implement fuzzy search
      return self.getDefaultPage()
    else:
      return self.getDefaultPage()
  
  def getDefaultPage(self):
    return render_template("search.html", \
                           search_selection=self.__selection)
    
  def render_fuzzy_search_result(self, keyword: str) -> str:
    return ""
  