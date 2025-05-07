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
  composer = database.getComposerDataFromCode(composer_code)
  longname = composer["firstname"] + " " + composer["lastname"]
  shortname = composer["knownas_name"]
  year = composer["bornyear"] + " - " + composer["diedyear"]
  c = {}
  c["ShortName"] = shortname
  c["AbbrName"] = getAbbrName(shortname)
  c["LongName"] = longname
  c["Year"] = year
  return c

def getComposerCodeNameList():
  return database.getComposerCodeNameMap()

def composerHasWorks(composer_code: str):
  return database.composerHasWorks(composer_code)

def pieceExists(folder_hash: str):
  return database.pieceExists(folder_hash)

def getPieceMetadata(folder_hash: str):
  row = database.getPieceDataFromHash(folder_hash)
  if row:
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
                "hash","comment"]:
      row[key] = ""
    return row