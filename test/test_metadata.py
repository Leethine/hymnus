#!/usr/bin/python3

from hymnus.metadata import SQLiteMetadataReader, SQLiteMetadataWriter
from hymnus.sqlite_adapter import SQLite3Adapter

import os

os.environ['HYMNUS_DB'] = "test.db"

def eraseDB():
  SQLite3Adapter().updateRows("DELETE FROM Pieces;")
  SQLite3Adapter().updateRows("DELETE FROM Piece_search;")
  SQLite3Adapter().updateRows("DELETE FROM Composers;")
  SQLite3Adapter().updateRows("DELETE FROM Collections;")

def test_create_composer():
  err = SQLiteMetadataWriter().createComposer("Johann Sebastian", "Bach", "Johann Sebastian Bach", "1685", "1750")
  assert err == "bach_j_s", f"Error occurred: {err}"
  err = SQLiteMetadataWriter().createComposer("Ludwig", "Beethoven", "Ludwig van Beethoven", "1770", "1827")
  assert err == "beethoven_l", f"Error occurred: {err}"
  err = SQLiteMetadataWriter().createComposer("Johannes", "Brahms", "Johannes Brahms", "1833", "1897")
  assert err == "brahms_j", f"Error occurred: {err}"

def test_get_composer():
  selection = SQLiteMetadataReader().getAllComposers(listed_only=False)
  assert len(selection) == 3, f"Assertion failed; Expected 3, Got {len(selection)}"
  selection = SQLiteMetadataReader().getPartialComposers(page_number=1, items_per_page=2, listed_only=False)
  assert len(selection) == 2, f"Assertion failed; Expected 2, Got {len(selection)}"
  selection = SQLiteMetadataReader().getPartialComposers(page_number=2, items_per_page=2, listed_only=False)
  assert len(selection) == 1, f"Assertion failed; Expected 1, Got {len(selection)}"

def test_delete_composer():
  err = SQLiteMetadataWriter().deleteComposer('bach_j_s')
  assert not err, f"Error occurred: {err}"
  count = SQLiteMetadataReader().countComposers(listed_only=False)
  assert count == 2, f"Assertion failed; Expected 2, Got {count}"

if __name__ == "__main__":
  eraseDB()

  test_create_composer()
  test_get_composer()
  test_delete_composer()

  eraseDB()