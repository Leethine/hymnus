import os, json
import metadata, database

ACCEPTED_EXT = ['txt', 'pdf', 'info', 'ly', 'zip', 'xml', 'musicxml']

def getPieceFilePath(folderhash: str):
  if len(folderhash) > 2:
    file_dir = f"{database.HYMNUS_FS}/{folderhash[:2]}/{folderhash}"
    return file_dir
  else:
    return None

def getNamesList(folderhash: str):
  if getPieceFilePath(folderhash):
    filelist = []
    for filename in os.listdir(getPieceFilePath(folderhash)):
      fnamelist = filename.split('.')
      if len(fnamelist) > 1 and fnamelist[-1] in ACCEPTED_EXT:
        name = '.'.join(fnamelist[:-1])
        #ext = fnamelist[-1]
        filelist.append(name)
    return filelist
  else:
    return []

def getFileMetaData(folderhash: str):
  fpath = getPieceFilePath(folderhash)
  if fpath:
    if os.path.isfile(f"{fpath}/desc.json"):
      with open(f"{fpath}/desc.json", 'r') as f:
        j = json.load(f)
        return j
  return None

def checkFileMetaData(folderhash: str):
  metadata = getFileMetaData(folderhash)
  fnamelist = []
  if not metadata:
    return False
  for d in metadata:
    if "fname" in d.keys():
      fnamelist.append(d["fname"])
    else:
      return False
  for fname in getNamesList(folderhash):
    if not fname in fnamelist:
      return False
  return True

def getFileInfo(folderhash: str):
  if metadata.pieceExists(folderhash):
    fileinfo = getFileMetaData(folderhash)
    finfo = []
    if fileinfo:
      if checkFileMetaData(folderhash):
        for j in fileinfo:
          f = {}
          f["popup_title"] = ""
          f["popup_content"] = j["description"]
          f["filename"] = j["headline"]
          f["filelink"] = "/download/" + folderhash + "/" + j["fname"] + j["ext"]
          f["filetype"] = j["ext"]
          finfo.append(f)
      else:
        f = {}
        f["popup_title"] = ""
        f["popup_content"] = ""
        f["filename"] = "File metadata corrupted"
        f["filelink"] = "#"
        f["filetype"] = "!!!"
        finfo = [f]
    else:
      f = {}
      f["popup_title"] = ""
      f["popup_content"] = ""
      f["filename"] = "No files yet"
      f["filelink"] = "#"
      f["filetype"] = "..."
      finfo = [f]
  return finfo