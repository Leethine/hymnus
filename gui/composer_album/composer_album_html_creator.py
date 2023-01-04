#!/usr/bin/python3

HTML_TAG_BEGIN = 0
HTML_TAG_END = 1
MAX_ALBUM_PER_PAGE = 9

ALBUM_TAG_BEGIN = "<!--#TOBESET-->"
ALBUM_TAG_END = "<!--#TOBESET-->"

PAGING_TAG_BEGIN = "<!--#TOBESET-->"
PAGING_TAG_END = "<!--#TOBESET-->"

ICON_DIR = ""

COMPOSER_NAME_LIST = []
COMPOSER_ICON_LIST = []
COMPOSER_YEAR_LIST = []

def reset_album_tag(tag_begin: str, tag_end: str):
  global ALBUM_TAG_BEGIN
  global ALBUM_TAG_END
  ALBUM_TAG_BEGIN = tag_begin
  ALBUM_TAG_END = tag_end

def reset_paging_tag(tag_begin: str, tag_end: str):
  global PAGING_TAG_BEGIN
  global PAGING_TAG_END
  PAGING_TAG_BEGIN = tag_begin
  PAGING_TAG_END = tag_end

def reset_icon_dir(icon_dir: str):
  global ICON_DIR
  ICON_DIR = icon_dir

def create_new_album(composer_name: str, iconfile: str, year: str):
  iconfile = ICON_DIR + "/" + iconfile

  HTML_DIV_TAG_END = "</div>"
  html_str = "<div class=\"col\">\n<div class=\"card shadow-sm\">\n" \
    + "<svg class=\"bd-placeholder-img card-img-top\" width=\"100%\" height=\"225\" xmlns=\"http://www.w3.org/2000/svg\" role=\"img\" aria-label=\"Placeholder: Thumbnail\" preserveAspectRatio=\"xMidYMid slice\" focusable=\"false\"><title>COMPOSERNAMEFIELD</title><image href=\"ICONFILENAMEFIELD\" width=\"100%\" height=\"100%\"/></svg>\n" \
    + "<div class=\"card-body\">\n<p class=\"card-text\">COMPOSERNAMEFIELD</p>\n" \
    + "<div class=\"d-flex justify-content-between align-items-center\">\n<div class=\"btn-group\">\n" \
    + "<button type=\"button\" class=\"btn btn-sm btn-outline-secondary\">View</button>\n" \
    + "<button type=\"button\" class=\"btn btn-sm btn-outline-secondary\">Edit</button>\n" \
    + HTML_DIV_TAG_END + "\n<small class=\"text-muted\">YEARFIELD</small>\n" \
    + HTML_DIV_TAG_END + "\n" + HTML_DIV_TAG_END + "\n" + HTML_DIV_TAG_END + "\n" + HTML_DIV_TAG_END + "\n"

  return html_str.replace("COMPOSERNAMEFIELD",composer_name).replace("ICONFILENAMEFIELD",iconfile).replace("YEARFIELD",year)

def create_page_section(nbr_of_pages: int, next_page: int):
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

def create_album_section(name_list: list, icon_list: list, year_list: list):
  html_album_section_str = ""
  assert(len(name_list) == len(icon_list))
  assert(len(year_list) == len(icon_list))
  assert(len(name_list) == len(year_list))
  assert(len(name_list) <= MAX_ALBUM_PER_PAGE)

  for i in range(0, len(name_list)):
    html_album_section_str += create_new_album(name_list[i], icon_list[i], year_list[i])

  return html_album_section_str

def create_html_file_simple(template_fname: str, new_fname: str, dbg = False):
  assert(len(COMPOSER_NAME_LIST) == len(COMPOSER_ICON_LIST))
  assert(len(COMPOSER_NAME_LIST) == len(COMPOSER_YEAR_LIST))
  assert(len(COMPOSER_YEAR_LIST) == len(COMPOSER_ICON_LIST))
  assert(len(COMPOSER_NAME_LIST) <= 9)

  html_albumsection_str = create_album_section(COMPOSER_NAME_LIST, COMPOSER_ICON_LIST, COMPOSER_YEAR_LIST)
  newhtmlfile_str = ""
  with open(template_fname, "r") as htmlfile:
    isInsideAlbumBlock = False
    isInsidePagingBlock = False
    for line in htmlfile.readlines():
      if isInsideAlbumBlock:
        if ALBUM_TAG_END in line:
          isInsideAlbumBlock = False
          newhtmlfile_str += html_albumsection_str
        else:
          pass
      elif isInsidePagingBlock:
        if PAGING_TAG_END in line:
          isInsidePagingBlock = False
          pass
        else:
          pass
      else:
        if ALBUM_TAG_BEGIN in line:
          isInsideAlbumBlock = True
        elif PAGING_TAG_BEGIN in line:
          isInsidePagingBlock = True
        else:
          newhtmlfile_str += line
  
  if dbg:
    print(newhtmlfile_str)

  with open(new_fname, "w") as htmlfile:
    htmlfile.write(newhtmlfile_str)

def create_html_file(template_fname: str, new_fname: str, dbg = False):
  from math import ceil as m_ceil
  assert(len(COMPOSER_NAME_LIST) == len(COMPOSER_ICON_LIST))
  assert(len(COMPOSER_NAME_LIST) == len(COMPOSER_YEAR_LIST))
  assert(len(COMPOSER_YEAR_LIST) == len(COMPOSER_ICON_LIST))

  html_albumsection_str = ""
  nbr_composers = len(COMPOSER_NAME_LIST)
  if nbr_composers <= MAX_ALBUM_PER_PAGE:
    create_html_file_simple(template_fname, new_fname, dbg)
  else:
    for i in range(0, nbr_composers, MAX_ALBUM_PER_PAGE):
      # get sublist from the complete list
      name_sublist = COMPOSER_NAME_LIST[i:i+MAX_ALBUM_PER_PAGE]
      icon_sublist = COMPOSER_ICON_LIST[i:i+MAX_ALBUM_PER_PAGE]
      year_sublist = COMPOSER_YEAR_LIST[i:i+MAX_ALBUM_PER_PAGE]
      html_albumsection_str = create_album_section(name_sublist, icon_sublist, year_sublist)
      html_pagesection_str = create_page_section(int(m_ceil(nbr_composers/MAX_ALBUM_PER_PAGE)),int(m_ceil(i/MAX_ALBUM_PER_PAGE)+1))
      newhtmlfile_str = ""
      with open(template_fname, "r") as htmlfile:
        isInsideAlbumBlock = False
        isInsidePagingBlock = False
        for line in htmlfile.readlines():
          if isInsideAlbumBlock:
            if ALBUM_TAG_END in line:
              isInsideAlbumBlock = False
              newhtmlfile_str += html_albumsection_str
            else:
              pass
          elif isInsidePagingBlock:
            if PAGING_TAG_END in line:
              isInsidePagingBlock = False
              newhtmlfile_str += html_pagesection_str
            else:
              pass
          else:
            if ALBUM_TAG_BEGIN in line:
              isInsideAlbumBlock = True
            elif PAGING_TAG_BEGIN in line:
              isInsidePagingBlock = True
            else:
              newhtmlfile_str += line
      
      if dbg:
        print("htmlfile_" + str(i+1) + ".html")
      
      next_fname = "index_" + str((m_ceil(i/MAX_ALBUM_PER_PAGE)+1)) + ".html"
      print(next_fname)
      with open(next_fname, "w") as htmlfile:
        htmlfile.write(newhtmlfile_str)

if __name__ == "__main__":
  reset_album_tag("<!--#CAVRFBEGIN-->", "<!--#CAVRFEND-->")
  reset_paging_tag("<!--CAVPNRFBEGIN-->", "<!--CAVPNRFEND-->")
  reset_icon_dir("thumbnail")
  COMPOSER_NAME_LIST = ["J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH","J.S BACH"]
  COMPOSER_ICON_LIST = ["jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg","jsbach.jpg"]
  COMPOSER_YEAR_LIST = ["XXXX","XXXX","XXXX","XXXX","XXXX","XXXX","XXXX","XXXX","XXXX","XXXX","XXXX","XXXX","XXXX","XXXX","XXXX","XXXX","XXXX"]

  create_html_file("index_t.html", "index.html")


