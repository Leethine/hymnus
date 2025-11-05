from flask import Flask, render_template, send_from_directory
from flask import redirect, request, url_for
from werkzeug.utils import secure_filename
from markupsafe import escape
import time

from metadata import Metadata
from piece_io import PieceIO
from submit import FileSubmit, checkUserAndPasswd
from create import NewComposerCreator, NewPieceCreator, NewCollectionCreator
from hymnus_tools import createAlertBox
import browse, hymnus_config

meta     = Metadata()
pieceio  = PieceIO()

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

@app.route("/new-composer", methods=['GET', 'POST'])
def createNewComposer():
  nc = NewComposerCreator()
  if request.method == 'POST':
    # Check username and password
    if not checkUserAndPasswd(request.form):
      return createAlertBox('Wrong username and password!', 'Error')
    # username and password ok, proceed
    return nc.submitHtmlForm(request.form)
  # Default page
  return nc.getCreationPage()

@app.route("/new-piece", methods=['GET', 'POST'])
def createNewPiece():
  np = NewPieceCreator()
  if request.method == 'POST':
    # Check username and password
    if not checkUserAndPasswd(request.form):
      return createAlertBox('Wrong username and password!', 'Error')
    # username and password ok, proceed
    return np.submitHtmlForm(request.form)
  # Default page
  return np.getCreationPage()

@app.route("/new-collection", methods=['GET', 'POST'])
def createNewCollection():
  nc = NewCollectionCreator()
  if request.method == 'POST':
    # Check username and password
    if not checkUserAndPasswd(request.form):
      return createAlertBox('Wrong username and password!', 'Error')
    # username and password ok, proceed
    return nc.submitHtmlForm(request.form)
  # Default page
  return nc.getSubmitPage()

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
  time.sleep(hymnus_config.FILE_DOWNLOAD_WAIT_TIME)
  return send_from_directory(pieceio.getPieceFileDir(folderhash), \
                             fname, as_attachment=False)

@app.route('/addfile/<folderhash>', methods=['GET', 'POST'])
def upload_file(folderhash):
  fs = FileSubmit(folderhash)
  if request.method == 'POST':
    # Check username and password
    if not checkUserAndPasswd(request.form):
      return createAlertBox('Wrong username and password!', 'Error')
    # username and password ok, upload
    return fs.uploadFile(request.files, request.form)
  # Default page
  #return fs.getSubmitPage()
  return fs.getSubmitPage()

@app.route('/rmfile/<folderhash>', methods=['GET', 'POST'])
def delete_file(folderhash):
  fs = FileSubmit(folderhash)
  if request.method == 'POST':
    # Check username and password
    if not checkUserAndPasswd(request.form):
      return createAlertBox('Wrong username and password!', 'Error')
    # username and password ok, delete file
    return fs.deleteFile(request.form)
  # Default page
  return fs.getDeletePage()

@app.route('/replacefile/<folderhash>', methods=['GET', 'POST'])
def replace_file(folderhash):
  fs = FileSubmit(folderhash)
  if request.method == 'POST':
    # Check username and password
    if not checkUserAndPasswd(request.form):
      return createAlertBox('Wrong username and password!', 'Error')
    # username and password ok, delete file
    return fs.replaceFile(request.files, request.form)
  # Default page
  return fs.getReplacePage()

@app.route('/mdfmetadata/<folderhash>', methods=['GET', 'POST'])
def modify_file_metadata(folderhash):
  fs = FileSubmit(folderhash)
  if request.method == 'POST':
    # Check username and password
    if not checkUserAndPasswd(request.form):
      return createAlertBox('Wrong username and password!', 'Error')
    # username and password ok, delete file
    return fs.modifyFileMetadata(request.form)
  # Default page
  return fs.getModifyPage()

"""
@app.route('/submit-script', methods=['GET', 'POST'])
def submit_script():
  smt = ScriptSubmit()
  if request.method == 'POST':
    # Check username and password
    if not checkUserAndPasswd(request.form):
      return createAlertBox('Wrong username and password!', 'Error')
    # If check username and password ok, submit script
    return smt.submitScript(request.form)
  # Default page
  return smt.getSubmitPage()
"""

if __name__ == '__main__':
  app.run()