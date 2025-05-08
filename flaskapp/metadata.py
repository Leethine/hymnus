import database

def getAbbrName(name: str):
  namelist = name.replace('-', ' ').split(' ')
  if len(namelist) > 1:
    first = ' '.join([x[0] for x in namelist[:-1]])
    last = namelist[-1]
    return f"{first} {last}"
  else:
    return name

def getComposerMetadata(composer_code: str):
  c = {}
  if composer_code == "zzz_unknown":
    c["code"] = "zzz_unknown"
    c["ShortName"] = "Unknown"
    c["AbbrName"] = "Unknown"
    c["LongName"] = "Unknown"
    c["Year"] = ""
  else:
    composer = database.getComposerRowFromCode(composer_code)
    longname = composer["firstname"] + " " + composer["lastname"]
    shortname = composer["knownas_name"]
    year = composer["bornyear"] + " - " + composer["diedyear"]
    c["code"] = composer_code
    c["ShortName"] = shortname
    c["AbbrName"] = getAbbrName(shortname)
    c["LongName"] = longname
    c["Year"] = year
  return c

def getComposerCodeNameList():
  composerlist = database.getComposerCodeNameMap()
  for c in composerlist:
    names = c["name"]
    c["name"] = names.split(" ")[-1] + ", " + ' '.join(names.split(" ")[:-1])
  return composerlist

def composerHasWorks(composer_code: str):
  return database.composerHasWorks(composer_code)

def pieceExists(folder_hash: str):
  return database.pieceExists(folder_hash)

def getPieceMetadata(folder_hash: str):
  row = database.getPieceRowFromHash(folder_hash)
  if row:
    # remove 'None' data
    for k in row.keys():
      if not row[k]:
        row[k] = "N/A"
    row["composer"] = getComposerMetadata(row["composer_code"])["ShortName"]
    if row["arranged"] == "1":
      arranger = getComposerMetadata(row["arranger_code"])
      row["arranged_by"] = arranger["AbbrName"]
    else:
      row["arranged_by"] = "N/A"
    return row
  else:
    row = {}
    for key in ["composer","composer_code","arranged","arranged_by",
                "arranger_code","collection_code","title","subtitle",
                "subsubtitle","dedicated_to","opus","instruments",
                "_folder_hash","comment"]:
      row[key] = ""
    return row

def getCollectionMetadata(collection_code: str):
  row = database.getCollectionRowFromCode(collection_code)
  if row:
    # remove 'None' data and white spaces
    for k in row.keys():
      if not row[k]:
        row[k] = "N/A"
    if row["composer_code"] == "" or row["composer_code"] == "zzz_unknown":
      row["composer"] = "Various"
    else:
      row["composer"] = getComposerMetadata(row["composer_code"])["ShortName"]
    return row
  else:
    row = {}
    for k in ["code", "composer_code", "composer", "title",
              "subtitle", "subsubtitle", "opus", "description_text",
              "volume", "instruments", "editor"]:
      row[k] = ""
    return row
    
