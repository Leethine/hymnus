import os, sys, shlex, subprocess, time
from piece_io import PieceIO
from metadata import Metadata
from auth import AuthWeak
from hymnus_tools import createAlertBox, logUserActivity
from flask import redirect, request, render_template
from werkzeug.utils import secure_filename
import hymnus_config

def checkUserAndPasswd(req_form):
  weakauth = AuthWeak()
  if 'user' in req_form and 'password' in req_form \
    and req_form['user'] != '' and req_form['password'] != '' \
    and weakauth.validateUserPassword(req_form['user'],
                                      req_form['password']):
    return True
  else:
    return False


class FileSubmit():
  def __init__(self, folder_hash: str):
    self.__hash = folder_hash
    self.__io = PieceIO()
    meta = Metadata()
    pieceinfo = meta.getPieceMetadata(self.__hash)
    if pieceinfo["opus"] == "" or pieceinfo["opus"] == "N/A":
      self.__work_title = pieceinfo["title"]
    else:
      self.__work_title = pieceinfo["title"] + ", " + pieceinfo["opus"]

  def getSubmitPage(self) -> str:
    return render_template('file_submit.html', piece_title=self.__work_title, \
                            folder_hash=self.__hash)
  
  def getDeletePage(self) -> str:
    title_list = []
    for item in self.__io.getFileMetaData(self.__hash):
      if item and 'headline' in item.keys():
        title_list.append(item['headline'])
    return render_template('file_delete.html', piece_title=self.__work_title, \
                            file_title_list=title_list, folder_hash=self.__hash)
  
  def getReplacePage(self) -> str:
    title_list = []
    for item in self.__io.getFileMetaData(self.__hash):
      if item and 'headline' in item.keys():
        title_list.append(item['headline'])
    return render_template('file_replace.html', piece_title=self.__work_title, \
                            file_title_list=title_list, folder_hash=self.__hash)
  
  def getModifyPage(self) -> str:
    title_list = []
    for item in self.__io.getFileMetaData(self.__hash):
      if item and 'headline' in item.keys():
        title_list.append(item['headline'])
    return render_template('file_modify.html', piece_title=self.__work_title, \
                            file_title_list=title_list, folder_hash=self.__hash)

  def uploadFile(self, req_files, req_form):
    # Check file input and form input
    if 'file' not in req_files \
      or 'title' not in req_form \
      or 'description' not in req_form:
      return createAlertBox('Input text or file not exist!', 'Error')
    else:
      file = req_files['file']
      title = req_form['title']
      desc = req_form['description']
      if file and file.filename and title and desc:
        filename = secure_filename(file.filename)
        if self.__io.checkFileExtension(filename):
          time.sleep(hymnus_config.FILE_UPLOAD_WAIT_TIME)
          if not os.path.isdir(self.__io.getPieceFileDir(self.__hash)):
            os.makedirs(self.__io.getPieceFileDir(self.__hash), exist_ok=True)
          file.save(self.__io.getSavedFilePath(self.__hash, filename))
          self.__io.addFileMetaData(self.__hash, filename, title, desc)
          logUserActivity(req_form['user'], f"Created file: {self.__hash} --> {title}")
          return redirect(f"/file/{self.__hash}")
      else:
        return createAlertBox('Input text is empty!', 'Error')
  
  def deleteFile(self, req_form) -> None:
    select = req_form.get('select-file')
    if select:
      self.__io.deleteFileAndMetaData(self.__hash, select)
      logUserActivity(request.form['user'], f"Deleted file: {self.__hash} --> {select}")
    return redirect(f"/file/{self.__hash}")

  def replaceFile(self, req_files, req_form) -> None:
    if 'file' not in req_files or 'select-file' not in req_form:
      return createAlertBox('Selected or uploaded file not exist!', 'Error')
    else:
      file = req_files['file']
      selected_title = req_form['select-file']
      if file and file.filename and selected_title:
        filename = secure_filename(file.filename)
        if self.__io.checkFileExtension(filename):
          time.sleep(hymnus_config.FILE_UPLOAD_WAIT_TIME)
          file.save(self.__io.getSavedFilePath(self.__hash, filename))
          self.__io.updateFileName(self.__hash, filename, selected_title)
          logUserActivity(req_form['user'], f"Replaced file: {self.__hash} --> {selected_title}")
          return redirect(f"/file/{self.__hash}")
      return createAlertBox('Selected file or input is empty!', 'Error')

  def modifyFileMetadata(self, req_form) -> None:
    if 'select-file' not in req_form \
      or 'title' not in req_form \
      or 'description' not in req_form:
      return createAlertBox('Input field not exist!', 'Error')
    else:
      oldtitle = req_form['select-file']
      newtitle = req_form['title']
      newdesc = req_form['description']
      # Update metadata
      time.sleep(hymnus_config.FILE_UPLOAD_WAIT_TIME)
      self.__io.updateFileMetadata(self.__hash, oldtitle, newtitle, newdesc)
      logUserActivity(req_form['user'], f"Modified file: {self.__hash} --> {oldtitle}")
      return redirect(f"/file/{self.__hash}")