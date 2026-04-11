from utilities import SingletonMeta
from db_sqlite import DB_SQLITE
from config import FILESYSTEM_PATH
import os, sys, shutil

class FileManager(metaclass=SingletonMeta):
  """ FileManager is responsible for managing the score library file system. """

  def getFSPath(self) -> str:
    """ Get the root path of the file system. """
    if 'HYMNUS_FS' in os.environ.keys():
      return os.environ['HYMNUS_FS']
    elif os.path.isdir(FILESYSTEM_PATH):
      return FILESYSTEM_PATH
    else:
      return "./"
    

  def getPieceDir(self, folder_hash: str) -> str:
    """ Get the directory path for a given folder_hash. """
    return f"{self.getFSPath()}/{folder_hash[:2]}/{folder_hash}"
  

  def getPieceFileListOS(self, folder_hash: str) -> list:
    """ Get a list of files in the directory corresponding to the given folder_hash. """
    file_list = []
    dir_path = self.getPieceDir(folder_hash)
    if os.path.isdir(dir_path):
      for filename in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, filename)):
          file_list.append(filename)
    return file_list
  
  def getPieceFileListDB(self, folder_hash: str) -> list:
    """ Get a list of files in the directory corresponding to the given folder_hash. """
    selected = DB_SQLITE().selectRows(f"SELECT * FROM piece_files WHERE folder_hash = '{folder_hash}';")
    return selected
  

  def getPieceFilePathDB(self, folder_hash: str, filename: str) -> str:
    """ Get the full file path from DB for a given folder_hash and filename. """
    selected = DB_SQLITE().selectRows(f"SELECT * FROM piece_files WHERE folder_hash = \
                                      '{folder_hash}' AND file_name = '{filename}';")
    if len(selected) == 1 and 'file_path' in selected[0].keys():
      return selected[0]['file_path']
    else:
      return ""


  def getPieceFilePathOS(self, folder_hash: str, filename: str) -> str:
    """ Get the full file path for a given folder_hash and filename. """
    dir_path = os.path.abspath(self.getPieceDir(folder_hash))
    if not os.path.isdir(dir_path):
      os.makedirs(dir_path)
    return f"{dir_path}/{filename}"

  
  def verifyFileList(self, folder_hash: str) -> bool:
    """ Verify that the files in the directory match the metadata in the database. """
    piece_files_db = self.getPieceFileListDB(folder_hash)
    piece_files_fs = self.getPieceFileListOS(folder_hash)
    if len(piece_files_fs) != len(piece_files_db):
      return False

    for p in piece_files_db:
      fpath = p.get('file_path', '?')
      if not os.path.isfile(fpath):
        return False
    return True
  

  def uploadFile(self, folder_hash: str, filename: str, file_title: str, \
                 file_desc: str, file_content: bytes) -> str:
    """ Upload a file to the file system and update the database metadata. """
    file_path = self.getPieceFilePathOS(folder_hash, filename)
    try:
      with open(file_path, 'wb') as f:
        f.write(file_content)
    except Exception as e:
      return f"Failed to write file to disk: {str(e)}"

    # Update DB metadata
    file_extension = os.path.splitext(filename)[1]
    insert_query = f"INSERT INTO piece_files \
                    (folder_hash, file_path, file_name, file_extension, file_title, file_description) \
                    VALUES ('{folder_hash}', '{file_path}', '{filename}', '{file_extension}', \
                            '{file_title}', '{file_desc}');"
    err = DB_SQLITE().updateRows(insert_query)
    if err:
      # Rollback file write if DB update fails
      os.remove(file_path)
      return f"Failed to update DB metadata: {err}"
    return ""
  

  def replaceFile(self, folder_hash: str, filename: str, file_content: bytes) -> str:
    """ Upload a file to the file system and update the database metadata. """
    file_path = self.getPieceFilePathOS(folder_hash, filename)
    try:
      with open(file_path, 'wb') as f:
        f.write(file_content)
    except Exception as e:
      return f"Failed to write file to disk: {str(e)}"

    # Update DB metadata
    insert_query = f"UPDATE piece_files SET last_modified = CURRENT_TIMESTAMP \
                     WHERE folder_hash = '{folder_hash}' AND file_name = '{filename}' ;"
    err = DB_SQLITE().updateRows(insert_query)
    if err:
      return f"Failed to update DB metadata: {err}"
    return ""
  

  def modifyFileMetadata(self, folder_hash: str, filename: str, new_title="", new_description="") -> str:
    """ Modify the metadata of a file in the file system. """
    if DB_SQLITE().countRows(f"SELECT COUNT(*) FROM piece_files WHERE \
                               folder_hash = '{folder_hash}' AND \
                               file_name = '{filename}';") != 1:
      return "File does not exist in DB, cannot modify metadata"
    
    update_fields = ""
    if new_title:
      update_fields += f", file_title = '{new_title}'"
    if new_description:
      update_fields += f" , file_description = '{new_description}' "

    if not update_fields:
      return ""
    
    update_query = f"UPDATE piece_files SET last_modified = CURRENT_TIMESTAMP \
                    {update_fields} \
                    WHERE folder_hash = '{folder_hash}' AND file_name = '{filename}' ;"
    err = DB_SQLITE().updateRows(update_query)
    if err:
      return f"Failed to update file metadata, DB error: {err}"
    return ""
  

  def deleteFile(self, folder_hash: str, filename: str) -> str:
    if DB_SQLITE().countRows(f"SELECT COUNT(*) FROM piece_files WHERE \
                               folder_hash = '{folder_hash}' AND \
                               file_name = '{filename}';") == 1:
      file_path = self.getPieceFilePathOS(folder_hash, filename)
      if os.path.isfile(file_path):
        os.remove(file_path)
      
      err = DB_SQLITE().updateRows(f"DELETE FROM piece_files WHERE \
                                     folder_hash = '{folder_hash}' AND \
                                     file_name = '{filename}';")
      if err:
        return f"Failed to delete file metadata from DB: {err}"
      return ""
    else:
      return "File does not exist in DB, cannot delete"


  def downloadFile(self, folder_hash: str, filename: str) -> bytes:
    """ Download a file from the file system. """
    file_path = self.getPieceFilePathOS(folder_hash, filename)
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
  

  def fileExists(self, folder_hash: str, filename: str) -> bool:
    """ Check if a file exists in the file system. """
    file_path = self.getPieceFilePathOS(folder_hash, filename)
    return os.path.isfile(file_path)
  

  def deletePieceFiles(self, folder_hash: str) -> str:
    """ Delete all files associated with a piece from the file system. """
    dir_path = os.path.abspath(self.getPieceDir(folder_hash))
    if os.path.isdir(dir_path):
      try:
        shutil.rmtree(dir_path)
      except Exception as e:
        return f"Failed to delete files from disk: {str(e)}"
    
    err = DB_SQLITE().updateRows(f"DELETE FROM piece_files WHERE folder_hash = '{folder_hash}';")
    if err:
      return f"Failed to delete file metadata from DB: {err}"
    return ""

