#!/usr/bin/python3

HTML_TAG_BEGIN = 0
HTML_TAG_END = 1

REPLACE_TAG_BEGIN = "<!--#TOBESET-->"
REPLACE_TAG_END = "<!--#TOBESET-->"

TABLE_HEAD = []
TABLE_ROWS = [[]]

def reset_tag(tag_begin: str, tag_end: str):
  global REPLACE_TAG_BEGIN
  global REPLACE_TAG_END
  REPLACE_TAG_BEGIN = tag_begin
  REPLACE_TAG_END = tag_end

def create_new_row(row: list):
  html_td_str = "".join([f"<td>{elem}</td>\n" for elem in row])
  return f"<tr>\n{html_td_str}\n</tr>"

def create_table(table_head: list, table_rows: list):
  """
  Create table according to composer list.
  table_head and table_rows should have the same dimention.
  """
  assert(len(table_head) == len(table_rows))

  html_table = ""
  html_elem_table = ("<table class=\"table table-sm\">", "</table>")
  # create table head
  html_str_th = "".join([f"<th scope=\"col\">{col}</th>\n" for col in table_head])
  html_elem_thead = ("<thead>\n" + "<tr>\n" + html_str_th + "</tr>\n", "</thead>")

  html_elem_tbody = ("<tbody>", "</tbody>")
  html_str_tr = "".join([create_new_row(row) for row in table_rows]) 

  html_table += html_elem_table[HTML_TAG_BEGIN] + "\n"
  html_table += html_elem_thead[HTML_TAG_BEGIN] + "\n"
  html_table += html_elem_tbody[HTML_TAG_BEGIN] + "\n"
  html_table += html_str_tr + "\n"
  html_table += html_elem_tbody[HTML_TAG_END] + "\n"
  html_table += html_elem_thead[HTML_TAG_END] + "\n"
  html_table += html_elem_table[HTML_TAG_END] + "\n"

  return html_table

def create_html_file(template_fname: str, new_fname: str, dbg = False):
  """
  Iterate lines in html template file until replacement tag is found,
  create and fill the table between replacement tags,
  create new html file with the new table.
  """
  newhtmlfile_str = ""
  isInsideBlock = False
  with open(template_fname, "r") as htmlfile:
    for line in htmlfile.readlines():
      if isInsideBlock:
        if REPLACE_TAG_END in line:
          isInsideBlock = False
          newhtmlfile_str += create_table(TABLE_HEAD, TABLE_ROWS)
        else:
          pass
      else:
        if REPLACE_TAG_BEGIN in line:
          isInsideBlock = True
        else:
          newhtmlfile_str += line
  
  with open(new_fname, "w") as htmlfile:
    htmlfile.write(newhtmlfile_str)
  
  if dbg:
    print(newhtmlfile_str)

if __name__ == "__main__":
  TABLE_HEAD = ["Name", "Year"]
  TABLE_ROWS = [["Bach J.S.", "(? - ?)"], ["Handel G.F.", "(1600 - ?)"],  ["Scarlatti D.", "(1600 - ?)"]]

  reset_tag("<!--#CALRFBEGIN-->", "<!--#CALRFEND-->")
  create_html_file("index_t.html", "index.html")
