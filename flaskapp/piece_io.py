import os, json, pickle, time
import metadata, database

FILE_METADATA_FORMAT = "json" # bin or json
ACCEPTED_EXT = ['txt', 'pdf', 'ly', 'zip', 'xml', 'musicxml']

def getPieceFilePath(folderhash: str):
  if len(folderhash) > 2:
    file_dir = f"{database.HYMNUS_FS}/{folderhash[:2]}/{folderhash}"
    return file_dir
  else:
    return None

def getFileNamesList(folderhash: str):
  if getPieceFilePath(folderhash):
    filelist = []
    for filename in os.listdir(getPieceFilePath(folderhash)):
      fnamelist = filename.split('.')
      if len(fnamelist) > 1 and fnamelist[-1] in ACCEPTED_EXT:
        name = '.'.join(fnamelist[:-1])
        filelist.append(name)
    return filelist
  else:
    return []

def getFileMetaData(folderhash: str):
  fpath = getPieceFilePath(folderhash)
  if fpath:
    if FILE_METADATA_FORMAT == "json":
      if os.path.isfile(f"{fpath}/desc.json"):
        with open(f"{fpath}/desc.json", 'r') as f:
          d = json.load(f)
          return d
  return None

def writeFileMetaData(folderhash: str, data: list):
  fpath = getPieceFilePath(folderhash)
  if fpath:
    if FILE_METADATA_FORMAT == "json":
      if os.path.isfile(f"{fpath}/desc.json"):
        with open(f"{fpath}/desc.json", 'w') as f:
          json.dump(data, f)


def checkFileMetaData(folderhash: str):
  data = getFileMetaData(folderhash)
  print(data)
  fnamelist = []
  if not data:
    return False
  for d in data:
    if "fname" in d.keys():
      fnamelist.append(d["fname"])
    else:
      return False
  for fname in getFileNamesList(folderhash):
    if not fname in fnamelist:
      return False
  return True

def getFilePageInfo(folderhash: str):
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

def getSimpleSubmitPage():
  return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="text" name="title" />
      <textarea type="text" name="description" rows="3">No description</textarea>
      <input type="submit" value="Upload">
    </form>
  '''

def getSimpleDeletePage(folderhash: str):
  data = getFileMetaData(folderhash)
  HTMLFORM = '''
    <!doctype html>
    <title>Delete File</title>
    <h1>Delete File</h1>
    <form method="post" enctype="multipart/form-data">
      <select name="select-file" id="select-file">
  '''
  for item in data:
    if item and 'headline' in item.keys():
        HTMLFORM += "<option>" + item['headline'] + "</option>"  
  HTMLFORM += '</select><input type="submit" value="Delete"></form>'
  return HTMLFORM
    

def checkInputForm(filename: str, filetitle: str, description: str):  
  if filename and filetitle and description:
    return True
  else:
    return False
  
def checkFileExtension(filname: str):
  ext = filname.split('.')[-1]
  if ext in ACCEPTED_EXT:
    return True
  return False

def addFileMetaData(folderhash: str, filename: str, title: str, desc: str):
  extention = filename.split('.')[-1]
  #newname = metadata.getPieceMetadata(folderhash)["title"].lower().replace(' ', '_') \
  #        + "_" + "{:.4f}".format(time.time() - int(time.time())).replace("0.","") \
  #        + "." + extention
  newname =  "File_" \
          + "{:.4f}".format(time.time() - int(time.time())).replace("0.","") \
          + "_" + filename.replace(' ', '_')

  os.rename(f"{getPieceFilePath(folderhash)}/{filename}",
            f"{getPieceFilePath(folderhash)}/{newname}")

  data = getFileMetaData(folderhash)
  newfile = {}
  newfile["headline"] = str(title)
  newfile["description"] = str(desc)
  newfile["ext"] = "." + extention
  newfile["fname"] = newname.replace(newfile["ext"], '')
  data.append(newfile)
  writeFileMetaData(folderhash, data)

def deleteFileAndMetaData(folderhash: str, title):
  data = getFileMetaData(folderhash)
  newdata = []
  data_deleted = {}
  for item in data:
    if item and 'headline' in item.keys():
      if item['headline'] == title:
        data_deleted = item
      else:
        newdata.append(item)

  filename = data_deleted['fname'] + data_deleted['ext']
  os.remove(f"{getPieceFilePath(folderhash)}/{filename}")
  writeFileMetaData(folderhash, newdata)

