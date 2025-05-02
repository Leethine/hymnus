PAGESETTING_DEFAULT = {
    "headline": "",
    "description": "",
    "toggle_menu_search"      : "", "url_search"     : "search",
    "toggle_menu_allpieces"   : "", "url_allpieces"  : "all-pieces",
    "toggle_menu_collections" : "", "url_collections": "collections",
    "toggle_menu_composers"   : "", "url_composers"  : "composers"
}

def getPageSetting(pagetype: str):
    pagesetting = PAGESETTING_DEFAULT.copy()
    if pagetype == "p":
        pagesetting["headline"] = "All Pieces"
        pagesetting["description"] = "Browse all pieces in this library."
        pagesetting["toggle_menu_allpieces"] = " w3-theme-l3 "
        pagesetting["url_allpieces"] = "#"
    elif pagetype == "c":
        pagesetting["headline"] = "Composers"
        pagesetting["description"] = "Browse the works of composers"
        pagesetting["toggle_menu_composers"] = " w3-theme-l3 "
        pagesetting["url_composers"] = "#"
    elif pagetype == "col":
        pagesetting["headline"] = "Collections"
        pagesetting["description"] = "Browse the list of collections"
        pagesetting["toggle_menu_collections"] = " w3-theme-l3 "
        pagesetting["url_collections"] = "#"
    elif pagetype == "s":
        pagesetting["headline"] = "Search"
        pagesetting["description"] = "Type to search..."
        pagesetting["toggle_menu_search"] = " w3-theme-l3 "
        pagesetting["url_search"] = "#"
    else:
        pass
    return pagesetting
