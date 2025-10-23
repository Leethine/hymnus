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

class ScriptSubmit():
  def __init__(self):
    self.__cmd =   ""
    self.__result = ""
    self.ALLOWED_CMD = ['script/new-composer.sh', 'script/new-collection.sh',
                        'script/new-piece.sh', 'script/delete-composer.sh',
                        'script/delete-collection.sh', 'script/delete-piece.sh',
                        'script/add-to-collection.sh', 'script/rm-from-collection.sh',
                        'script/enable-composer.sh']
  
  def getSubmitPage(self) -> str:
    return '''
      <!doctype html>
      <title>Submit script</title>
      <h1>Submit script</h1>
      <form method="post" enctype="multipart/form-data">
        <textarea type="text" name="submitted-script" rows="4" placeholder="script here"></textarea>
        <br>
        <input type="text" name="user" placeholder="User Name">
        <input type="password" name="password" placeholder="Password">
        <br>
        <input type="submit" value="Upload">
      </form>
    '''

  def runScript(self, script: str) -> str:
    if 'HYMNUS_DB' not in os.environ.keys():
      return "$HYMNUS_DB not defined"
    if 'HYMNUS_FS' not in os.environ.keys():
      return "$HYMNUS_FS not defined"
    if 'DATAPATH' not in os.environ.keys():
      #TODO change env variable name
      return "$DATAPATH not defined"
    if 'HYMNUS_ROOT' not in os.environ.keys():
      #TODO change env variable name
      return "$HYMNUS_ROOT not defined"
    
    arglist = shlex.split(script)
    self.__cmd = ' '.join(arglist)
    if len(arglist) > 1 and arglist[0] in self.ALLOWED_CMD:
      subprocess.os.chdir(os.environ['HYMNUS_ROOT'])
      try:
        out = subprocess.run(arglist, capture_output=True, timeout=3)
        self.__result = out.stderr.decode('utf-8') + "<br>" + out.stdout.decode('utf-8')
      except subprocess.TimeoutExpired:
        self.__result = "Timeout..."
    else:
      self.__result = "Not allowed, nothing done."
    return self.__cmd + "<br><br<br><br>" + self.__result
  
  def submitScript(self, req_form):
    # Check input
    if 'submitted-script' not in req_form:
      return createAlertBox('Script input doesn not exist!', 'Error')
    else:
      # Run script
      script = req_form['submitted-script']
      if script and script != '':
        logUserActivity(req_form['user'], f"Run script: \n{script}")
        return self.runScript(script)
      else:
        return createAlertBox('Script is empty!', 'Error')


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

  def getPrettySubmitPage(self) -> str:
    return render_template('file_submit.html', piece_title=self.__work_title, \
                            folder_hash=self.__hash)
  
  def getPrettyDeletePage(self) -> str:
    title_list = []
    for item in self.__io.getFileMetaData(self.__hash):
      if item and 'headline' in item.keys():
        title_list.append(item['headline'])
    return render_template('file_delete.html', piece_title=self.__work_title, \
                            file_title_list=title_list, folder_hash=self.__hash)
  
  def getPrettyReplacePage(self) -> str:
    title_list = []
    for item in self.__io.getFileMetaData(self.__hash):
      if item and 'headline' in item.keys():
        title_list.append(item['headline'])
    return render_template('file_replace.html', piece_title=self.__work_title, \
                            file_title_list=title_list, folder_hash=self.__hash)
  
  def getPrettyModifyPage(self) -> str:
    title_list = []
    for item in self.__io.getFileMetaData(self.__hash):
      if item and 'headline' in item.keys():
        title_list.append(item['headline'])
    return render_template('file_modify.html', piece_title=self.__work_title, \
                            file_title_list=title_list, folder_hash=self.__hash)

  def getUglySubmitPage(self) -> str:
    return '''
      <!doctype html>
      <title>Upload new File</title>
      <h1>Upload new File</h1>
      <form method="post" enctype="multipart/form-data">
        <input type="file" name="file" id="file-upload">
        <br>
        <input type="text" name="title" placeholder="File title">
        <br>
        <textarea type="text" name="description" rows="3">File description</textarea>
        <br>
        <input type="text" name="user" placeholder="User Name">
        <input type="password" name="password" placeholder="Password">
        <br>
        <input type="submit" value="Upload">
      </form>
      <script>
      const uploadFile = document.getElementById("file-upload");
      uploadFile.onchange = function() {
        if (this.files.length > 0) {
          var filesize = ((this.files[0].size/1024)/1024).toFixed(4);
          if (filesize > 5) {
            alert("File too big! (> 5MB)");
            this.value = "";
          }
        }
      };
      </script>
    '''

  def getUglyDeletePage(self) -> str:
    data = self.__io.getFileMetaData(self.__hash)
    HTMLFORM = '''
      <!doctype html>
      <title>Delete File</title>
      <h1>Delete File</h1>
      <form method="post" enctype="multipart/form-data">
        <select name="select-file" id="select-file">
    '''
    for item in data:
      if item and 'headline' in item.keys():
        HTMLFORM += "<option>" + item['headline'] + "</option>"  
    HTMLFORM += '</select><br>'
    HTMLFORM += '<input type="text" name="user" placeholder="User Name">'
    HTMLFORM += '<input type="password" name="password" placeholder="Password">'
    HTMLFORM += '<br><input type="submit" value="Delete"></form>'
    return HTMLFORM

  def getUglyModifyPage(self) -> str:
    HTMLFORM1 = '''
      <!doctype html>
      <title>Modify File Metadata</title>
      <h1>Modify the Metadata of an Exisiting File</h1>
      <form method="post" enctype="multipart/form-data">
        
        Select which file to modify: 
        <select name="select-file" id="select-file">
    '''
    HTMLFORM_OPTIONS = ""
    data = self.__io.getFileMetaData(self.__hash)
    for item in data:
      if item and 'headline' in item.keys():
        HTMLFORM_OPTIONS += "<option>" + item['headline'] + "</option>"  
    HTMLFORM2 = '''
        </select>
        <br><br>
        <p>New title</p>
        <input type="text" name="title" placeholder="Leave it untouched if no modification">
        <br>
        <p>New description</p>
        <textarea type="text" name="description" rows="3" placeholder="Leave it untouched if no modification"></textarea>
        <br>
        <input type="text" name="user" placeholder="User Name">
        <input type="password" name="password" placeholder="Password">
        <br>
        <input type="submit" value="Upload">
      </form>
    '''
    return HTMLFORM1 + HTMLFORM_OPTIONS + HTMLFORM2

  def getUglyReplacePage(self) -> str:
    HTMLFORM1 = '''
      <!doctype html>
      <title>Replace File</title>
      <h1>Replace an old file with a new one</h1>
      <form method="post" enctype="multipart/form-data">
        
        Select which file to replace: 
        <select name="select-file" id="select-file">
    '''
    HTMLFORM_OPTIONS = ""
    data = self.__io.getFileMetaData(self.__hash)
    for item in data:
      if item and 'headline' in item.keys():
        HTMLFORM_OPTIONS += "<option>" + item['headline'] + "</option>"  
    HTMLFORM2 = '''
        </select>
        <br><br>
        <input type="file" name="file" id="file-upload">
        <br>
        
        <input type="text" name="user" placeholder="User Name">
        <input type="password" name="password" placeholder="Password">
        <br>
        <input type="submit" value="Upload">
      </form>
      <script>
      const uploadFile = document.getElementById("file-upload");
      uploadFile.onchange = function() {
        if (this.files.length > 0) {
          var filesize = ((this.files[0].size/1024)/1024).toFixed(4);
          if (filesize > 5) {
            alert("File too big! (> 5MB)");
            this.value = "";
          }
        }
      };
      </script>
    '''
    return HTMLFORM1 + HTMLFORM_OPTIONS + HTMLFORM2

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