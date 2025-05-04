import os, sqlite3, json
from flask import Flask, render_template
from flask import redirect, request
from markupsafe import escape
import hymnus_page, hymnus_db

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", page_title="Hymnus Library")

@app.route("/about")
def about():
    return "About Blank"

@app.route("/contact")
def contact():
    return "Contact"

@app.route("/all-pieces")
def pieces():
    html = hymnus_db.createPieceTableAndPagination(composer_code="franck_c", pagenumber=1)
    return render_template("item_list.html", \
        page_title="Pieces • Hymnus Library", \
        list_items_page_property=hymnus_page.getPageSetting("p"), \
        list_items_table=html["Table"], \
        list_items_pagination=html["Pagination"])

@app.route("/all-pieces/<pagenumber>")
def page_pieces(pagenumber):
    if not str(pagenumber).isdigit():
        return "Invalid page number: " + str(pagenumber)
    html = hymnus_db.createPieceTableAndPagination(pagenumber=int(pagenumber))

    # Avoid having href="#" for composer page 
    page_setting = hymnus_page.getPageSetting("p")
    page_setting["url_allpieces"] = "all-pieces"

    return render_template("item_list.html", \
        page_title="Pieces • Hymnus Library", \
        list_items_page_property=page_setting, \
        list_items_table=html["Table"], \
        list_items_pagination=html["Pagination"])

# Without paging
@app.route("/composers-all")
def all_composers():
    return render_template("item_list.html", page_title="Composers • Hymnus Library", \
        list_items_page_property=hymnus_page.getPageSetting("c"), \
        list_items_table=hymnus_db.createHtmlTable())

@app.route("/composers/<pagenumber>")
def page_composers(pagenumber):
    if not str(pagenumber).isdigit():
        return "Invalid page number: " + str(pagenumber)
    html = hymnus_db.createComposerTableAndPagination(pagenumber=int(pagenumber))
    
    # Avoid having href="#" for composer page 
    page_setting = hymnus_page.getPageSetting("c")
    page_setting["url_composers"] = "composers"

    return render_template("item_list.html", \
        page_title="Composers • Hymnus Library", \
        list_items_page_property=page_setting, \
        list_items_table=html["Table"], \
        list_items_pagination=html["Pagination"])

@app.route("/composers")
def composers():
    html = hymnus_db.createComposerTableAndPagination(1)
    return render_template("item_list.html", \
        page_title="Composers • Hymnus Library", \
        list_items_page_property=hymnus_page.getPageSetting("c"), \
        list_items_table=html["Table"], \
        list_items_pagination=html["Pagination"])


@app.route("/collections/<pagenumber>")
def page_collections(pagenumber):
    if not str(pagenumber).isdigit():
        return "Invalid page number: " + str(pagenumber)
    html = hymnus_db.createCollectionTableAndPagination(pagenumber=int(pagenumber))

    # Avoid having href="#" for composer page 
    page_setting = hymnus_page.getPageSetting("col")
    page_setting["url_collections"] = "collections"

    return render_template("item_list.html", \
        page_title="Collections • Hymnus Library", \
        list_items_page_property=page_setting, \
        list_items_table=html["Table"], \
        list_items_pagination=html["Pagination"])

@app.route("/collections")
def collections():
    return render_template("item_list.html", page_title="Collections • Hymnus Library", list_items_page_property=hymnus_page.getPageSetting("col"))

@app.route("/search")
def page_search():
    return render_template("item_list.html", page_title="Search • Hymnus Library", list_items_page_property=hymnus_page.getPageSetting("s"))


# Page test
@app.route('/works/<composercode>')
def show_user_profile(composercode):
    con = sqlite3.connect("/home/lizian/Projects/hymnus/blob/tables.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    res = cur.execute("SELECT * FROM pieces;")
    page = f"Composer: "
    for one in res.fetchall():
        if one["composer_code"] == composercode:
            page += f'{escape(one["folder_hash"])}'
    
    return page

if __name__ == '__main__':
   app.run()