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


  def getSimpleSubmitPage(self) -> str:
    return '''
      <!doctype html>
      <title>Upload new File</title>
      <h1>Upload new File</h1>
      <form method="post" enctype="multipart/form-data">
        <input type="file" name="file" id="file-upload">
        <br>
        <input type="text" name="title" placeholder="File title">
        <br>
        <textarea type="text" name="description" rows="3">File description</textarea>
        <br>
        <input type="text" name="user" placeholder="User Name">
        <input type="password" name="password" placeholder="Password">
        <br>
        <input type="submit" value="Upload">
      </form>
      <script>
      const uploadFile = document.getElementById("file-upload");
      uploadFile.onchange = function() {
        if (this.files.length > 0) {
          var filesize = ((this.files[0].size/1024)/1024).toFixed(4);
          if (filesize > 5) {
            alert("File too big! (> 5MB)");
            this.value = "";
          }
        }
      };
      </script>
    '''


  def getSimpleDeletePage(self, folderhash: str) -> str:
    data = self.getFileMetaData(folderhash)
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
    HTMLFORM += '</select><br>'
    HTMLFORM += '<input type="text" name="user" placeholder="User Name">'
    HTMLFORM += '<input type="password" name="password" placeholder="Password">'
    HTMLFORM += '<br><input type="submit" value="Delete"></form>'
    return HTMLFORM
    
  
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


# Test
if __name__ == '__main__':
  pass