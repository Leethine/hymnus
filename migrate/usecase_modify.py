from fileinput import filename

from metadata import Metadata
from filemanager import FileManager
from flask import request
from flask import render_template, redirect
from werkzeug.utils import secure_filename
from utilities import createHtmlAlertBox, verifyFormKeys
from auth import AuthWeak
from config import ACCEPTED_FILE_UPLOAD_EXTENSIONS, FILE_UPLOAD_WAIT_TIME
import re, os, time

def get_modify_collection_pieces_page(collection_code: str) -> str:
  collection = Metadata().reader().getCollection(collection_code)
  if not collection:
    return createHtmlAlertBox("Collection not found.", "Error")
  title = collection.get('title', 'Unknown Collection')
  opus = collection.get('opus', '')
  if opus:
    title += f" , {opus}"  
  return render_template("update_collection_pieces.html", collection_title=title)


def modify_collection_pieces(collection_code: str, req_form) -> str:
  """ This is the workflow for modifying (add/remove) pieces in an existing collection. """
  verify_usr_pwd_err = AuthWeak().verifyReqFormUserPassword(req_form)
  if verify_usr_pwd_err:
    return verify_usr_pwd_err

  action = req_form.get('select-action', '')
  if action not in ['add-to', 'remove-from']:
    return createHtmlAlertBox("Invalid action selected.", "Error")
  
  if action == 'add-to':
    if 'list-of-pieces-add' not in req_form.keys():
      return createHtmlAlertBox("Form fields missing, please check your input.", "Error")
    err = ""
    for piece_hash in req_form.get('list-of-pieces-add', '').split(','):
      piece_hash = piece_hash.replace(' ', '')
      if piece_hash and Metadata().reader().getPiece(piece_hash):
        # Ignore non-existing pieces
        err += Metadata().writer().addPieceToCollection(piece_hash, collection_code)
    if err:
      #TODO use production-level error handling here
      return f"<h2>Error occurred while updating collection:</h2> {err}"
    else:
      return redirect(f"/collection-at/{collection_code}")

  elif action == 'remove-from':
    if 'list-of-pieces-remove' not in req_form.keys():
      return createHtmlAlertBox("Form fields missing, please check your input.", "Error")
    err = ""
    for piece_hash in req_form.get('list-of-pieces-remove', '').split(','):
      piece_hash = piece_hash.replace(' ', '')
      if piece_hash and Metadata().reader().getPiece(piece_hash):
        err += Metadata().writer().rmPieceFromCollection(piece_hash, collection_code)
        
    if err:
      #TODO use production-level error handling here
      return f"<h2>Error occurred while updating collection:</h2> {err}"
    else:
      return redirect(f"/collection-at/{collection_code}")
  
  return redirect("/")



def get_update_piece_page(piece_hash: str) -> str:
  piece = Metadata().reader().getPiece(piece_hash)
  composer_code = piece.get('composer_code', '')
  composer_name = Metadata().reader().getComposer(composer_code).get('knownas_name', '')
  arranger_code = piece.get('arranger_code', '')
  arranger_name = piece.get('arranger_name', '')
  arranger_selected = ""
  if arranger_code:
    arranger_selected = Metadata().reader().getComposer(arranger_code).get('knownas_name', '')

  if not piece:
    return createHtmlAlertBox("Piece not found.", "Error")
  
  return render_template("update_piece_info.html", \
                          piece_info=piece, composer_selected=composer_name, \
                          arranger_selected=arranger_selected, arranger_name=arranger_name)


def update_piece_info(piece_hash: str, req_form) -> str:
  """ This is the workflow for updating piece information. """
  verify_usr_pwd_err = AuthWeak().verifyReqFormUserPassword(req_form)
  if verify_usr_pwd_err:
    return verify_usr_pwd_err

  action = req_form.get('select-action', '')
  if action not in ['modify', 'delete']:
    return createHtmlAlertBox("Invalid action selected.", "Error")
  
  if action == 'delete':
    err = Metadata().writer().deletePiece(piece_hash)
    err += FileManager().deleteAllFiles(piece_hash)
    if err:
      #TODO use production-level error handling here
      return f"<h2>Error occurred while deleting piece:</h2> {err}"
    else:
      return redirect("/all-pieces")
  
  elif action == 'modify':
    formkeys = ['new-piece-title', 'new-piece-subtitle', 'new-piece-subsubtitle', \
                'new-piece-dedicated', 'new-piece-opus', 'new-piece-year', \
                'new-piece-instrument', 'new-piece-comment']
    if not verifyFormKeys(req_form, formkeys):
      return createHtmlAlertBox("Form fields missing, please check your input.", "Error")
    new_title       = req_form.get('new-piece-title', '')
    new_subtitle    = req_form.get('new-piece-subtitle', '')
    new_subsubtitle = req_form.get('new-piece-subsubtitle', '')
    new_dedicated   = req_form.get('new-piece-dedicated', '')
    new_opus        = req_form.get('new-piece-opus', '')
    new_year        = req_form.get('new-piece-year', '')
    new_instrument  = req_form.get('new-piece-instrument', '')
    new_comment     = req_form.get('new-piece-comment', '')
    err = Metadata().writer().updatePiece( \
      piece_hash=piece_hash, title=new_title, subtitle=new_subtitle, subsubtitle=new_subsubtitle, \
      opus=new_opus, dedicated=new_dedicated, collection_code="", year=new_year, \
      instruments=new_instrument, comment=new_comment)
    if err:
      #TODO use production-level error handling here
      return f"<h2>Error occurred while modifying piece:</h2> {err}"
    else:
      return redirect(f"/file/{piece_hash}")
    
  return redirect("/")


def get_update_collection_page(collection_code: str) -> str:
  collection = Metadata().reader().getCollection(collection_code)
  if not collection:
    return createHtmlAlertBox("Collection not found.", "Error")
  composer_code = collection.get('composer_code', '')
  if composer_code:
    composer = Metadata().reader().getComposer(composer_code)
    if composer:
      collection['composer_name'] = composer.get('knownas_name', '')
  
  return render_template("update_collection.html", collection_info=collection)


def update_collection_info(collection_code: str, req_form) -> str:
  """ This is the workflow for updating collection information. """
  verify_usr_pwd_err = AuthWeak().verifyReqFormUserPassword(req_form)
  if verify_usr_pwd_err:
    return verify_usr_pwd_err

  action = req_form.get('select-action', '')
  if action not in ['modify', 'delete']:
    return createHtmlAlertBox("Invalid action selected.", "Error")
  
  if action == 'delete':
    err = ""
    for piece in Metadata().reader().getCollectionPieces(collection_code):
      folder_hash = piece.get('folder_hash', '')
      if folder_hash and Metadata().reader().getPiece(folder_hash):
        err += Metadata().writer().rmPieceFromCollection(folder_hash, collection_code)
    err += Metadata().writer().deleteCollection(collection_code)
    if err:
      #TODO use production-level error handling here
      return f"<h2>Error occurred while deleting collection:</h2> {err}"
    else:
      return redirect("/collections")
    
  elif action == 'modify':
    formkeys = ['new-collection-title', 'new-collection-subtitle', 'new-collection-subsubtitle', \
                'new-collection-editor', 'new-collection-opus', 'new-collection-volume', \
                'new-collection-instrument', 'new-collection-description']
    if not verifyFormKeys(req_form, formkeys):
      return createHtmlAlertBox("Form fields missing, please check your input.", "Error")
    new_title       = req_form.get('new-collection-title', '')
    new_subtitle    = req_form.get('new-collection-subtitle', '')
    new_subsubtitle = req_form.get('new-collection-subsubtitle', '')
    new_editor      = req_form.get('new-collection-editor', '')
    new_opus        = req_form.get('new-collection-opus', '')
    new_volume      = req_form.get('new-collection-volume', '')
    new_instrument  = req_form.get('new-collection-instrument', '')
    new_description = req_form.get('new-collection-description', '')
    err = Metadata().writer().updateCollection( \
      collection_code=collection_code, title=new_title, subtitle=new_subtitle,
      subsubtitle=new_subsubtitle, editor=new_editor, composer_code="",
      opus=new_opus, volume=new_volume, instruments=new_instrument, description=new_description)
    if err:
      #TODO use production-level error handling here
      return f"<h2>Error occurred while modifying collection:</h2> {err}"
    else:
      return redirect(f"/collection-at/{collection_code}")
  return redirect("/")


def get_update_composer_page() -> str:
  composer_list = Metadata().reader().getAllComposers(listed_only=False)
  if not composer_list:
    return createHtmlAlertBox("No composers found in DB.", "Error")
  return render_template("update_composer.html", composer_list=composer_list)


def update_or_delete_composer(req_form) -> str:
  """ This is the workflow for unhide/hide composer or deleting composer. """
  verify_usr_pwd_err = AuthWeak().verifyReqFormUserPassword(req_form)
  if verify_usr_pwd_err:
    return verify_usr_pwd_err

  action = req_form.get('select-action', '')
  if action not in ['delete', 'hide', 'unhide']:
    return createHtmlAlertBox("Invalid action selected.", "Error")
  composer_code = req_form.get('select-composer', '')
  if not composer_code:
    return createHtmlAlertBox("No composer selected.", "Error")
  
  if action == 'delete':
    err = ""
    if 'also-delete-pieces' in req_form.keys() and req_form['also-delete-pieces'] == 'on':
      for piece in Metadata().reader().getComposerPieces(composer_code):
        folder_hash = piece.get('folder_hash', '')
        # delete piece first
        if folder_hash and Metadata().reader().getPiece(folder_hash):
          err += FileManager().deleteAllFiles(folder_hash)
          err += Metadata().writer().deletePiece(folder_hash)
    if 'also-delete-collections' in req_form.keys() and req_form['also-delete-collections'] == 'on':
      for collection in Metadata().reader().getComposerCollections(composer_code):
        collection_code = collection.get('code', '')
        if collection_code:
          # remove pieces from collection before deleting collection
          for piece in Metadata().reader().getCollectionPieces(collection_code):
            folder_hash = piece.get('folder_hash', '')
            if folder_hash and Metadata().reader().getPiece(folder_hash):
              err += Metadata().writer().rmPieceFromCollection(folder_hash, collection_code)
          err += Metadata().writer().deleteCollection(collection_code)
    err += Metadata().writer().deleteComposer(composer_code)
    if err:
      #TODO use production-level error handling here
      return f"<h2>Error occurred while deleting composer:</h2> {err}"
    else:
      return redirect("/composers")
  
  elif action == 'hide':
    err = Metadata().writer().hideComposer(composer_code)
    if err:
      #TODO use production-level error handling here
      return f"<h2>Error occurred while hiding composer:</h2> {err}"
    else:
      return redirect("/composers")
  
  elif action == 'unhide':
    err = Metadata().writer().unhideComposer(composer_code)
    if err:
      #TODO use production-level error handling here
      return f"<h2>Error occurred while unhiding composer:</h2> {err}"
    else:
      return redirect("/composers")

  return redirect("/")


#TODO
def update_file_metadata(folder_hash: str, file_title: str, req_form) -> str:
  """ This is the workflow for updating file metadata. """
  verify_usr_pwd_err = AuthWeak().verifyReqFormUserPassword(req_form)
  if verify_usr_pwd_err:
    return verify_usr_pwd_err

  new_title = req_form.get('new-file-title', '')
  new_description = req_form.get('new-file-description', '')
  err = FileManager().modifyFileMetadata(folder_hash, file_title, new_title, new_description)
  if err:
    #TODO use production-level error handling here
    return f"<h2>Error occurred while modifying file metadata:</h2> {err}"
  else:
    return redirect(f"/file/{folder_hash}")


#TODO
def delete_file(folder_hash: str, file_title: str, req_form) -> str:
  """ This is the workflow for deleting a file. """
  verify_usr_pwd_err = AuthWeak().verifyReqFormUserPassword(req_form)
  if verify_usr_pwd_err:
    return verify_usr_pwd_err

  err = FileManager().deleteFile(folder_hash, file_title)
  if err:
    #TODO use production-level error handling here
    return f"<h2>Error occurred while deleting file:</h2> {err}"
  else:
    return redirect(f"/file/{folder_hash}")


#TODO
def replace_file(folder_hash: str, file_title: str, req_form) -> str:
  pass