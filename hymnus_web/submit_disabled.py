import os, sys, shlex, subprocess, time
from piece_io import PieceIO
from metadata import Metadata
from auth import AuthWeak
from hymnus_tools import createAlertBox, logUserActivity
from flask import redirect, request, render_template
from werkzeug.utils import secure_filename
import hymnus_config

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

