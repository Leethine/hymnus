#!/usr/bin/python3
import sys, os, shutil, re

sys.path.append('../')
from html_creator import HtmlCreator

class ComposerListHtmlCreator(HtmlCreator):
  def __init__(self) -> None:
    super().__init__()
    self.PAGE_DIR = "../composer_page/info"
  
  def create_new_row(self, row: list, page_link="") -> str:
    assert(len(row) != 0)
    if ".html" in page_link:
      page_link = self.PAGE_DIR + "/" + page_link
    else:
      page_link = "#"
    
    html_td_str = f"<td><a href=\"{page_link}\" class=\"composer-name-link\">{row[0]}</a></td>\n"
    html_td_str += "".join([f"<td>{elem}</td>\n" for elem in row[1:]])

    return f"<tr>\n{html_td_str}\n</tr>"

  def create_table(self, table_head: list, table_rows: list, page_links=[]) -> str:
    """
    Create table according to composer list.
    table_head and table_rows should have the same dimention.
    """
    assert(len(table_head) == len(table_rows[0]))
    assert(len(page_links) == 0 or len(page_links) == len(table_rows))

    html_table_section = ""
    html_elem_table = ("<table class=\"table table-sm\">", "</table>")
    # create table head
    html_str_th = "".join([f"<th scope=\"col\">{col}</th>\n" for col in table_head])
    html_elem_thead = ("<thead>\n" + "<tr>\n" + html_str_th + "</tr>\n", "</thead>")

    html_elem_tbody = ("<tbody>", "</tbody>")
    html_tr_section = ""
    if not page_links:
      html_tr_section = "".join([self.create_new_row(row) for row in table_rows])
    else:
      for i in range(len(page_links)):
        html_tr_section += self.create_new_row(table_rows[i], page_links[i])

    html_table_section += html_elem_table[0] + "\n"
    html_table_section += html_elem_thead[0] + "\n"
    html_table_section += html_elem_tbody[0] + "\n"
    html_table_section += html_tr_section + "\n"
    html_table_section += html_elem_tbody[1] + "\n"
    html_table_section += html_elem_thead[1] + "\n"
    html_table_section += html_elem_table[1] + "\n"

    return html_table_section

  def create_alphabetical_list_html_file(self, table_head: list, table_rows: list, page_links=[]) -> str:
    """
    Create composer alphabetical list according to the table given.
    Examle:
      table_head:
      ["Name", Year"]
      table_rows:
      [["Bach J.S.", "(? - ?)"],["Handel G.F.", "(1600 - ?)"],["Scarlatti D.", "(1600 - ?)"]]
    """

    # reset replaceable field tag
    self.reset_tag("<!--#CALRFBEGIN-->", "<!--#CALRFEND-->")
    # reset template file
    self.HTML_TEMPLATE_FILE = self.HTML_TEMPLATE + "_alpha" + self.HTML_EXTENSION
    # set output file name and create the file
    self.HTML_INDEX_FILE = self.HTML_INDEX + "_alpha" + self.HTML_EXTENSION
    
    # read template file, replace section, write to new file
    self.read_template_file()
    self.replace_html_section(self.create_table(table_head, table_rows, page_links))
    self.write_index_file()

    # create default index file, since alphabetical list the default entry
    shutil.copyfile(self.HTML_INDEX_FILE, "index.html")

    return self.HTMLFILE_BUFFER

  def create_chronological_list_html_file(self, table_head: list, table_rows: list, page_links=[]) -> str:
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
    self.replace_html_section(self.create_table(table_head, table_rows, page_links))
    self.write_index_file()

    return self.HTMLFILE_BUFFER

if __name__ == "__main__":

  heads = ["Name", "Year"]
  rows = [["Bach J.S.", "(? - ?)"], ["Handel G.F.", "(1600 - ?)"], ["Scarlatti D.", "(1600 - ?)"]]
  links = ["", "handel_g_f.html", ""]

  clc = ComposerListHtmlCreator()
  clc.create_alphabetical_list_html_file(heads, rows, links)
  rows = [["Bach J.S.", "(1600 - ?)"], ["Handel G.F.", "(1600 - ?)"]]
  links = ["bach_j_s.html", "#"]

  clc.create_chronological_list_html_file(heads, rows, links)
