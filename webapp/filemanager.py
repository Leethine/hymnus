from utilities import SingletonMeta
from db_sqlite import DB_SQLITE
from config import FILESYSTEM_PATH
import os, sys, shutil

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
    

  def getPieceDir(self, folder_hash: str) -> str:
    """ Get the directory path for a given folder_hash. """
    return os.path.join(self.getFSPath(), folder_hash[:2], folder_hash)
  

  def getPieceFileListOS(self, folder_hash: str) -> list:
    """ Get a list of files in the directory corresponding to the given folder_hash. """
    file_list = []
    dir_path = self.getPieceDir(folder_hash)
    if os.path.isdir(dir_path):
      for file_name in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, file_name)):
          file_list.append(file_name)
    return file_list
  

  def getPieceFileListDB(self, folder_hash: str) -> list:
    """ Get a list of files in the directory corresponding to the given folder_hash. """
    selected = DB_SQLITE().selectRows(f"SELECT * FROM piece_files WHERE folder_hash = '{folder_hash}';")
    return selected
  

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
    selected = DB_SQLITE().selectRows(QUERY)
    if len(selected) == 1 and 'file_path' in selected[0].keys():
      return selected[0]['file_path']
    else:
      return ""


  def getPieceFilePathOS(self, folder_hash: str, file_name: str) -> str:
    """ Get the full file path for a given folder_hash and filename. """
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

    for p in piece_files_db:
      fpath = p.get('file_path', '?')
      if not os.path.isfile(fpath):
        return False
    return True


  def rollbackFileUpload(self, folder_hash: str, file_name: str) -> str:
    """ Rollback a file upload by deleting the file from the file system and removing the metadata from the database. """
    file_path = self.getPieceFilePathDB(folder_hash=folder_hash, file_name=file_name, file_title="")
    if os.path.isfile(file_path):
      try:
        os.remove(file_path)
      except Exception as e:
        return f"Failed to delete file from disk: {str(e)}"
    err = DB_SQLITE().updateRows(f"DELETE FROM piece_files WHERE folder_hash = '{folder_hash}' AND file_name = '{file_name}';")
    if err:
      return f"Failed to delete file metadata from DB: {err}"
    return ""


  def uploadFileMetadata(self, folder_hash: str, file_name: str, file_title: str, file_desc: str) -> str:
    """ Create database metadata for a new uploaded file. """
    file_path = os.path.join(self.getPieceDir(folder_hash), file_name)

    # Update DB metadata
    file_extension = os.path.splitext(file_name)[-1].lower()
    select_query = f"SELECT COUNT(*) FROM piece_files WHERE folder_hash = '{folder_hash}' AND file_name = '{file_name}';"
    if DB_SQLITE().countRows(select_query) > 0:
      return "File metadata already exists in DB."
    insert_query = f"INSERT INTO piece_files \
                    (folder_hash, file_path, file_name, file_extension, file_title, file_description) \
                    VALUES ('{folder_hash}', '{file_path}', '{file_name}', '{file_extension}', \
                            '{file_title}' , '{file_desc}');"
    err = DB_SQLITE().updateRows(insert_query)
    return err
  

  def rollbackFileReUpload(self, folder_hash: str, new_file_name: str, old_file_name: str) -> str:
    """ Rollback a re-uploaded file and reset its metadata. """
    old_file_path = self.getPieceFilePathOS(folder_hash, old_file_name)
    new_file_path = self.getPieceFilePathOS(folder_hash, new_file_name)
    if os.path.isfile(new_file_path):
      try:
        os.remove(new_file_path)
      except Exception as e:
        return f"Failed to rename file on disk: {str(e)}"
    
    err = DB_SQLITE().updateRows(f"UPDATE piece_files SET last_modified = CURRENT_TIMESTAMP, \
                                   file_path  = '{old_file_path}', file_name = '{old_file_name}' \
                                   WHERE folder_hash = '{folder_hash}' AND file_name = '{new_file_name}';")
    if err:
      return f"Failed to restore DB metadata: {err}"
    return ""


  def reUploadFileMetadata(self, folder_hash: str, new_file_name: str, old_file_name: str) -> str:
    """ Update database metadata for a re-uploaded file. """
    if new_file_name == old_file_name:
      return "Cannot re-upload file with the same name."

    file_path = os.path.join(self.getPieceDir(folder_hash), new_file_name)
    file_extension = os.path.splitext(new_file_name)[-1].lower()

    # Check metadata and extension
    old_file_metadata = DB_SQLITE().selectRows( \
      f"SELECT * FROM piece_files WHERE folder_hash = '{folder_hash}' AND file_name = '{old_file_name}';")
    if not old_file_metadata or len(old_file_metadata) != 1:
      return "File metadata does not exist in DB, or duplicate entries found."
    old_extension = old_file_metadata[0].get('file_extension', '')
    if old_extension != file_extension:
      return "File extension cannot be changed when re-uploading file."

    update_query = f"UPDATE piece_files SET last_modified = CURRENT_TIMESTAMP, \
                    file_path = '{file_path}', file_name = '{new_file_name}'   \
                    WHERE folder_hash = '{folder_hash}' AND file_name = '{old_file_name}';"
    err = DB_SQLITE().updateRows(update_query)
    return err


  def modifyFileMetadata(self, folder_hash: str, old_title: str, new_title="", new_description="") -> str:
    """ Modify the metadata of a file in the file system. """
    if DB_SQLITE().countRows(f"SELECT COUNT(*) FROM piece_files WHERE \
                               folder_hash = '{folder_hash}' AND \
                               file_title = '{old_title}';") != 1:
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
                    WHERE folder_hash = '{folder_hash}' AND file_title = '{old_title}' ;"
    err = DB_SQLITE().updateRows(update_query)
    if err:
      return f"Failed to update file metadata, DB error: {err}"
    return ""
  

  def deleteFileByTitle(self, folder_hash: str, file_title: str) -> str:
    if DB_SQLITE().countRows(f"SELECT COUNT(*) FROM piece_files WHERE \
                               folder_hash = '{folder_hash}' AND \
                               file_title = '{file_title}';") == 1:
      file_metadata = DB_SQLITE().selectRows(f"SELECT * FROM piece_files WHERE \
                                              folder_hash = '{folder_hash}' AND \
                                              file_title = '{file_title}';")
      if len(file_metadata) != 1 or 'file_name' not in file_metadata[0].keys():
        return "File metadata is corrupted in DB, cannot delete file"
      
      file_path = self.getPieceFilePathOS(folder_hash, file_metadata[0]['file_name'])
      if os.path.isfile(file_path):
        os.remove(file_path)
      
      err = DB_SQLITE().updateRows(f"DELETE FROM piece_files WHERE \
                                     folder_hash = '{folder_hash}' AND \
                                     file_title = '{file_title}';")
      if err:
        return f"Failed to delete file metadata from DB: {err}"
      return ""
    else:
      return "File does not exist in DB, cannot delete"
  

  def deleteFileByName(self, folder_hash: str, file_name: str) -> str:
    if DB_SQLITE().countRows(f"SELECT COUNT(*) FROM piece_files WHERE \
                               folder_hash = '{folder_hash}' AND \
                               file_name = '{file_name}';") == 1:
      file_metadata = DB_SQLITE().selectRows(f"SELECT * FROM piece_files WHERE \
                                              folder_hash = '{folder_hash}' AND \
                                              file_name = '{file_name}';")
      if len(file_metadata) != 1 or 'file_name' not in file_metadata[0].keys():
        return "File metadata is corrupted in DB, cannot delete file"
      
      file_path = self.getPieceFilePathOS(folder_hash, file_metadata[0]['file_name'])
      if os.path.isfile(file_path):
        os.remove(file_path)
      
      err = DB_SQLITE().updateRows(f"DELETE FROM piece_files WHERE \
                                     folder_hash = '{folder_hash}' AND \
                                     file_name = '{file_name}';")
      if err:
        return f"Failed to delete file metadata from DB: {err}"
      return ""
    else:
      return "File does not exist in DB, cannot delete"
  

  def deleteAllFiles(self, folder_hash: str) -> str:
    """ Delete all files associated with a piece from the file system. """
    dir_path = os.path.abspath(self.getPieceDir(folder_hash))
    if os.path.isdir(dir_path):
      try:
        shutil.rmtree(dir_path)
      except Exception as e:
        return f"Failed to delete files from disk: {str(e)}"
    
    err = DB_SQLITE().updateRows(f"DELETE FROM piece_files WHERE folder_hash = '{folder_hash}';")
    if err:
      return f"Failed to delete metadata from DB: {err}"
    return ""


  def downloadFile(self, folder_hash: str, file_name: str) -> bytes:
    """ Download a file from the file system. """
    file_path = self.getPieceFilePathOS(folder_hash, file_name)
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
  

  def fileExists(self, folder_hash: str, file_name: str) -> bool:
    """ Check if a file exists in the file system. """
    file_path = self.getPieceFilePathOS(folder_hash, file_name)
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

