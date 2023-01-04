#!/usr/bin/python3
import sys, os, shutil, re
from math import ceil as m_ceil
sys.path.append('../')
from html_creator import HtmlCreator

class ComposerAlbumHtmlCreator(HtmlCreator):
  def __init__(self) -> None:
    super().__init__()
    self.ICON_DIR = "thumbnail"
    self.MAX_ALBUM_PER_PAGE = 9

  def reset_tag(self, tag_begin: str, tag_end: str) -> None:
    super().reset_tag(tag_begin, tag_end)
  
  def create_new_album(self, name: str, iconfile: str, year: str) -> str:
    iconfile = self.ICON_DIR + "/" + iconfile

    HTML_DIV_TAG_END = "</div>"
    html_str = "<div class=\"col\">\n<div class=\"card shadow-sm\">\n" \
      + "<svg class=\"bd-placeholder-img card-img-top\" width=\"100%\" height=\"225\" xmlns=\"http://www.w3.org/2000/svg\" role=\"img\" aria-label=\"Placeholder: Thumbnail\" preserveAspectRatio=\"xMidYMid slice\" focusable=\"false\"><title>COMPOSERNAMEFIELD</title><image href=\"ICONFILENAMEFIELD\" width=\"100%\" height=\"100%\"/></svg>\n" \
      + "<div class=\"card-body\">\n<p class=\"card-text\">COMPOSERNAMEFIELD</p>\n" \
      + "<div class=\"d-flex justify-content-between align-items-center\">\n<div class=\"btn-group\">\n" \
      + "<button type=\"button\" class=\"btn btn-sm btn-outline-secondary\">View</button>\n" \
      + "<button type=\"button\" class=\"btn btn-sm btn-outline-secondary\">Edit</button>\n" \
      + HTML_DIV_TAG_END + "\n<small class=\"text-muted\">YEARFIELD</small>\n" \
      + HTML_DIV_TAG_END + "\n" + HTML_DIV_TAG_END + "\n" + HTML_DIV_TAG_END + "\n" + HTML_DIV_TAG_END + "\n"

    return html_str.replace("COMPOSERNAMEFIELD",name).replace("ICONFILENAMEFIELD",iconfile).replace("YEARFIELD",year)

  def create_page_section(self, nbr_of_pages: int, next_page: int) -> str:
    assert(nbr_of_pages >= 2)
    assert(next_page <= nbr_of_pages)
    html_str = "<footer class=\"text-muted py-5\">\n<div class=\"container\">\n" \
      + "<p class=\"float-end mb-1\"><a href=\"" + "index_" + str(next_page) + ".html\">&thinsp; next</a></p>\n" \
      + "<p class=\"float-end mb-1\">&emsp;</p>\n" \
      + "<p class=\"float-end mb-1\"><a href=\"" + "index_" + str(nbr_of_pages) + ".html\">&thinsp; end</a></p>\n" \
      + "<p class=\"float-end mb-1\">&emsp;</p>\n" \
      + "<p class=\"float-end mb-1\">...</a></p>\n"
    
    for pagenumber in range(1,nbr_of_pages+1):
      new_p_str = "<p class=\"float-end mb-1\">&emsp;</p>\n<p class=\"float-end mb-1\"><a href=\"" + "index_" + str(pagenumber) + ".html\">&thinsp; " + str(pagenumber) + "</a></p>\n"
      html_str += new_p_str

    return html_str + "</div>\n</footer>\n"

  def create_album_section(self, name_list: list, icon_list: list, year_list: list):
    html_album_section_str = ""
    assert(len(name_list) == len(icon_list))
    assert(len(year_list) == len(icon_list))
    assert(len(name_list) == len(year_list))
    assert(len(name_list) <= self.MAX_ALBUM_PER_PAGE)

    for i in range(0, len(name_list)):
      html_album_section_str += self.create_new_album(name_list[i], icon_list[i], year_list[i])

    return html_album_section_str

  def create_small_album_html_file(self, name_list: list, icon_list: list, year_list: list) -> str:
    """
    Create album index.html, for less than 9 composers.
    Without paging number.
    """
    assert(len(name_list) == len(icon_list))
    assert(len(name_list) == len(year_list))
    assert(len(year_list) == len(icon_list))
    assert(len(name_list) <= self.MAX_ALBUM_PER_PAGE)

    #TODO add sort method
    
    # reset tag for album section
    self.reset_tag("<!--#CAVRFBEGIN-->", "<!--#CAVRFEND-->")
    
    # read template file, replace album section
    self.read_template_file()
    self.replace_html_section(self.create_album_section(name_list, icon_list, year_list))

    # reset tag for page section
    self.reset_tag("<!--CAVPNRFBEGIN-->", "<!--CAVPNRFEND-->")

    # replace page section, write to new file
    self.replace_html_section('')
    self.write_index_file()

    return self.HTMLFILE_BUFFER
  
  def create_big_album_html_file(self, name_list: list, icon_list: list, year_list: list) -> str:
    """
    Create album index.html, for more than 9 composers.
    With paging number.
    """
    assert(len(name_list) == len(icon_list))
    assert(len(name_list) == len(year_list))
    assert(len(year_list) == len(icon_list))
    assert(len(name_list) > self.MAX_ALBUM_PER_PAGE)

    #TODO add sort method

    nbr_composers = len(name_list)

    for i in range(0, nbr_composers, self.MAX_ALBUM_PER_PAGE):
      # get sublist from the complete list
      name_sublist = name_list[i:i+self.MAX_ALBUM_PER_PAGE]
      icon_sublist = icon_list[i:i+self.MAX_ALBUM_PER_PAGE]
      year_sublist = year_list[i:i+self.MAX_ALBUM_PER_PAGE]

      # calculate new file number
      newfile_nbr = m_ceil(i / self.MAX_ALBUM_PER_PAGE) + 1
      # calculate end file number (aka number of pages)
      endfile_nbr = m_ceil(nbr_composers / self.MAX_ALBUM_PER_PAGE)

      # reset tag for album section
      self.reset_tag("<!--#CAVRFBEGIN-->", "<!--#CAVRFEND-->")
      
      # read template file, replace album section
      self.read_template_file()
      self.replace_html_section(self.create_album_section(name_sublist, icon_sublist, year_sublist))

      # reset tag for page section
      self.reset_tag("<!--CAVPNRFBEGIN-->", "<!--CAVPNRFEND-->")

      # replace page section, write to new file
      self.replace_html_section(self.create_page_section(endfile_nbr, newfile_nbr))
      
      # reset new file name, write new file
      self.HTML_INDEX_FILE = self.HTML_INDEX \
                           + "_" + str(newfile_nbr) \
                           + self.HTML_EXTENSION
      self.write_index_file()
    
    # reset entry file name to index.html
    self.HTML_INDEX_FILE = self.HTML_INDEX + self.HTML_EXTENSION

    # set default entry file index.html
    if os.path.exists("index_1.html"):
      shutil.copyfile("index_1.html", self.HTML_INDEX_FILE)
    
    return self.HTMLFILE_BUFFER

  def create_album_html_file(self, name_list: list, icon_list: list, year_list: list) -> str:
    """
    Create album html pages from the list given.
    """
    assert(len(name_list) == len(icon_list))
    assert(len(name_list) == len(year_list))
    assert(len(year_list) == len(icon_list))
    if len(name_list) > self.MAX_ALBUM_PER_PAGE:
      return self.create_big_album_html_file(name_list, icon_list, year_list)
    else:
      return self.create_small_album_html_file(name_list, icon_list, year_list)

if __name__ == "__main__":
  cac = ComposerAlbumHtmlCreator()
  """
  names = ["J.S BACH","J.S BACH","J.S BACH"]
  icons = ["jsbach.jpg","jsbach.jpg","jsbach.jpg"]
  years = ["XXXX","XXXX","XXXX"]

  cac.create_album_html_file(names, icons, years)

  """
  names = ["J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH"]
  icons = ["jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg"]
  years = ["XXXX","XXXX","XXXX","XXXX","XXXX","XXXX","XXXX","XXXX","XXXX","XXXX","XXXX","XXXX","XXXX","XXXX","XXXX","XXXX","XXXX"]

  cac.create_album_html_file(names, icons, years)
  
