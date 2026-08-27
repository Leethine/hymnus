import importlib
import os, sys, shutil

if importlib.util.find_spec('hymnus') is not None:
  from hymnus.utilities import SingletonMeta
  from hymnus.sqlite_adapter import SQLite3Adapter
  from hymnus.CONFIG import FILESYSTEM_PATH
else:
  from hymnus.utilities import SingletonMeta
  from hymnus.sqlite_adapter import SQLite3Adapter
  from hymnus.CONFIG import FILESYSTEM_PATH


class FileManager(metaclass=SingletonMeta):
  """ FileManager is responsible for managing the score library file system. """

  def getFSPath(self) -> str:
    """ Get the root path of the file system. """
    if 'HYMNUS_FS' in os.environ.keys() and os.path.isdir(os.environ['HYMNUS_FS']):
      return os.path.abspath(os.environ['HYMNUS_FS'])
    elif os.path.isdir(FILESYSTEM_PATH):
      return os.path.abspath(FILESYSTEM_PATH)
    else:
      return os.path.abspath("./")

  
  def getPieceDirReplaceStr(self) -> str:
    """ Get the string to be replaced with the piece directory in DB table. """
    return "#$%PIECEDIR%$#"


  def getPieceDir(self, folder_hash: str) -> str:
    """ Get the directory path for a given folder_hash. """
    return os.path.join(self.getFSPath(), folder_hash[:2], folder_hash)


  def getPieceFileMetadataList(self, folder_hash: str) -> list:
    """ Get the list of file metadata for a given folder_hash from DB. """
    selected = SQLite3Adapter().selectRows(f"SELECT * FROM piece_files WHERE folder_hash = '{folder_hash}';")
    for row in selected:
      if 'file_path' in row.keys():
        # Replace absolute path with replacement string
        row['file_path'] = row['file_path'].replace(self.getPieceDirReplaceStr(), self.getPieceDir(folder_hash))
    return selected


  def getPieceFileListOS(self, folder_hash: str) -> list:
    """ Get a list of files in the directory corresponding to the given folder_hash by scanning the file system.
        Not recommended for production use; for monitoring/debugging only.
    """
    file_list = []
    dir_path = self.getPieceDir(folder_hash)
    if os.path.isdir(dir_path):
      for file_name in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, file_name)):
          file_list.append(file_name)
    return file_list


  def getPieceFileListDB(self, folder_hash: str) -> list:
    """ Get a list of files in the directory corresponding to the given folder_hash from DB."""
    selected = SQLite3Adapter().selectRows(f"SELECT * FROM piece_files WHERE folder_hash = '{folder_hash}';")
    flist = []
    for row in selected:
      if 'file_path' in row.keys():
        flist.append(row['file_path'].replace(self.getPieceDirReplaceStr(), self.getPieceDir(folder_hash)))
    return flist


  def getPieceFilePathDB(self, folder_hash: str, file_title: str, file_name: str) -> str:
    """ Get the full file path from DB for a given folder_hash, then file_name or file_title (at least one). """
    if file_name and file_title:
      QUERY = f"SELECT * FROM piece_files WHERE folder_hash = '{folder_hash}' \
                AND file_name = '{file_name}' AND file_title = '{file_title}';"
    elif file_title:
      QUERY = f"SELECT * FROM piece_files WHERE folder_hash = '{folder_hash}' \
                AND file_title = '{file_title}';"
    elif file_name:
      QUERY = f"SELECT * FROM piece_files WHERE folder_hash = '{folder_hash}' \
                AND file_name = '{file_name}';"
    else:
      return ""
    selected = SQLite3Adapter().selectRows(QUERY)
    if len(selected) == 1 and 'file_path' in selected[0].keys():
      return selected[0]['file_path'].replace(self.getPieceDirReplaceStr(), self.getPieceDir(folder_hash))
    else:
      return ""


  def getPieceFilePathOS(self, folder_hash: str, file_name: str) -> str:
    """ Get the full file path for a given folder_hash and filename.
        Not recommended for production use; for monitoring/debugging only.
    """
    dir_path = self.getPieceDir(folder_hash)
    if not os.path.isdir(dir_path):
      os.makedirs(dir_path)
    return os.path.join(dir_path, file_name)

  
  def verifyFileList(self, folder_hash: str) -> bool:
    """ Verify that the files in the directory match the metadata in the database. """
    piece_files_db = self.getPieceFileListDB(folder_hash)
    piece_files_fs = self.getPieceFileListOS(folder_hash)
    if len(piece_files_fs) != len(piece_files_db):
      return False

    for fpath in piece_files_db:
      if not os.path.isfile(fpath):
        return False
    return True


  def uploadFile(self, folder_hash: str, file_name: str, file_blob: bytes):
    file_path = os.path.join(self.getPieceDir(folder_hash), file_name)
    if os.path.isfile(file_path):
      os.remove(file_path)
    with open(file_path, 'wb') as f:
      f.write(file_blob)


  def reuploadFile(self, folder_hash: str, old_file_name: str, new_file_name: str, file_blob: bytes):
    old_file_path = os.path.join(self.getPieceDir(folder_hash), old_file_name)
    new_file_path = os.path.join(self.getPieceDir(folder_hash), new_file_name)
    if os.path.isfile(old_file_path):
      os.remove(old_file_path)
    if os.path.isfile(new_file_path):
      os.remove(new_file_path)
    with open(new_file_path, 'wb') as f:
      f.write(file_blob)


  def uploadFileMetadata(self, folder_hash: str, file_name: str, file_title: str, file_desc: str) -> str:
    """ Create database metadata for a new uploaded file. """
    file_path = os.path.join(self.getPieceDir(folder_hash), file_name)
    file_path = file_path.replace(self.getPieceDir(folder_hash), self.getPieceDirReplaceStr())

    # Update DB metadata
    file_extension = os.path.splitext(file_name)[-1].lower()
    QUERY_COUNT = f"SELECT COUNT(*) FROM piece_files WHERE folder_hash = '{folder_hash}' AND file_name = '{file_name}';"
    if SQLite3Adapter().countRows(QUERY_COUNT) > 0:
      return f"File metadata already exists in DB: \n{folder_hash} - {file_name} - {file_title}"
    INSERT_SQL = f"INSERT INTO piece_files \
                    (folder_hash, file_path, file_name, file_extension, file_title, file_description) \
                   VALUES ('{folder_hash}', '{file_path}', '{file_name}', \
                           '{file_extension}', '{file_title}' , '{file_desc}');"
    err = SQLite3Adapter().updateRows(INSERT_SQL)
    return err


  def reuploadFileMetadata(self, folder_hash: str, new_file_name: str, old_file_name: str) -> str:
    """ Update database metadata for a re-uploaded file. """
    file_path = os.path.join(self.getPieceDir(folder_hash), new_file_name)
    file_path = file_path.replace(self.getPieceDir(folder_hash), self.getPieceDirReplaceStr())
    file_extension = os.path.splitext(new_file_name)[-1].lower()

    # Check dulpicate
    old_file_metadata = SQLite3Adapter().selectRows( \
      f"SELECT * FROM piece_files WHERE folder_hash = '{folder_hash}' AND file_name = '{old_file_name}';")
    if not old_file_metadata or len(old_file_metadata) != 1:
      return f"File metadata does not exist in DB, or duplicate entries found. \
               \n{folder_hash} - {new_file_name} - {old_file_name}"
    # Check if extension remains the same
    old_extension = old_file_metadata[0].get('file_extension', '')
    if old_extension != file_extension:
      return f"File extension cannot be changed when re-uploading file."
    # Update DB
    UPDATE_SQL = f"UPDATE piece_files SET last_modified = CURRENT_TIMESTAMP, \
                     file_path = '{file_path}', file_name = '{new_file_name}'   \
                   WHERE folder_hash = '{folder_hash}' AND file_name = '{old_file_name}';"
    if old_file_name != new_file_name:
      err = SQLite3Adapter().updateRows(UPDATE_SQL)
    return err


  def modifyFileMetadata(self, folder_hash: str, old_title: str, new_title="", new_description="") -> str:
    """ Modify the metadata of a file in the file system. """
    count = SQLite3Adapter().countRows( \
      f"SELECT COUNT(*) FROM piece_files WHERE \
        folder_hash = '{folder_hash}' AND file_title = '{old_title}';")
    if count != 1:
      return f"File title \"{old_title}\" does not exist in DB."
    
    update_fields = ""
    if new_title:
      update_fields += f", file_title = '{new_title}'"
    if new_description:
      update_fields += f" , file_description = '{new_description}' "
    if not update_fields:
      # no update provided, nothing to do
      return ""
    
    UPDATE_SQL = f"UPDATE piece_files SET last_modified = CURRENT_TIMESTAMP \
                    {update_fields} \
                   WHERE folder_hash = '{folder_hash}' AND file_title = '{old_title}' ;"
    err = SQLite3Adapter().updateRows(UPDATE_SQL)
    if err:
      return f"Failed to update file metadata, DB error: {err}"
    return ""


  def deleteFileByTitle(self, folder_hash: str, file_title: str) -> str:
      # Get file path and delete it
      file_path = self.getPieceFilePathDB(folder_hash=folder_hash, \
                                          file_title=file_title, \
                                          file_name="")
      if file_path and os.path.isfile(file_path):
        os.remove(file_path)
        err = SQLite3Adapter().updateRows( \
          f"DELETE FROM piece_files WHERE \
            folder_hash = '{folder_hash}' AND file_title = '{file_title}';")
        if err:
          return f"Failed to delete file metadata from DB: {err}"
        return ""
      else:
        return f"Cannot find file by title \"{file_title}\", DB might be corrupt."


  def deleteFileByName(self, folder_hash: str, file_name: str) -> str:
      # Get file path and delete it
      file_path = self.getPieceFilePathDB(folder_hash=folder_hash, \
                                          file_title="", \
                                          file_name=file_name)
      if file_path and os.path.isfile(file_path):
        os.remove(file_path)
        err = SQLite3Adapter().updateRows( \
          f"DELETE FROM piece_files WHERE \
            folder_hash = '{folder_hash}' AND file_name = '{file_name}';")
        if err:
          return f"Failed to delete file metadata from DB: {err}"
        return ""
      else:
        return f"Cannot find file by name \"{file_name}\", DB might be corrupt."


  def downloadFileByName(self, folder_hash: str, file_name: str) -> bytes:
    """ Download a file from the file system. """
    file_path = self.getPieceFilePathDB(folder_hash=folder_hash, file_title="", file_name=file_name)
    if os.path.isfile(file_path):
      try:
        with open(file_path, 'rb') as f:
          return f.read()
      except Exception as e:
        print(f"Failed to read file from disk: {str(e)}", file=sys.stderr)
        return b""
    else:
      print("File does not exist on disk.", file=sys.stderr)
      return b""


  def downloadFileByTitle(self, folder_hash: str, file_title: str) -> bytes:
    """ Download a file from the file system. """
    file_path = self.getPieceFilePathDB(folder_hash=folder_hash, file_title=file_title, file_name="")
    if os.path.isfile(file_path):
      try:
        with open(file_path, 'rb') as f:
          return f.read()
      except Exception as e:
        print(f"Failed to read file from disk: {str(e)}", file=sys.stderr)
        return b""
    else:
      print("File does not exist on disk.", file=sys.stderr)
      return b""


  def checkFileExistsByName(self, folder_hash: str, file_name: str) -> bool:
    """ Check if a file exists in the file system. """
    file_path = self.getPieceFilePathDB(folder_hash=folder_hash, file_title="", file_name=file_name)
    return os.path.isfile(file_path)


  def checkFileExistsByTitle(self, folder_hash: str, file_title: str) -> bool:
    """ Check if a file exists in the file system. """
    file_path = self.getPieceFilePathDB(folder_hash=folder_hash, file_title=file_title, file_name="")
    return os.path.isfile(file_path)


  def deletePieceFiles(self, folder_hash: str) -> str:
    """ Delete all files associated with a piece from the file system. """
    dir_path = os.path.abspath(self.getPieceDir(folder_hash))
    if os.path.isdir(dir_path):
      try:
        shutil.rmtree(dir_path)
      except Exception as e:
        return f"Failed to delete files from disk: {str(e)}"
    
    err = SQLite3Adapter().updateRows(f"DELETE FROM piece_files WHERE folder_hash = '{folder_hash}';")
    if err:
      return f"Failed to delete file metadata from DB: {err}"
    return ""
  

  def deleteOwnerlessFiles(self) -> str:
    """ Delete files in DB and File system if nothing found in Pieces table. """
    err = ""
    for piece in SQLite3Adapter().selectRows( \
      f"SELECT * FROM Piece_files WHERE folder_hash NOT IN (SELECT folder_hash FROM Pieces);" ):
      piece_hash = piece.get('folder_hash', '')
      if piece_hash:
        err = self.deletePieceFiles(piece_hash)
      if err:
        return f"Error occurred while deleting piece files and metadata: \n {piece_hash} \n {err}"
    err = SQLite3Adapter().updateRows( \
      f"DELETE FROM Piece_files WHERE folder_hash NOT IN (SELECT folder_hash FROM Pieces);");
    return f"Error occurred while deleting all ownerless metadata: {err}"
