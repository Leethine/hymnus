import sys
sys.path.append("../migrate/")

from metadata import Metadata
from db_sqlite import DB_SQLITE
import os

os.environ['HYMNUS_DB'] = "test.db"

def eraseDB():
  DB_SQLITE().updateRows("DELETE FROM Pieces;")
  DB_SQLITE().updateRows("DELETE FROM Piece_search;")
  DB_SQLITE().updateRows("DELETE FROM Composers;")
  DB_SQLITE().updateRows("DELETE FROM Collections;")

if __name__ == "__main__":
  eraseDB()

  ret = Metadata().writer().createComposer("Foo", "Bar", "Foo bar", "1900", "1950")
  assert Metadata().reader().composerExists(ret) == True or print(f"Error: {ret}")
  ret = Metadata().writer().createComposer("Baz", "Qux", "Baz qux")
  assert Metadata().reader().composerExists(ret) == True or print(f"Error: {ret}")

  ret = Metadata().writer().createPiece("bar_f", title="Bar Tétété hîhôhö")
  assert Metadata().reader().pieceExists(ret) == True or print(f"Error: {ret}")

  ret = Metadata().writer().createPiece(composer_code="bar_f", title="Tîtlé ë", subtitle="sub", subsubtitle="subsub", \
                                        opus="op1", dedicated="someone", arranger_code="", arranger_name="Unknown", collection_code="", \
                                        year="1111", instruments="Many", comment="Something")
  assert Metadata().reader().pieceExists(ret) == True or print(f"Error: {ret}")

  ret = Metadata().writer().createCollection(title="Collection 1", subtitle="Subtitle 1", subsubtitle="Subsubtitle 1", editor="Editor 1");
  assert Metadata().reader().collectionExists(ret) == True or print(f"Error: {ret}")

  composers = Metadata().reader().getAllComposers(listed_only=False)
  pieces = Metadata().reader().getAllPieces()
  collections = Metadata().reader().getAllCollections()
  
  assert len(composers) == 2 or print("Error: composer count mismatch")
  assert len(pieces) == 2 or print("Error: piece count mismatch")
  assert len(collections) == 1 or print("Error: collection count mismatch")

  composers1 = Metadata().reader().getPartialComposers(items_per_page=1, page_number=1, listed_only=False)
  composers2 = Metadata().reader().getPartialComposers(items_per_page=1, page_number=2, listed_only=False)

  print(Metadata().reader().getPartialPieces(items_per_page=2, page_number=2))

  assert len(composers1) == 1 or print("Error: composer1 count mismatch")
  assert len(composers2) == 1 or print("Error: composer2 count mismatch")
  assert composers1[0]['code'] != composers2[0]['code'] or print("Error: composer1 and composer2 should be different")


  Metadata().writer().deleteComposer("bar_f", deleted_associated_works=True)

  assert Metadata().reader().countComposers() == 1 or print("Error: composer count mismatch")
  assert Metadata().reader().countPieces() == 0 or print("Error: piece count mismatch")

  print("All tests passed!")
  eraseDB()