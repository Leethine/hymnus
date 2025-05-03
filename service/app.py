import os, sqlite3, json
from flask import Flask, render_template, redirect, request
from markupsafe import escape
import hymnus_page, hymnus_db

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", page_title="Hymnus Library", root_url="")

@app.route("/all-pieces")
def page_allpieces():
    return render_template("item_list.html", page_title="All Pieces • Hymnus Library", list_items_page_property=hymnus_page.getPageSetting("p"), root_url="")

@app.route("/composers-all")
def all_composers():
    return render_template("item_list.html", page_title="Composers • Hymnus Library", \
        list_items_page_property=hymnus_page.getPageSetting("c"), \
        list_items_table=hymnus_db.createComposerTable())

@app.route("/composers")
def composers():
    tables = hymnus_db.createComposerTableAndPages()
    n_pagination = len(tables)
    pagination = ["<a class=\"w3-button w3-black\" href=\"#\">1</a>"]

    for i in range(1, n_pagination):
        pagination.append("<a class=\"w3-button w3-hover-black\" href=\"composers/" \
                          + str(i+1) + "\">" + str(i+1) + "</a>")
    if n_pagination > 1:
        return render_template("item_list.html", \
            root_url="", \
            page_title="Composers • Hymnus Library", \
            list_items_page_property=hymnus_page.getPageSetting("c"), \
            list_items_table=tables[0], \
            list_items_pagination=" ".join(pagination))
    else:
        return render_template("item_list.html", \
            root_url="", \
            page_title="Composers • Hymnus Library", \
            list_items_page_property=hymnus_page.getPageSetting("c"), \
            list_items_table=hymnus_db.createComposerTable(), \
            list_items_pagination="")
    
@app.route("/composers/<pagenumber>")
def page_composers(pagenumber):
    if not pagenumber.isdigit():
        return "Invalid page number: " + pagenumber
    i_pagenumber = int(pagenumber) - 1
    tables = hymnus_db.createComposerTableAndPages()
    n_pagination = len(tables)
    pagination = []
    for i in range(n_pagination):
        pagination.append("<a class=\"w3-button w3-hover-black\" href=\"" \
                          + str(i+1) + "\">" + str(i+1) + "</a>")
    if i_pagenumber >= 0 and i_pagenumber < n_pagination:
        pagination[i_pagenumber] = "<a class=\"w3-button w3-black\" href=\"#\">" \
                                 + str(pagenumber) + "</a>"
        return render_template("item_list.html", \
            root_url="", \
            page_title="Composers • Hymnus Library", \
            list_items_page_property=hymnus_page.getPageSetting("c"), \
            list_items_table=tables[i_pagenumber], \
            list_items_pagination=" ".join(pagination))
    else:
        return "Page out of range"

@app.route("/collections")
def page_collections():
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