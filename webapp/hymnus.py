import usecase_display, usecase_create, usecase_modify

from flask import Flask, request, render_template, send_file, abort

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
@app.route("/index")
def index():
  if not usecase_display.check_setup():
    return render_template("front_page_nosetup.html")
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

@app.route("/search", methods=['GET', 'POST'])
def search_piece():
  if request.method == 'GET':
    return usecase_display.render_search_result(request.args)
  return usecase_display.render_search_page()


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

@app.route("/new-collection", methods=['GET', 'POST'])
def new_collection():
  if request.method == 'POST':
    return usecase_create.create_collection(request.form)
  return usecase_create.render_create_collection_page()

@app.route("/addfile/<string:folder_hash>", methods=['GET', 'POST'])
def add_file(folder_hash):
  if request.method == 'POST':
    return usecase_create.add_piece_file(folder_hash, request.form, request.files)
  return usecase_create.render_add_file_page(folder_hash)

@app.route("/mdfmetadata/<string:folder_hash>", methods=['GET', 'POST'])
def modify_file_metadata(folder_hash):
  if request.method == 'POST':
    return usecase_modify.update_file_metadata(folder_hash, request.form)
  return usecase_modify.render_update_file_info_page(folder_hash)

@app.route("/rmfile/<string:folder_hash>", methods=['GET', 'POST'])
def delete_file(folder_hash):
  if request.method == 'POST':
    return usecase_modify.delete_file(folder_hash, request.form)
  return usecase_modify.render_file_deletion_page(folder_hash)

@app.route("/replacefile/<string:folder_hash>", methods=['GET', 'POST'])
def replace_file(folder_hash):
  if request.method == 'POST':
    return usecase_modify.replace_file(folder_hash, request.form, request.files)
  return usecase_modify.render_replace_file_page(folder_hash)

@app.route("/add-rm-collection-pieces/<string:collection_code>", methods=['GET', 'POST'])
def add_rm_collection_pieces(collection_code):
  if request.method == 'POST':
    return usecase_modify.modify_collection_pieces(collection_code, request.form)
  return usecase_modify.render_modify_collection_pieces_page(collection_code)

@app.route("/modify-piece/<string:folder_hash>", methods=['GET', 'POST'])
def modify_piece(folder_hash):
  if request.method == 'POST':
    return usecase_modify.update_piece_info(folder_hash, request.form)
  return usecase_modify.render_update_piece_page(folder_hash)

@app.route("/modify-collection/<string:collection_code>", methods=['GET', 'POST'])
def modify_collection(collection_code):
  if request.method == 'POST':
    return usecase_modify.update_collection_info(collection_code, request.form)
  return usecase_modify.render_update_collection_page(collection_code)

@app.route("/modify-composer", methods=['GET', 'POST'])
def modify_composer():
  if request.method == 'POST':
    return usecase_modify.update_or_delete_composer(request.form)
  return usecase_modify.render_update_composer_page()
