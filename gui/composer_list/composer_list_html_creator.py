#!/usr/bin/python3
import sys, os, shutil, re

sys.path.append('../')
from html_creator import HtmlCreator

class ComposerListHtmlCreator(HtmlCreator):
  def __init__(self) -> None:
    super().__init__()
  
  def create_new_row(self, row: list) -> str:
    html_td_str = "".join([f"<td>{elem}</td>\n" for elem in row])
    return f"<tr>\n{html_td_str}\n</tr>"

  def create_table(self, table_head: list, table_rows: list) -> str:
    """
    Create table according to composer list.
    table_head and table_rows should have the same dimention.
    """
    assert(len(table_head) == len(table_rows[0]))

    html_table_section = ""
    html_elem_table = ("<table class=\"table table-sm\">", "</table>")
    # create table head
    html_str_th = "".join([f"<th scope=\"col\">{col}</th>\n" for col in table_head])
    html_elem_thead = ("<thead>\n" + "<tr>\n" + html_str_th + "</tr>\n", "</thead>")

    html_elem_tbody = ("<tbody>", "</tbody>")
    html_tr_section = "".join([self.create_new_row(row) for row in table_rows]) 

    html_table_section += html_elem_table[0] + "\n"
    html_table_section += html_elem_thead[0] + "\n"
    html_table_section += html_elem_tbody[0] + "\n"
    html_table_section += html_tr_section + "\n"
    html_table_section += html_elem_tbody[1] + "\n"
    html_table_section += html_elem_thead[1] + "\n"
    html_table_section += html_elem_table[1] + "\n"

    return html_table_section

  def create_alphabetical_list_html_file(self, table_head: list, table_rows: list) -> str:
    """
    Create composer alphabetical list according to the table given.
    Examle:
      table_head:
      ["Name", Year"]
      table_rows:
      [["Bach J.S.", "(? - ?)"],["Handel G.F.", "(1600 - ?)"],["Scarlatti D.", "(1600 - ?)"]]
    """
    #TODO add sorting method

    # reset replaceable field tag
    self.reset_tag("<!--#CALRFBEGIN-->", "<!--#CALRFEND-->")
    # reset template file
    self.HTML_TEMPLATE_FILE = self.HTML_TEMPLATE + "_alpha" + self.HTML_EXTENSION
    # set output file name and create the file
    self.HTML_INDEX_FILE = self.HTML_INDEX + "_alpha" + self.HTML_EXTENSION
    
    # read template file, replace section, write to new file
    self.read_template_file()
    self.replace_html_section(self.create_table(table_head, table_rows))
    self.write_index_file()

    # create default index file, since alphabetical list the default entry
    shutil.copyfile(self.HTML_INDEX_FILE, "index.html")

    return self.HTMLFILE_BUFFER

  def create_chronological_list_html_file(self, table_head: list, table_rows: list) -> str:
    """
    Create composer chronological list according to the table given.
    Examle:
      table_head:
      ["Name", Year"]
      table_rows:
      [["Bach J.S.", "(? - ?)"],["Handel G.F.", "(1600 - ?)"],["Scarlatti D.", "(1600 - ?)"]]
    """
    #TODO add sorting method

    # reset replaceable field tag
    self.reset_tag("<!--#CCLRFBEGIN-->", "<!--#CCLRFEND-->")
    # reset template file
    self.HTML_TEMPLATE_FILE = self.HTML_TEMPLATE + "_chrono" + self.HTML_EXTENSION
    # set output file name and create the file
    self.HTML_INDEX_FILE = self.HTML_INDEX + "_chrono" + self.HTML_EXTENSION

    # read template file, replace section, write to new file
    self.read_template_file()
    self.replace_html_section(self.create_table(table_head, table_rows))
    self.write_index_file()

    return self.HTMLFILE_BUFFER

if __name__ == "__main__":
  heads = ["Name", "Year"]
  rows = [["Bach J.S.", "(? - ?)"], ["Handel G.F.", "(1600 - ?)"], ["Scarlatti D.", "(1600 - ?)"]]

  clc = ComposerListHtmlCreator()
  clc.create_alphabetical_list_html_file(heads, rows)
  rows = [["Bach J.S.", "(1600 - ?)"], ["Handel G.F.", "(1600 - ?)"]]

  clc.create_chronological_list_html_file(heads, rows)
