from metadata import Metadata
from filemanager import FileManager
from flask import request
from flask import render_template, redirect
from werkzeug.utils import secure_filename
from utilities import createHtmlAlertBox, verifyFormKeys
from auth import AuthWeak
from config import ACCEPTED_FILE_UPLOAD_EXTENSIONS, FILE_UPLOAD_WAIT_TIME
import re, os, time


def render_create_composer_page() -> str:
  return render_template("new_composer.html")


def create_composer(req_form) -> str:
  """ This is the workflow for creating a new composer.
      It validates the user credentials, checks the form fields, preprocesses the input,
      and creates the composer in the database. """
  verify_usr_pwd_err = AuthWeak().verifyReqFormUserPassword(req_form)
  if verify_usr_pwd_err:
    return verify_usr_pwd_err  

  formkeys = ['firstname', 'lastname', 'knownas', 'bornyear', 'diedyear']
  if not verifyFormKeys(req_form, formkeys):
    return createHtmlAlertBox("Form fields missing, please check your input.", "Error")
  
  firstname = req_form.get('firstname', '')
  lastname  = req_form.get('lastname', '')
  knownas   = req_form.get('knownas', '')
  bornyear  = req_form.get('bornyear', '')
  diedyear  = req_form.get('diedyear', '')
  bornyear = int(bornyear) if bornyear.isdigit() else -1
  diedyear = int(diedyear) if diedyear.isdigit() else -1

  # Preprocess the input to remove extra spaces and handle special characters
  firstname = re.sub(' +', ' ', firstname)
  firstname = re.sub(r'\s+-', '-', firstname)
  firstname = re.sub(r'-\s+', '-', firstname)
  firstname = firstname.replace("'","’")
  lastname  = re.sub(' +', ' ', lastname)
  lastname  = re.sub(r'\s+-', '-', lastname)
  lastname  = re.sub(r'-\s+', '-', lastname)
  lastname = lastname.replace("'","’")
  knownas   = re.sub(' +', ' ', knownas)
  knownas = re.sub(r'\s+-', '-', knownas)
  knownas = re.sub(r'-\s+', '-', knownas)
  knownas = knownas.replace("'","’")
  firstname = firstname.title()
  lastname  = lastname.title()
  knownas   = knownas.title()

  # Verify creation result in DB
  code_or_err = Metadata().writer().createComposer(firstname, lastname, knownas, bornyear, diedyear)
  if "already exists in DB" in code_or_err:
    return createHtmlAlertBox("Composer already created. Please check the name and try again.", "Error")
  else:
    if not Metadata().reader().getComposer(code_or_err):
      #TODO use production-level error handling here
      return f"<h2>Error occurred while creating composer, error was:</h2> {code_or_err}"
    if 'hide-composer' in req_form:
      Metadata().writer().hideComposer(code_or_err)
    else:
      Metadata().writer().unhideComposer(code_or_err)
  
  return redirect(f"/works-by/{code_or_err}")


def render_create_piece_page() -> str:
  composer_list = Metadata().reader().getAllComposers(listed_only=False)
  return render_template("new_piece.html", composer_list=composer_list)


def create_piece(req_form) -> str:
  """ This is the workflow for creating a new piece. """
  verify_usr_pwd_err = AuthWeak().verifyReqFormUserPassword(req_form)
  if verify_usr_pwd_err:
    return verify_usr_pwd_err

  formkeys = ['new-piece-title', 'new-piece-subtitle', 'new-piece-subsubtitle',
              'new-piece-dedicated', 'new-piece-year', 'new-piece-opus',
              'select-composer', 'arranger-name', 'new-piece-instrument', 'new-piece-comment']
  if not verifyFormKeys(req_form, formkeys):
    return createHtmlAlertBox("Form fields missing, please check your input.", "Error")
  
  if ('check-is-arranged-piece' not in req_form and 'check-is-not-arranged-piece' not in req_form) or \
     ('check-is-arranged-piece'     in req_form and 'check-is-not-arranged-piece'     in req_form) or \
     ('check-is-arranged-piece'     in req_form and 'select-arranger' not in req_form \
                                                and 'arranger-name'   not in req_form):
    return createHtmlAlertBox("Please specify whether the piece is an arranged piece or not."
                              "If yes, choose the arranger from the list or provide the name.", "Error")
    
  if not req_form['new-piece-title'] or not req_form['select-composer']:
    return createHtmlAlertBox("Please provide the piece title and composer.", "Error")
  
  title       = req_form.get('new-piece-title', '')
  subtitle    = req_form.get('new-piece-subtitle', '')
  subsubtitle = req_form.get('new-piece-subsubtitle', '')
  dedicated   = req_form.get('new-piece-dedicated', '')
  year        = req_form.get('new-piece-year', '')
  opus        = req_form.get('new-piece-opus', '')
  composer_code = req_form.get('select-composer', '')
  arranger_name = ""
  arranger_code = ""
  if 'check-is-arranged-piece' in req_form:
    if 'select-arranger' in req_form and req_form['select-arranger']:
      arranger_code = req_form['select-arranger']
    elif 'arranger-name' in req_form and req_form['arranger-name']:
      arranger_name = req_form['arranger-name']
  instrument  = req_form.get('new-piece-instrument', '')
  comment     = req_form.get('new-piece-comment', '')

  # Verify creation result in DB
  hash_or_err = Metadata().writer().createPiece( \
    composer_code=composer_code, title=title, subtitle=subtitle, \
    subsubtitle=subsubtitle, opus=opus, dedicated=dedicated, \
    arranger_code=arranger_code, arranger_name=arranger_name, collection_code="", \
    year=year, instruments=instrument, comment=comment)
  
  if 'already exists in DB' in hash_or_err:
    return createHtmlAlertBox("Piece already exists. Please check your input.", "Error")
  
  if not Metadata().reader().getPiece(hash_or_err):
    #TODO use production-level error handling here
    return f"<h2>Error occurred while creating piece, error was:</h2> {hash_or_err}"
  
  return redirect(f"/file/{hash_or_err}")


def render_create_collection_page() -> str:
  """ This is the workflow for creating a new collection. """
  composer_list = Metadata().reader().getAllComposers(listed_only=False)
  return render_template("new_collection.html", composer_list=composer_list)


def create_collection(req_form) -> str:
  check_usr_pwd_err = AuthWeak().verifyReqFormUserPassword(req_form)
  if check_usr_pwd_err:
    return check_usr_pwd_err

  formkeys = ['new-collection-title', 'new-collection-subtitle', 'new-collection-subsubtitle', \
              'new-collection-editor', 'new-collection-opus', 'new-collection-volume', \
              'new-collection-instrument', 'new-collection-description']
  
  if not verifyFormKeys(req_form, formkeys):
    return createHtmlAlertBox("Form fields missing, please check your input.", "Error")

  title       = req_form.get('new-collection-title', '')
  subtitle    = req_form.get('new-collection-subtitle', '')
  subsubtitle = req_form.get('new-collection-subsubtitle', '')
  editor      = req_form.get('new-collection-editor', '')
  opus        = req_form.get('new-collection-opus', '')
  volume      = req_form.get('new-collection-volume', '')
  instrument  = req_form.get('new-collection-instrument', '')
  description = req_form.get('new-collection-description', '')
  composer_code = ""
  if 'collection-has-composer' in req_form and 'select-composer' in req_form:
    composer_code = req_form['select-composer']
    if not Metadata().reader().getComposer(composer_code):
      composer_code = "" # Invalid composer code, ignore it

  # Verify creation result in DB  
  hash_or_err = Metadata().writer().createCollection( \
    title=title, subtitle=subtitle, subsubtitle=subsubtitle, editor=editor, \
    composer_code=composer_code, opus=opus, volume=volume, \
    instruments=instrument, description=description)
  
  if "already exists in DB" in hash_or_err:
    return createHtmlAlertBox("Collection already created. Please check the input and try again.", "Error")
  else:
    if not Metadata().reader().getCollection(hash_or_err):
      #TODO use production-level error handling here
      return f"<h2>Error occurred while creating collection, error was:</h2> {hash_or_err}"
  
  return redirect(f"/collection-at/{hash_or_err}")


def add_piece_file(folder_hash, req_form, req_file) -> str:
  """ This is the workflow for adding a piece file. """
  verify_usr_pwd_err = AuthWeak().verifyReqFormUserPassword(req_form)
  if verify_usr_pwd_err:
    return verify_usr_pwd_err
  
  if not verifyFormKeys(req_form, ['title', 'description']) or \
     not 'file' in req_file:
    return createHtmlAlertBox("Form fields missing, please check your input.", "Error")
  if 'file' not in req_file:
    return createHtmlAlertBox("No file uploaded, please check your input.", "Error")
  file = req_file['file']
  title = req_form['title']
  desc = req_form['description']

  if not file or not title or not desc:
    return createHtmlAlertBox("Please provide the file, title and description.", "Error")
  
  filename = secure_filename(file.filename)
  ext = os.path.splitext(filename)[-1].lower()
  if ext not in ACCEPTED_FILE_UPLOAD_EXTENSIONS:
    return createHtmlAlertBox(f"Uploaded file type \"{ext}\" not accepted.", "Error")
  time.sleep(FILE_UPLOAD_WAIT_TIME)

  err = FileManager().uploadFile(folder_hash, filename, title, desc, file)
  if err:
    return createHtmlAlertBox(f"Failed to upload file: {err}", "Error")
  
  return redirect(f"/file/{folder_hash}")


def render_add_file_page(folder_hash) -> str:
  piece = Metadata().reader().getPiece(folder_hash)
  if not piece:
    return createHtmlAlertBox("Piece does not exist. Cannot add file.", "Error")
  return render_template("upload_piece_file.html", \
                         folder_hash=folder_hash, piece_title=piece.get('title', '!!??'))
