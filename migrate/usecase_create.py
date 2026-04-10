from metadata import Metadata
from filemanager import FileManager
from flask import render_template, request, redirect
from utilities import createHtmlAlertBox
import re, os


def render_create_composer_page() -> str:
  return render_template("new_composer.html")


def create_composer(req_form) -> str:
  formkeys = ['firstname', 'lastname', 'knownas', 'bornyear', 'diedyear']
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

  #TODO validate user name and password




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
