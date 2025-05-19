from flask import Flask, render_template, send_from_directory
from flask import redirect, request, flash, url_for
from werkzeug.utils import secure_filename
from markupsafe import escape

from metadata import Metadata
from piece_io import PieceIO
from toggle_menu import ToggleHtmlMenu
from auth import AuthWeak
from submit import ScriptSubmit

import browse, hymnus_config, hymnus_tools
import time, os

meta     = Metadata()
pieceio  = PieceIO()
weakauth = AuthWeak()

### APP starts here ###

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
@app.route("/index")
def index():
  return render_template("index.html", page_title="Hymnus Library")

@app.route("/about")
def about():
  return  render_template("about.html")

@app.route("/contact")
def contact():
  return "Contact"

@app.route("/new-composer")
def createNewComposer():
  return render_template("new_composer.html")

@app.route("/new-piece")
def createNewPiece():
  return render_template("new_piece.html",
                         composerlist=meta.getComposerCodeNameList())

@app.route("/new-collection")
def createNewCollection():
  return render_template("new_collection.html",
                         composerlist=meta.getComposerCodeNameList())

@app.route("/browse/composers")
def browseComposer():
  return browse.browsePageAtPageNumber("c", "1", "")

@app.route("/browse/composers/<currentpage>")
def browseComposerAtPage(currentpage):
  return browse.browsePageAtPageNumber("c", currentpage, "")

@app.route("/browse/collections")
def browseCollection():
  return browse.browsePageAtPageNumber("col", "1", "")

@app.route("/browse/collections/<currentpage>")
def browseCollectionAtPage(currentpage):
  return browse.browsePageAtPageNumber("col", currentpage, "")

@app.route("/browse/all-pieces")
def browseAllPieces():
  return browse.browsePageAtPageNumber("a", "1", "")

@app.route("/browse/all-pieces/<currentpage>")
def browseAllPiecesAtPage(currentpage):
  return browse.browsePageAtPageNumber("a", currentpage, "")

@app.route("/browse/works-by/<composercode>")
def browseComposerPieces(composercode):
  return browse.browsePageAtPageNumber("w", "1", composercode)

@app.route("/browse/works-by/<composercode>/<currentpage>")
def browseComposerPiecesAtPage(composercode, currentpage):
  return browse.browsePageAtPageNumber("w", currentpage, composercode)

@app.route("/collection-at/<collection_code>")
def openCollection(collection_code):
  return browse.browseCollectionAtCode(collection_code)

@app.route("/file/<folderhash>")
def openPiecePage(folderhash):
  pieceinfo = meta.getPieceMetadata(folderhash)
  filesinfo = pieceio.getPiecePageFileList(folderhash)
  if pieceinfo and filesinfo:
    return render_template("piece_files.html", \
                          piece_metadata=pieceinfo, \
                          file_metadata_list=filesinfo, \
                          has_footer="N")
  else:
    return "<h1>Page does not exist!!!</h1>"


@app.route("/search")
def searchWorks():
  return "<h1>WIP</h1>"

@app.route("/download/<folderhash>/<fname>")
def downloadFile(folderhash, fname):
  wait_time = 3
  time.sleep(wait_time)
  return send_from_directory(pieceio.getPieceFileDir(folderhash), \
                             fname, as_attachment=False)


@app.route('/addfile/<folderhash>', methods=['GET', 'POST'])
def upload_file(folderhash):
  if request.method == 'POST':
    # Check password
    if 'user' in request.form and 'password' in request.form \
      and request.form['user'] != '' and request.form['password'] != '' \
      and weakauth.validateUserPassword(request.form['user'],
                                        request.form['password']):
        pass
    else:
      return hymnus_tools.createAlertBox('Empty or wrong username and password!', 'Error')
    
    # Check file and input
    if 'file' not in request.files \
      or 'title' not in request.form \
      or 'description' not in request.form: 
      return hymnus_tools.createAlertBox('Input text or file is empty!', 'Error')
    else:
      file = request.files['file']
      title = request.form['title']
      desc = request.form['description']
      if file and file.filename and title and desc:
        filename = secure_filename(file.filename)
        if pieceio.checkFileExtension(filename):
          file.save(pieceio.getSavedFilePath(folderhash, filename))
          pieceio.addFileMetaData(folderhash, filename, title, desc)
          flash('New file successfully added.')
          return redirect(f"/file/{folderhash}")
      else:
        return hymnus_tools.createAlertBox('Input text is empty!', 'Error')

  return pieceio.getSimpleSubmitPage()


@app.route('/rmfile/<folderhash>', methods=['GET', 'POST'])
def delete_file(folderhash):
  if request.method == 'POST':
    if 'user' in request.form and 'password' in request.form \
      and request.form['user'] != '' and request.form['password'] != '' \
      and weakauth.validateUserPassword(request.form['user'],
                                    request.form['password']):
      select = request.form.get('select-file')
      if select:
        pieceio.deleteFileAndMetaData(folderhash, select)
        flash(f'File "{select}" deleted.')
        return redirect(f"/file/{folderhash}")
    else:
      return hymnus_tools.createAlertBox('Empty or wrong username and password!', 'Error')
  return pieceio.getSimpleDeletePage(folderhash)


@app.route('/submit-script', methods=['GET', 'POST'])
def submit_script():
  smt = ScriptSubmit()
  if request.method == 'POST':
    # Check password
    if 'user' in request.form and 'password' in request.form \
      and request.form['user'] != '' and request.form['password'] != '' \
      and weakauth.validateUserPassword(request.form['user'],
                                        request.form['password']):
        pass
    else:
      return hymnus_tools.createAlertBox('Empty or wrong username and password!', 'Error')
    
    # Check file and input
    if 'submitted-script' not in request.form:
      return hymnus_tools.createAlertBox('Script input doesn not exist!', 'Error')
    else:
      script = request.form['submitted-script']
      if script and script != '':
        return smt.runScript(script)
      else:
        return hymnus_tools.createAlertBox('Script is empty!', 'Error')

  return smt.getSubmitPage()


if __name__ == '__main__':
  app.run()