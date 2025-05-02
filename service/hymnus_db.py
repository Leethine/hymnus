import os, sqlite3, json
from flask import request
import math
from markupsafe import escape

def createComposerTable():
    QUERY = "SELECT * FROM composers ORDER BY lastname;"
    con = sqlite3.connect("/home/lizian/Projects/hymnus/blob/tables.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    res = cur.execute(QUERY)
    
    composers = []
    for one in res.fetchall():
        if one["code"]:
            one_composer = {}
            one_composer["fullname"] = f'{escape(one["knownas_name"])}'
            one_composer["lastname"] = one_composer["fullname"].split(' ')[-1]
            one_composer["code"] = one["code"]
            one_composer["born"] = str(one["bornyear"])
            one_composer["died"] = str(one["diedyear"])
            composers.append(one_composer)

    table = """<table class="table">
        <thead><tr>
        <th scope="col"></th><th scope="col">Full Name</th>
        <th scope="col">Born</th>
        <th scope="col">Died</th>
        <th scope="col">Code</th>
        </tr></thead>
        <tbody>"""

    for c in composers:
        table += "<tr>"
        table += "<th scope=\"row\">" + c["lastname"] + "</th>"
        table += "<td>" + c["fullname"] + "</td>"
        table += "<td>" + c["born"] + "</td>"
        table += "<td>" + c["died"] + "</td>"
        table += "<td>" + c["code"] + "</td>"
        table += "</tr>"
    table += "</tbody></table>"
    return table
  
def createComposerTableAndPages():
    QUERY = "SELECT * FROM composers ORDER BY lastname;"
    con = sqlite3.connect("/home/lizian/Projects/hymnus/blob/tables.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    res = cur.execute(QUERY)
    
    composers = []
    for one in res.fetchall():
        if one["code"]:
            one_composer = {}
            one_composer["fullname"] = f'{escape(one["knownas_name"])}'
            one_composer["lastname"] = one_composer["fullname"].split(' ')[-1]
            one_composer["code"] = one["code"]
            one_composer["born"] = str(one["bornyear"])
            one_composer["died"] = str(one["diedyear"])
            composers.append(one_composer)

    tables = []
    composer_per_page = 20
    if len(composers) > composer_per_page:
        n_pagination = math.ceil(float(len(composers)) / composer_per_page)
        for i in range(n_pagination):
            table = """<table class="table">
                <thead><tr>
                <th scope="col"></th><th scope="col">Full Name</th>
                <th scope="col">Born</th>
                <th scope="col">Died</th>
                <th scope="col">Code</th>
                </tr></thead>
                <tbody>"""
            for c in composers[i*composer_per_page:(i+1)*composer_per_page]:
                table += "<tr>"
                table += "<th scope=\"row\">" + c["lastname"] + "</th>"
                table += "<td>" + c["fullname"] + "</td>"
                table += "<td>" + c["born"] + "</td>"
                table += "<td>" + c["died"] + "</td>"
                table += "<td>" + c["code"] + "</td>"
                table += "</tr>"
            table += "</tbody></table>"
            tables.append(table)
    return tables
