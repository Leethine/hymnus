from flask import render_template, request
from database import Database
from metadata import Metadata
from piece_io import PieceIO
from hymnus_tools import createAlertBox

import shutil, os

class ComposerMod:
  def __init__(self):
    self.__meta = Metadata()
    self.__composer_code = ""
  
  def getModifyPageAllComposers(self):
    return render_template("delete_composer.html", \
      composerlist=self.__meta.getComposerCodeNameList())

  def getModifyPage(self, code):
    if code and code != "zzz_unknown" and self.__meta.composerExists(code):
      composer = self.__meta.getComposerMetadata(code)
      return render_template("delete_composer2.html", \
        composer_name=composer["ShortName"])
    else:
      return self.getModifyPageAllComposers()

  def __setComposer(self, req_form: request):
    if 'select-composer' in req_form:
      if req_form['select-composer'] != "":
        self.__composer_code = req_form['select-composer']

  def __isAlsoDeletePieces(self, req_form: request):
    if 'also-delete-pieces' in req_form:
      return True
    return False

  def __isAlsoDeleteCollections(self, req_form: request):
    if 'also-delete-collections' in req_form:
      return True
    return False
  
  def __deletePieces(self):
    pio = PieceIO()
    piece_list = Database().selectAllRows(f"SELECT folder_hash FROM Pieces WHERE \
                                            composer_code = '{self.__composer_code}'")
    for p in piece_list:
      piece_dir = pio.getPieceFileDir(p)
      if os.path.exists(piece_dir):
        shutil.rmtree(piece_dir)

    err = Database().executeInsertion(f"DELETE FROM Pieces WHERE \
                                        composer_code = '{self.__composer_code}'")
    if err:
      page += "<h2>Error encountered:</h2>" + err + "<br>"
    
    return err
  
  def getOption(self, req_form: request):
    if 'select-action' in req_form:
      return req_form['select-action']
  
  def hideComposer(self, req_form: request):
    page = ""
    self.__setComposer(req_form)
    if self.__composer_code and \
       self.__composer_code != "zzz_unknown" and \
       self.__meta.composerExists(self.__composer_code):
      composer = self.__meta.getComposerMetadata(self.__composer_code)
      err = Database().executeInsertion(f"UPDATE Composers SET listed = 0 WHERE code = '{self.__composer_code}'")
      if err:
        page += "<h2>Error encountered:</h2>" + err + "<br>"
    else:
      page += "<h2>No action.</h2>"
    page += '<h2><a href="/browse/composers">Go back to composers page</a></h2>'
    return page

  def unhideComposer(self, req_form: request):
    page = ""
    self.__setComposer(req_form)
    if self.__composer_code and \
       self.__composer_code != "zzz_unknown" and \
       self.__meta.composerExists(self.__composer_code):
      composer = self.__meta.getComposerMetadata(self.__composer_code)
      err = Database().executeInsertion(f"UPDATE Composers SET listed = 1 WHERE code = '{self.__composer_code}'")
      if err:
        page += "<h2>Error encountered:</h2>" + err + "<br>"
    else:
      page += "<h2>No action.</h2>"
    page += '<h2><a href="/browse/composers">Go back to composers page</a></h2>'
    return page
  
  def deleteComposer(self, req_form: request):
    page = ""
    self.__setComposer(req_form)
    
    if self.__composer_code and \
       self.__composer_code != "zzz_unknown" and \
       self.__meta.composerExists(self.__composer_code):
      composer = self.__meta.getComposerMetadata(self.__composer_code)
      err = Database().executeInsertion(f"DELETE FROM Composers WHERE code = '{self.__composer_code}'")
      if err:
        page += "<h2>Error encountered:</h2>" + err + "<br>"
      # validate the deletion
      if not self.__meta.composerExists(self.__composer_code):
        page += f"<h2>Composer deleted: {composer["ShortName"]}</h2>"
      # delete also pieces and collections
      if self.__isAlsoDeleteCollections(req_form):
        err = Database().executeInsertion(f"DELETE FROM Collections WHERE composer_code = '{self.__composer_code}'")
        if err:
          page += "<h2>Error encountered:</h2>" + err + "<br>"
      if self.__isAlsoDeletePieces(req_form):
        page += self.__deletePieces()

    # if selected composer doesn't exist or empty string
    else:
      page += "<h2>No action.</h2>"
    page += '<h2><a href="/browse/composers">Go back to composers page</a></h2>'
    
    return page
  
  def applyChange(self, req_form: request):
    if 'select-composer' not in req_form:
      createAlertBox("Please select the composer!")
      
    if self.getOption(req_form) == "delete":
      return self.deleteComposer(req_form)
    elif self.getOption(req_form) == "hide":
      return self.hideComposer(req_form)
    else:
      return self.unhideComposer(req_form)


class PieceMod:
  def __init__(self, folder_hash=""):
    self.__hash = folder_hash
    self.__meta = Metadata()

  def getModifyPage(self):
    if self.__meta.pieceExists(self.__hash):
      data = self.__meta.getPieceMetadata(self.__hash)
      # Set arranger name
      if data["arranged"] != "1":
        data["arranger"] = " "
      elif data["arranged"] == "1" and data["arranger_code"] \
        and self.__meta.composerExists(data["arranger_code"]):
        data["arranger"] = self.__meta.getComposerMetadata(data["arranger_code"])["ShortName"]
      elif data["arranged"] == "1" and data["arranger_name"]:
        data["arranger"] = data["arranger_name"]
      else:
        data["arranger"] = " "
      # Set composer name
      if data["composer_code"] and self.__meta.composerExists(data["composer_code"]):
        data["composer"] = self.__meta.getComposerMetadata(data["composer_code"])["ShortName"]
      else:
        data["composer"] = " "
      # Clean "N/A"
      for k in data.keys():
        if data[k] == "N/A":
          data[k] = ""
      
      return render_template("modify_piece.html", metadata=data)
  
  def __isDeletion(self, req_form: request):
    if "select-action" in req_form and req_form["select-action"] == "delete":
      return True
    return False
  
  def __deletePiece(self):
    pio = PieceIO()
    if self.__meta.pieceExists(self.__hash):
      if os.path.exists(pio.getPieceFileDir(self.__hash)):
        shutil.rmtree(pio.getPieceFileDir(self.__hash))
      err = Database().executeInsertion(f"DELETE FROM Pieces WHERE folder_hash = '{self.__hash}'")
      if not err:
        return f"<h4>Deleted piece {self.__hash}</h4>"
      else:
        return err
    return "<h3>No action</h3>"
  
  def __modifyPiece(self, req_form):
    keylist = ['new-piece-title', 'new-piece-subtitle', 'new-piece-subsubtitle',
               'new-piece-dedicated', 'new-piece-year', 'new-piece-opus',
               'new-piece-instrument', 'new-piece-comment']
    err = ""
    for k in keylist:
      if k not in req_form:
        err += f"Input '{k}' not exist!\n"
    if err == "":
      new_title       = req_form["new-piece-title"]
      new_subtitle    = req_form["new-piece-subtitle"]
      new_subsubtitle = req_form["new-piece-subsubtitle"]
      new_dedicated   = req_form["new-piece-dedicated"]
      new_opus        = req_form["new-piece-opus"]
      new_year        = req_form["new-piece-year"]
      new_instrument  = req_form["new-piece-instrument"]
      new_comment     = req_form["new-piece-comment"]
      SQL = f"UPDATE Pieces SET title = '{new_title}', subtitle = '{new_subtitle}', \
              subsubtitle = '{new_subsubtitle}', dedicated_to = '{new_dedicated}',\
              opus = '{new_opus}', composed_year = '{new_year}', \
              instruments = '{new_instrument}', comment = '{new_comment}' \
              WHERE folder_hash = '{self.__hash}';"
      err = Database().executeInsertion(SQL)
    return err
  
  def submitChanges(self, req_form):
    page = '<h2><a href="/browse/all-pieces">Go back to list of pieces.</a></h2>'
    err = ""
    if self.__isDeletion(req_form):
      err = self.__deletePiece()
    else:
      err = self.__modifyPiece(req_form)
      if err == "":
        err = "<h3>Piece modified.</h3>"
    
    return err + "<br>" + page

class CollectionMod:
  def __init__(self, collection_code=""):
    self.__code = collection_code
    self.__meta = Metadata()

  def getModifyPage(self):
    if self.__meta.collectionExists(self.__code):
      data = self.__meta.getCollectionMetadata(self.__code)
      # Set composer name
      if data["composer_code"] and self.__meta.composerExists(data["composer_code"]):
        data["composer"] = self.__meta.getComposerMetadata(data["composer_code"])["ShortName"]
      else:
        data["composer"] = " "
      # Clean "N/A"
      for k in data.keys():
        if data[k] == "N/A":
          data[k] = ""
    
    return render_template("modify_collection.html", metadata=data)

  def __isDeletion(self, req_form: request):
    if "select-action" in req_form and req_form["select-action"] == "delete":
      return True
    return False
  
  def __dissociatePieces(self):
    err = ""
    SQL = f"SELECT folder_hash FROM Pieces WHERE collection_code LIKE '%{self.__code}%';"
    for piece_hash in Database().selectAllRows(SQL):
      SQL2 = f"SELECT collection_code FROM Pieces WHERE folder_hash = '{piece_hash["folder_hash"]}';"
      old_collection = Database().selectAllRows(SQL2)[0]['collection_code']
      # Remove the old collection code from the new collection
      new_collection = old_collection \
                                      .replace(f"{self.__code},","") \
                                      .replace(f",{self.__code}","") \
                                      .replace(f"{self.__code}","")
      SQL3 = f"UPDATE Pieces SET collection_code = '{new_collection}' \
               WHERE folder_hash = '{piece_hash["folder_hash"]}';"
      err += Database().executeInsertion(SQL3)
    return err
  
  def __deleteCollection(self):
    if self.__meta.collectionExists(self.__code):
      err = self.__dissociatePieces()
      err += Database().executeInsertion(f"DELETE FROM Collections WHERE code = '{self.__code}'")
      if not err:
        return f"<h4>Deleted collection {self.__code}</h4>"
      else:
        return err
    return "<h3>No action.</h3>"

  def __modifyCollection(self, req_form):
    keylist = ['new-collection-title', 'new-collection-subtitle',
               'new-collection-subsubtitle', 'new-collection-editor',
               'new-collection-opus', 'new-collection-volume',
               'new-collection-instrument', 'new-collection-description']
    err = ""
    for k in keylist:
      if k not in req_form:
        err += f"Input '{k}' not exist!\n"
    if err == "":
      new_title       = req_form["new-collection-title"]
      new_subtitle    = req_form["new-collection-subtitle"]
      new_subsubtitle = req_form["new-collection-subsubtitle"]
      new_editor      = req_form["new-collection-editor"]
      new_opus        = req_form["new-collection-opus"]
      new_volume      = req_form["new-collection-volume"]
      new_instrument  = req_form["new-collection-instrument"]
      new_description = req_form["new-collection-description"]
      SQL = f"UPDATE Collections SET title = '{new_title}', subtitle = '{new_subtitle}', \
              subsubtitle = '{new_subsubtitle}', editor = '{new_editor}', opus = '{new_opus}', \
              volume = '{new_volume}', instruments = '{new_instrument}', \
              description_text = '{new_description}' WHERE code = '{self.__code}';"
      err = Database().executeInsertion(SQL)
    return err

  def submitChanges(self, req_form: request):
    page = '<h2><a href="/browse/collections">Go back to list of collections.</a></h2>'
    err = ""
    if self.__isDeletion(req_form):
      err = self.__deleteCollection()
    else:
      err = self.__modifyCollection(req_form)
      if err == "":
        err = "<h3>Collection modified.</h3>"
    
    return err + "<br>" + page
  
  def getAddToCollectionPage(self):
    if self.__meta.collectionExists(self.__code):
      data = self.__meta.getCollectionMetadata(self.__code)
      title = data["title"] + ", " + data["opus"]
      return render_template("add_to_collection.html", collection_title=title)
    else:
      return render_template("add_to_collection.html", collection_title="?")
  
  def addToCollection(self, req_form: request):
    page = ""
    if 'list-of-pieces' in req_form and req_form['list-of-pieces']:
      err = ""
      list_of_pieces = req_form['list-of-pieces'].split(',')
      for p in list_of_pieces:
        if self.__meta.pieceExists(p):
          # Append "," to the piece's existing collections
          old_collection_code = self.__meta.getPieceMetadata(p)['collection_code'].replace("N/A","")
          if old_collection_code:
            old_collection_code += ","
          # Prevent adding repetitive collection code in the same piece
          if not self.__code in old_collection_code:
            SQL = f"UPDATE Pieces SET collection_code = '{old_collection_code}{self.__code}' WHERE folder_hash = '{p}';"
            err += Database().executeInsertion(SQL)
      if err == "":
        page += "<h3>Piece(s) added to collection.</h3>"
      else:
        page += "<h3>Error: </h3>"
        page += err
    else:
      page += "<h3>No action.</h3>"
    page += '<h2><a href="/browse/collections">Go back to list of collections.</a></h2>'
    
    return page
