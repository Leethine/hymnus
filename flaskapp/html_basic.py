LIST_ITEM_PAGE_CONTENT = {
  "headline": "",
  "description": "",
  "toggle_menu_search"      : "", "url_search"     : "search",
  "toggle_menu_allpieces"   : "", "url_allpieces"  : "browse/all-pieces",
  "toggle_menu_collections" : "", "url_collections": "browse/collections",
  "toggle_menu_composers"   : "", "url_composers"  : "browse/composers"
}

def getPageContent(page_type: str):
  content = LIST_ITEM_PAGE_CONTENT.copy()
  if page_type == "p" or page_type == "pieces" or \
     page_type == "w" or page_type == "works":
    content["headline"] = "Pieces"
    content["description"] = "Browse all work pieces in this library."
    content["toggle_menu_allpieces"] = " w3-theme-l3 "
    content["url_allpieces"] = "#"
  elif page_type == "c" or page_type == "composers":
    content["headline"] = "Composers"
    content["description"] = "Browse the works of composers"
    content["toggle_menu_composers"] = " w3-theme-l3 "
    content["url_composers"] = "#"
  elif page_type == "col" or page_type == "collections":
    content["headline"] = "Collections"
    content["description"] = "Browse the list of collections"
    content["toggle_menu_collections"] = " w3-theme-l3 "
    content["url_collections"] = "#"
  elif page_type == "s" or page_type == "search":
    # TODO
    content["headline"] = "Search (WIP)"
    content["description"] = "Type to search..."
    content["toggle_menu_search"] = " w3-theme-l3 "
    content["url_search"] = "#"
  else:
    pass
  return content
