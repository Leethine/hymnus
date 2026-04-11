import usecase_display, usecase_create

from flask import Flask, request, render_template, send_file, abort

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
@app.route("/index")
def index():
  return render_template("front_page.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/contact")
def contact():
  return render_template("contact.html")

@app.route("/composers")
def display_composers():
  return usecase_display.render_composer_list()

@app.route("/composers/<int:page>")
def display_composers_paginated(page):
  return usecase_display.render_composer_list(page=page)

@app.route("/collections")
def display_collections():
  return usecase_display.render_collection_list()

@app.route("/collections/<int:page>")
def display_collections_paginated(page):
  return usecase_display.render_collection_list(page=page)

@app.route("/all-pieces")
def display_all_pieces():
  return usecase_display.render_piece_list()

@app.route("/all-pieces/<int:page>")
def display_all_pieces_paginated(page):
  return usecase_display.render_piece_list(page=page)

@app.route("/works-by/<string:composer_code>")
def display_composer_pieces(composer_code):
  html = usecase_display.render_composer_piece_list(composer_code)
  if html:
    return html
  else:
    abort(404)

@app.route("/works-by/<string:composer_code>/<int:page>")
def display_composer_pieces_paginated(composer_code, page):
  html = usecase_display.render_composer_piece_list(composer_code, page=page)
  if html:
    return html
  else:
    abort(404)

@app.route("/collection-at/<string:collection_code>")
def display_collection_pieces(collection_code):
  html = usecase_display.render_collection_piece_list(collection_code)
  if html:
    return html
  else:
    abort(404)

@app.route("/file/<string:folder_hash>")
def display_piece_files(folder_hash):
  html = usecase_display.render_piece_files(folder_hash)
  if html:
    return html
  else:
    abort(404)

@app.route("/download/<string:folder_hash>/<string:filename>")
def download_piece_file(folder_hash, filename):
  file_path = usecase_display.get_download_file_path(folder_hash, filename)
  if file_path:
    return send_file(file_path, as_attachment=False)
  else:
    abort(502)

@app.route("/new-composer", methods=['GET', 'POST'])
def new_composer():
  if request.method == 'POST':
    return usecase_create.create_composer(request.form)
  return usecase_create.render_create_composer_page()

@app.route("/new-piece", methods=['GET', 'POST'])
def new_piece():
  if request.method == 'POST':
    return usecase_create.create_piece(request.form)
  return usecase_create.render_create_piece_page()
