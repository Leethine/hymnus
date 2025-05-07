from flask import Flask, render_template, send_from_directory
from flask import redirect, request
from markupsafe import escape
import metadata, browse, piece_io, html_basic
import time

app = Flask(__name__)

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
                         composerlist_dict=str(metadata.getComposerCodeNameList()))

@app.route("/new-collection")
def createNewCollection():
  return render_template("new_collection.html",
                         composerlist_dict=str(metadata.getComposerCodeNameList()))

@app.route("/browse/<browsetype>")
def browseByType(browsetype):
  html = {"Table": "", "Pagination": ""}
  title = ""
  page = {}
  if browsetype == "composers":
    title = "Composers"
    html = browse.browseComposers(pagenumber=1, items_per_page=20)
    page = html_basic.getPageContent("c")
  elif browsetype == "collections":
    title = "Collections"
    html = browse.browseCollections(pagenumber=1, items_per_page=40)
    page = html_basic.getPageContent("col")
  elif browsetype == "all-pieces":
    title = "Pieces"
    html = browse.browseWorks(pagenumber=1, items_per_page=100)
    page = html_basic.getPageContent("p")
  else:
    return f"<h2>Invalid URL \"/{browsetype}\"</h2>"

  return render_template("item_list.html", \
    page_title=f"{title} • Hymnus Library", \
    list_items_page_content=page, \
    list_items_table=html["Table"], \
    list_items_pagination=html["Pagination"])

@app.route("/browse/<browsetype>/<pagenumber>")
def browseByTypeAndPage(browsetype, pagenumber):
  if not browsetype in ["composers","all-pieces","collections"]:
    return f"<h2>Invalid URL \"/{browsetype}/{pagenumber}\"</h2>"
  if not str(pagenumber).isdigit():
    return f"<h2>Invalid page number: {pagenumber}</h2>"

  html = {"Table": "", "Pagination": ""}
  title = ""
  page = {}
  if browsetype == "composers":
    title = "Composers"
    html = browse.browseComposers(pagenumber=int(pagenumber), items_per_page=20)
    page = html_basic.getPageContent("c")
    page["url_composers"] = "browse/composers"
  elif browsetype == "collections":
    title = "Collections"
    html = browse.browseCollections(pagenumber=int(pagenumber), items_per_page=40)
    page = html_basic.getPageContent("col")
    page["url_collections"] = "browse/collections"
  elif browsetype == "all-pieces":
    title = "Pieces"
    html = browse.browseWorks(pagenumber=int(pagenumber), items_per_page=100)
    page = html_basic.getPageContent("p")
    page["url_allpieces"] = "browse/all-pieces"
  else:
    return f"<h2>Invalid URL \"/{browsetype}/{pagenumber}\"</h2>"

  return render_template("item_list.html", \
    page_title=f"{title} • Hymnus Library", \
    list_items_page_content=page, \
    list_items_table=html["Table"], \
    list_items_pagination=html["Pagination"])

@app.route("/works-by/<composer_code>")
def composerWorks(composer_code):
  page = html_basic.getPageContent("NA")
  composer = metadata.getComposerMetadata(composer_code)
  page["headline"] = "List of works by " + composer["AbbrName"]
  page["description"] = "<p><b>" + composer["ShortName"] + "</b><br>" \
                      + composer["LongName"] + " (" + composer["Year"] + ")</p>"
  
  if metadata.composerHasWorks(composer_code):
    html = browse.browseWorks(composer_code=composer_code, pagenumber=1)
    return render_template("item_list.html", \
      page_title=composer["AbbrName"] + " • Hymnus Library", \
      list_items_page_content=page, \
      list_items_table=html["Table"], \
      list_items_pagination=html["Pagination"])
  else:
    html = {}
    html["Table"] = "<h4>No works found.</h4>"
    html["Pagination"] = ""
    return render_template("item_list.html", \
      page_title=composer["AbbrName"] + " • Hymnus Library", \
      list_items_page_content=page, \
      list_items_table=html["Table"], \
      list_items_pagination=html["Pagination"])
    

@app.route("/works-by/<composer_code>/<pagenumber>")
def composerWorksPagination(composer_code, pagenumber):
  if not str(pagenumber).isdigit():
    return f"Invalid page number: {pagenumber}"
  html = browse.browseWorks(composer_code=composer_code, pagenumber=int(pagenumber))

  page = html_basic.getPageContent("NA")
  composer = metadata.getComposerMetadata(composer_code)
  page["headline"] = "List of works by " + composer["AbbrName"]
  page["description"] = "<p></b>" + composer["ShortName"] + "</p></b><br>" \
                      + "<p>" + composer["LongName"] + "</p><br>" \
                      + "<p>" + composer["Year"] + "</p><br>"

  return render_template("item_list.html", \
    page_title=composer["AbbrName"] + " • Hymnus Library", \
    list_items_page_content=page, \
    list_items_table=html["Table"], \
    list_items_pagination=html["Pagination"])


@app.route("/file/<folderhash>")
def openPiecePage(folderhash):
  pieceinfo = metadata.getPieceMetadata(folderhash)
  filesinfo = piece_io.getFileInfo(folderhash)
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


if __name__ == '__main__':
  app.run()