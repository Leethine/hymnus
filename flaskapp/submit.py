import os, sys, shlex, subprocess
from flask import Flask, render_template, send_from_directory
from flask import redirect, request, flash, url_for

class ScriptSubmit():
  def __init__(self):
    self.__cmd =   ""
    self.__result = ""
    self.ALLOWED_CMD = ['script/new-composer.sh', 'script/new-collection.sh', 'script/new-piece.sh',
                        'script/delete-composer.sh', 'script/delete-collection.sh', 'script/delete-piece.sh']
  
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


class FileSubmit():
  def __init__(self):
    pass
