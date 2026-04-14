from metadata import Metadata
from filemanager import FileManager
from flask import request
from flask import render_template, redirect
from werkzeug.utils import secure_filename
from utilities import createHtmlAlertBox, verifyFormKeys
from auth import AuthWeak
from config import ACCEPTED_FILE_UPLOAD_EXTENSIONS, FILE_UPLOAD_WAIT_TIME
import re, os, time


def get_add_piece_to_collection_page(collection_code: str) -> str:
  collection = Metadata().reader().getCollection(collection_code)
  if not collection:
    return createHtmlAlertBox("Collection not found.", "Error")
  title = collection.get('title', 'Unknown Collection')
  opus = collection.get('opus', '')
  if opus:
    title += f" , {opus}"  
  return render_template("update_add_to_collection.html", collection_title=title)


def get_rm_piece_from_collection_page(collection_code: str) -> str:
  collection = Metadata().reader().getCollection(collection_code)
  if not collection:
    return createHtmlAlertBox("Collection not found.", "Error")
  title = collection.get('title', 'Unknown Collection')
  opus = collection.get('opus', '')
  if opus:
    title += f" , {opus}"  
  return render_template("update_rm_from_collection.html", collection_title=title)


def add_piece_to_collection(collection_code: str, req_form) -> str:
  """ This is the workflow for adding pieces to an existing collection. """
  verify_usr_pwd_err = AuthWeak().verifyReqFormUserPassword(req_form)
  if verify_usr_pwd_err:
    return verify_usr_pwd_err  

  formkeys = ['list-of-pieces']
  if not verifyFormKeys(req_form, formkeys):
    return createHtmlAlertBox("Form fields missing, please check your input.", "Error")
  
  list_of_pieces = req_form.get('list-of-pieces', '')
  piece_hashes = list_of_pieces.split(',')

  err = ""
  for piece_hash in piece_hashes:
    piece_hash = piece_hash.replace(' ', '')
    if Metadata().reader().getPiece(piece_hash):
      # Ignore non-existing pieces
      err += Metadata().writer().addPieceToCollection(piece_hash, collection_code)
  if err:
    #TODO use production-level error handling here
    return f"<h2>Error occurred while updating collection:</h2> {err}"
  else:
    return redirect(f"/collection-at/{collection_code}")
  

def rm_piece_from_collection(collection_code: str, req_form) -> str:
  """ This is the workflow for removing a piece from a collection. """
  verify_usr_pwd_err = AuthWeak().verifyReqFormUserPassword(req_form)
  if verify_usr_pwd_err:
    return verify_usr_pwd_err  

  formkeys = ['piece-hash']
  if not verifyFormKeys(req_form, formkeys):
    return createHtmlAlertBox("Form fields missing, please check your input.", "Error")
  
  piece_hash = req_form.get('piece-hash', '')
  err = ""
  if Metadata().reader().getPiece(piece_hash):
    err = Metadata().writer().rmPieceFromCollection(piece_hash, collection_code)
  if err:
    #TODO use production-level error handling here
    return f"<h2>Error occurred while updating collection:</h2> {err}"
  else:
    return redirect(f"/collection-at/{collection_code}")
  

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
    return f"<h2>Error occurred while updating piece information:</h2> {err}"
  else:
    return redirect(f"/file/{piece_hash}")


