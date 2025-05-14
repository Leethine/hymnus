from flask import Flask, render_template, send_from_directory
from flask import redirect, request, flash, url_for
from werkzeug.utils import secure_filename
from markupsafe import escape
import metadata, browse, piece_io, toggle_menu, config
import time, os

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
                         composerlist=metadata.getComposerCodeNameList())

@app.route("/new-collection")
def createNewCollection():
  return render_template("new_collection.html",
                         composerlist=metadata.getComposerCodeNameList())

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
  pieceinfo = metadata.getPieceMetadata(folderhash)
  filesinfo = piece_io.getFilePageInfo(folderhash)
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
  return send_from_directory(piece_io.getPieceFilePath(folderhash), \
                             fname, as_attachment=False)


@app.route('/addfile/<folderhash>', methods=['GET', 'POST'])
def upload_file(folderhash):
  if request.method == 'POST':
    if 'file' not in request.files \
      or 'title' not in request.form \
      or 'description' not in request.form: 
      flash('Missing input data', 'error')
      return redirect(request.url)
    else:
      file = request.files['file']
      title = request.form['title']
      desc = request.form['description']
      if file and piece_io.checkInputForm(file.filename, title, desc):
        filename = secure_filename(file.filename)
        if piece_io.checkFileExtension(filename):
          file.save(os.path.join(piece_io.getPieceFilePath(folderhash), filename))
          piece_io.addFileMetaData(folderhash, filename, title, desc)
          flash('New file added.')
          return redirect(f"/file/{folderhash}")
      else:
        flash('Empty input field!', 'error')
        return redirect(request.url)
  return piece_io.getSimpleSubmitPage()


@app.route('/rmfile/<folderhash>', methods=['GET', 'POST'])
def delete_file(folderhash):
  if request.method == 'POST':
    select = request.form.get('select-file')
    if select:
      piece_io.deleteFileAndMetaData(folderhash, select)
      flash(f'File "{select}" deleted.')
      return redirect(f"/file/{folderhash}")
  return piece_io.getSimpleDeletePage(folderhash)

@app.route('/addfiletest2', methods=['GET', 'POST'])
def upload_file2():
  if request.method == 'POST':
    if 'file' not in request.files:
      flash('No file part', 'error')
      return redirect(request.url)
    file = request.files['uploaded-file']
    if file.filename == '':
      flash('No selected file', 'error')
      return redirect(request.url)
    if file:
      filename = secure_filename(file.filename)
      file.save(os.path.join("/home/lizian/Projects/hymnus/flaskapp/hymnus_env/upload", filename))
      return redirect(url_for('searchWorks'))
      #return request.form['file-title'] + "\n" + request.form['file-description']
  return piece_io.getSubmitPage()

if __name__ == '__main__':
  app.run()