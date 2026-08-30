#!/usr/bin/python3

from hymnus.filemanager import FileManager
from hymnus.sqlite_adapter import SQLite3Adapter

import os
os.environ['HYMNUS_FS'] = "test_fs"
os.environ['HYMNUS_DB'] = "test.db"

TEST_HASH1 = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaqqqqqqqqqq"
TEST_HASH2 = "zsfklqsfnqslkflkjsqfsnfklqsfnqslkflkjsqf"

def eraseDB():
  SQLite3Adapter().updateRows("DELETE FROM Piece_files;")

def test_upload():
  with open("testfile_txt", "rb") as f:
    FileManager().uploadFile(TEST_HASH1, "testfile.txt", f.read())
    FileManager().uploadFileMetadata(TEST_HASH1, "testfile.txt", "test file 1", "some kind of test file")
    f.seek(0)
    FileManager().uploadFile(TEST_HASH2, "testfile.txt", f.read())
    FileManager().uploadFileMetadata(TEST_HASH2, "testfile.txt", "test file 2", "some kind of test file")

  assert len(FileManager().getPieceFileListDB(TEST_HASH1)) == len(FileManager().getPieceFileListOS(TEST_HASH1))
  with open(FileManager().getPieceFilePathDB(TEST_HASH1, "", "testfile.txt"), 'r') as f:
    assert f.readline() == "FILETESTTESTFILE"

def test_reupload_same_name():
  with open("testfile2_txt", "rb") as f:
    FileManager().reuploadFile(TEST_HASH1, "testfile.txt", "testfile.txt", f.read())
    FileManager().reuploadFileMetadata(TEST_HASH1, "testfile.txt", "testfile.txt")
    f.seek(0)
    FileManager().reuploadFile(TEST_HASH2, "testfile.txt", "testfile.txt", f.read())
    FileManager().reuploadFileMetadata(TEST_HASH2, "testfile.txt", "testfile.txt")

  with open(FileManager().getPieceFilePathDB(TEST_HASH1, "", "testfile.txt"), 'r') as f:
    assert f.readline() == "FILETESTTESTFILEXXXXXXXX"


def test_reupload_different_name():
  with open("testfile_txt", "rb") as f:
    FileManager().reuploadFile(TEST_HASH1, "testfile.txt", "testfile_new.txt", f.read())
    FileManager().reuploadFileMetadata(TEST_HASH1, "testfile.txt", "testfile_new.txt")
    f.seek(0)
    FileManager().reuploadFile(TEST_HASH2, "testfile.txt", "testfile_new.txt", f.read())
    FileManager().reuploadFileMetadata(TEST_HASH2, "testfile.txt", "testfile_new.txt")

  with open(FileManager().getPieceFilePathDB(TEST_HASH1, "", "testfile_new.txt"), 'r') as f:
    assert f.readline() == "FILETESTTESTFILE"

def test_download():
  fh1 = FileManager().downloadFileByName(TEST_HASH1, "testfile_new.txt")
  assert fh1 == b"FILETESTTESTFILE"

  fh2 = FileManager().downloadFileByTitle(TEST_HASH2, "test file 2")
  assert fh2 == b"FILETESTTESTFILE"

def test_deletion():
  FileManager().deleteFileByName(TEST_HASH1, "testfile_new.txt")
  FileManager().deleteFileByName(TEST_HASH2, "testfile_new.txt")

if __name__ == "__main__":
  eraseDB()

  test_upload()

  test_reupload_same_name()

  test_reupload_different_name()

  test_download()

  test_deletion()

  eraseDB()