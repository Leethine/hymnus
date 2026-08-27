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

def test_create_piece():
  err = SQLiteMetadataWriter().createPiece(composer_code='bach_j_s', title="Prelude and Fugue in C Minor", \
                                           subtitle="Test1", subsubtitle="Test2", opus="BWV 546", dedicated="Test3", \
                                           arranger_code="", arranger_name="", year="?", instruments="Organ", comment="TeTeTest")
  assert len(err) == 40 and ' ' not in err, f"Error occurred: {err}"

  err = SQLiteMetadataWriter().createPiece(composer_code='bach_j_s', title="Prelude and Fugue in C Minor", \
                                           subtitle="Arranged by Beethoven", subsubtitle="Test2", opus="BWV 546", dedicated="Test3", \
                                           arranger_code="beethoven_l", arranger_name="", year="?", instruments="Piano", comment="TeTeTest")
  assert len(err) == 40 and ' ' not in err, f"Error occurred: {err}"

  err = SQLiteMetadataWriter().createPiece(composer_code='brahms_j', title="DansePiano Concerto", \
                                           subtitle="No. 1", subsubtitle="D minor", opus="Op.15", dedicated="Test3", \
                                           arranger_code="brahms_j", arranger_name="", year="?", instruments="Piano,Orchestra")
  assert len(err) == 40 and ' ' not in err, f"Error occurred: {err}"


def test_get_piece():
  selection = SQLiteMetadataReader().getAllPieces()
  assert len(selection) == 3, f"Assertion failed; Expected 3, Got {len(selection)}"
  selection = SQLiteMetadataReader().getPartialPieces(1,1)
  assert len(selection) == 1, f"Assertion failed; Expected 1, Got {len(selection)}"
  selection = SQLiteMetadataReader().getPartialPieces(2,1)
  assert len(selection) == 1, f"Assertion failed; Expected 1, Got {len(selection)}"
  selection = SQLiteMetadataReader().getComposerPieces('brahms_j')
  assert len(selection) == 1, f"Assertion failed; Expected 1, Got {len(selection)}"

def test_delete_piece():
  for p in SQLiteMetadataReader().getComposerPieces('bach_j_s'):
    err = SQLiteMetadataWriter().deletePiece(p['folder_hash'])
    assert not err, f"Error occurred: {err}"
  selection = SQLiteMetadataReader().getAllPieces()
  assert len(selection) == 1, f"Assertion failed; Expected 1, Got {len(selection)}"

def test_create_collection():
  err = SQLiteMetadataWriter().createCollection("Test collection 1")
  assert len(err) == 10 and ' ' not in err, f"Error occurred: {err}"
  collectioncode1 = err
  err = SQLiteMetadataWriter().createCollection("Test collection 2")
  assert len(err) == 10 and ' ' not in err, f"Error occurred: {err}"
  collectioncode2 = err

  # verify if collections are created
  count = SQLiteMetadataReader().countCollections()
  assert count == 2, f"Assertion failed; Expected 2, Got {count}"

  # Add pieces to colleciton
  for piece in SQLiteMetadataReader().getAllPieces():
    err = SQLiteMetadataWriter().addPieceToCollection(piece['folder_hash'], collectioncode2)
    assert not err, f"Error occurred: {err}"
    err = SQLiteMetadataWriter().addPieceToCollection(piece['folder_hash'], collectioncode1)
    assert not err, f"Error occurred: {err}"
    # test duplicated add
    err = SQLiteMetadataWriter().addPieceToCollection(piece['folder_hash'], collectioncode1)
    assert not err, f"Error occurred: {err}"

  # Verify collections have the correct number of pieces
  selected = SQLiteMetadataReader().getCollectionPieces(collectioncode1)
  assert len(selected) == 3, f"Assertion failed; Expected 3, Got {len(selected)}"
  selected = SQLiteMetadataReader().getCollectionPieces(collectioncode2)
  assert len(selected) == 3, f"Assertion failed; Expected 3, Got {len(selected)}"

  # Delete pieces from colleciton1
  for piece in SQLiteMetadataReader().getAllPieces():
    err = SQLiteMetadataWriter().rmPieceFromCollection(piece['folder_hash'], collectioncode1)
    assert not err, f"Error occurred: {err}"
  # Verify that collection1 is empty
  selected = SQLiteMetadataReader().getCollectionPieces(collectioncode1)
  assert len(selected) == 0, f"Assertion failed; Expected 0, Got {len(selected)}"

def test_delete_composer():
  err = SQLiteMetadataWriter().deleteComposer('bach_j_s', True)
  assert not err, f"Error occurred: {err}"
  count = SQLiteMetadataReader().countComposers(listed_only=False)
  assert count == 2, f"Assertion failed; Expected 2, Got {count}"
  count = SQLiteMetadataReader().countPieces()
  assert count == 1, f"Assertion failed; Expected 1, Got {count}"

def test_delete_collection():
  # Select first collection
  selection1 = SQLiteMetadataReader().getPartialCollections(1,1)
  assert len(selection1) == 1, f"Assertion failed; Expected 1, Got {len(selection1)}"
  # Select second collection
  selection2 = SQLiteMetadataReader().getPartialCollections(2,1)
  assert len(selection2) == 1, f"Assertion failed; Expected 1, Got {len(selection2)}"

  # Delete collection without deleting pieces
  SQLiteMetadataWriter().deleteCollection(selection1[0]['code'], False)
  count = SQLiteMetadataReader().countPieces()
  assert count > 0, f"Assertion failed; Expected > 0, Got {count}"

  # Delete collection and delete pieces
  SQLiteMetadataWriter().deleteCollection(selection2[0]['code'], True)
  count = SQLiteMetadataReader().countPieces()
  assert count == 0, f"Assertion failed; Expected 0, Got {count}"

  count = SQLiteMetadataReader().countCollections()
  assert count == 0, f"Assertion failed; Expected 0, Got {count}"


if __name__ == "__main__":

  ## Test 1
  eraseDB()

  # Create 3 composers
  test_create_composer()

  # Check composer created
  test_get_composer()

  # create works then delete one
  test_create_piece()
  test_get_piece()
  test_delete_piece()

  # Test delete composer, should also delete works
  test_delete_composer()


  ## Test 2
  eraseDB()

  # Create 3 composers
  test_create_composer()
  
  # create works
  test_create_piece()
  test_get_piece()
  
  # Test create collection and add pieces
  test_create_collection()

  # Test delete collection, should also remove pieces
  test_delete_collection()

  # clean up
  eraseDB()