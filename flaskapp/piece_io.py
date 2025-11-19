import os, json, time, sys
from metadata import Metadata
from database import Database

class PieceIO():
  def __init__(self):
    self.FILE_METADATA_FORMAT = "json" # bin or json
    self.ACCEPTED_EXT = ['txt','pdf','ly','zip','xml','musicxml',
                         'xz','gz','tar','eps','png']
    self._piecefile_dir = ""
    self._piece_page_filelist = []
    

  def getPieceFileDir(self, folderhash: str) -> str:
    if len(folderhash) > 2:
      _piecefile_dir = f"{Database().getFSPath()}/{folderhash[:2]}/{folderhash}"
      return _piecefile_dir
    else:
      return ""
  

  def getSavedFilePath(self, folderhash: str, filename: str) -> str:
    return os.path.join(self.getPieceFileDir(folderhash), filename)


  def getFileNamesList(self, folderhash: str) -> list:
    filelist = []
    if self.getPieceFileDir(folderhash):
      for filename in os.listdir(self.getPieceFileDir(folderhash)):
        fnamelist = filename.split('.')
        if len(fnamelist) > 1 and fnamelist[-1] in self.ACCEPTED_EXT:
          name = '.'.join(fnamelist[:-1])
          filelist.append(name)
    return filelist


  def getFileMetaData(self, folderhash: str) -> list:
    fpath = self.getPieceFileDir(folderhash)
    data = []
    if fpath != "":
      if self.FILE_METADATA_FORMAT == "json":
        if os.path.isfile(f"{fpath}/desc.json"):
          with open(f"{fpath}/desc.json", 'r') as f:
            data = json.load(f)
    return data


  def writeFileMetaData(self, folderhash: str, data: list) -> None:
    fpath = self.getPieceFileDir(folderhash)
    if fpath != "":
      if self.FILE_METADATA_FORMAT == "json":
        if os.path.isdir(fpath):
          with open(f"{fpath}/desc.json", 'w') as f:
            json.dump(data, f)
    return None


  def checkFileMetaData(self, folderhash: str) -> bool:
    data = self.getFileMetaData(folderhash)
    fnamelist = []
    if not data:
      print("[Error] File metadata is empty!", file=sys.stderr)
      return False
    for d in data:
      if "fname" in d.keys():
        fnamelist.append(d["fname"])
      else:
        print("[Error] Missing key 'fname' in json file!", file=sys.stderr)
        return False
    # Check if files in directory are all listed in desc.json
    for fname in self.getFileNamesList(folderhash):
      if not fname in fnamelist:
        print(f"[Error] '{fname}' not in desc.json", file=sys.stderr)
        return False
    return True


  def getPiecePageFileList(self, folderhash: str) -> list:
    meta = Metadata()
    if meta.pieceExists(folderhash):
      fileinfo = self.getFileMetaData(folderhash)
      _piece_page_filelist = []
      if fileinfo:
        if self.checkFileMetaData(folderhash):
          for j in fileinfo:
            f = {}
            f["popup_title"] = ""
            f["popup_content"] = j["description"]
            f["filename"] = j["headline"]
            f["filelink"] = "/download/" + folderhash + "/" + j["fname"] + j["ext"]
            f["filetype"] = j["ext"]            
            _piece_page_filelist.append(f)
        else:
          f = {}
          f["popup_title"] = ""
          f["popup_content"] = ""
          f["filename"] = "File metadata corrupted"
          f["filelink"] = "#"
          f["filetype"] = "!!!"
          _piece_page_filelist = [f]
      else:
        f = {}
        f["popup_title"] = ""
        f["popup_content"] = ""
        f["filename"] = "No files yet"
        f["filelink"] = "#"
        f["filetype"] = "..."
        _piece_page_filelist = [f]
    return _piece_page_filelist

  
  def checkFileExtension(self, filname: str) -> bool:
    ext = filname.split('.')[-1]
    if ext in self.ACCEPTED_EXT:
      return True
    return False


  def addFileMetaData(self, folderhash: str, filename: str, title: str, desc: str) -> None:
    extention = filename.split('.')[-1]
    newname =  "File_" \
            + "{:.4f}".format(time.time() - int(time.time())).replace("0.","") \
            + "_" + filename.replace(' ', '_').replace("'", "_").replace('"', '_')

    os.rename(f"{self.getPieceFileDir(folderhash)}/{filename}",
              f"{self.getPieceFileDir(folderhash)}/{newname}")

    data = self.getFileMetaData(folderhash)
    newfile = {}
    newfile["headline"] = str(title)
    newfile["description"] = str(desc)
    newfile["ext"] = "." + extention
    newfile["fname"] = newname.replace(newfile["ext"], '')
    data.append(newfile)
    self.writeFileMetaData(folderhash, data)


  def deleteFileAndMetaData(self, folderhash: str, title) -> None:
    data = self.getFileMetaData(folderhash)
    newdata = []
    data_deleted = {}
    for item in data:
      if item and 'headline' in item.keys():
        if item['headline'] == title:
          data_deleted = item
        else:
          newdata.append(item)

    filename = data_deleted['fname'] + data_deleted['ext']
    os.remove(f"{self.getPieceFileDir(folderhash)}/{filename}")
    self.writeFileMetaData(folderhash, newdata)

  def updateFileName(self, folderhash: str, new_filename: str, title: str) -> None:
    """ Re-upload file requires changing file name """
    extention = new_filename.split('.')[-1]
    newname =  "File_" \
            + "{:.4f}".format(time.time() - int(time.time())).replace("0.","") \
            + "_" + new_filename.replace(' ', '_').replace("'", "_").replace('"', '_')

    olddata = self.getFileMetaData(folderhash)
    oldfilename = ""
    newdata = []
    title_exists = False
    for item in olddata:
      if item["headline"] == title:
        title_exists = True
        # recover old file name
        oldfilename = item["fname"] + item["ext"]
        # change file to new name
        item["ext"] = "." + extention
        item["fname"] = newname.replace(item["ext"], '')
      newdata.append(item)

    if title_exists:
      self.writeFileMetaData(folderhash, newdata)
      os.rename(f"{self.getPieceFileDir(folderhash)}/{new_filename}",
                f"{self.getPieceFileDir(folderhash)}/{newname}")
      os.remove(f"{self.getPieceFileDir(folderhash)}/{oldfilename}")

  def updateFileMetadata(self, folderhash: str, old_title: str, new_title: str, new_desc: str) -> None:
    olddata = self.getFileMetaData(folderhash)
    newdata = []
    title_exists   = False
    something_modified = False
    for item in olddata:
      if item["headline"] == old_title:
        title_exists = True
        # change title and description if not empty
        if new_title.replace(' ',''):
          something_modified = True
          item["headline"] = str(new_title)
        if new_desc.replace(' ',''):
          something_modified = True
          item["description"] = str(new_desc)
      newdata.append(item)

    if title_exists and something_modified:
      self.writeFileMetaData(folderhash, newdata)

# Test
if __name__ == '__main__':
  pass