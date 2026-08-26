import hashlib
from utilities import SingletonMeta, toAscii
from sqlite_adapter import SQLite3Adapter

class SQLiteMetadataReader(metaclass=SingletonMeta):
  """Metadata READ interface for SQLITE database."""

  def getAllComposers(self, listed_only=True) -> list:
    """Get all composer metadata from DB"""
    if listed_only:
      rows = SQLite3Adapter().selectRows("SELECT * FROM Composers WHERE listed != 0 ORDER BY code;")
    else:
      rows = SQLite3Adapter().selectRows("SELECT * FROM Composers ORDER BY code;")
    if not SQLite3Adapter().getSqlSelectError(rows):
      return rows
    else:
      return []


  def getPartialComposers(self, items_per_page: int, page_number: int, listed_only=True) -> list:
    """Get metadata of partial (paginated) composers from DB."""
    if listed_only:
      rows = SQLite3Adapter().selectRows( \
        f"SELECT * FROM Composers WHERE listed != 0 ORDER BY code \
          LIMIT {items_per_page} OFFSET {(page_number - 1) * items_per_page} ;")
    else:
      rows = SQLite3Adapter().selectRows( \
        f"SELECT * FROM Composers ORDER BY code \
          LIMIT {items_per_page} OFFSET {(page_number - 1) * items_per_page} ;")
    if not SQLite3Adapter().getSqlSelectError(rows):
      return rows
    else:
      return []


  def getComposer(self, composer_code: str) -> dict:
    """Get composer metadata with composer code."""
    rows = SQLite3Adapter().selectRows(f"SELECT * FROM Composers WHERE code = '{composer_code}';")
    if rows and type(rows[0]) == dict:
      return rows[0]
    return {}


  def getComposerCodeNameDict(self) -> dict:
    """Get a dictionary of composer code and knownas_name for all composers in DB."""
    rows = SQLite3Adapter().selectRows("SELECT code, knownas_name FROM Composers;")
    if not SQLite3Adapter().getSqlSelectError(rows):
      code_name_dict = {composer['code']: composer['knownas_name'] for composer in rows}
      return code_name_dict
    else:
      return {}


  def getAllPieces(self) -> list:
    """Get metadata of all pieces from DB."""
    rows = SQLite3Adapter().selectRows("SELECT * FROM Pieces ORDER BY title;")
    if not SQLite3Adapter().getSqlSelectError(rows):
      return rows
    else:
      return []


  def getPartialPieces(self, items_per_page: int, page_number: int) -> list:
    """Get metadata of partial (paginated) pieces from DB."""
    rows = SQLite3Adapter().selectRows( \
      f"SELECT * FROM Pieces ORDER BY title \
        LIMIT {items_per_page} OFFSET {(page_number-1) * items_per_page} ;")
    if not SQLite3Adapter().getSqlSelectError(rows):
      return rows
    else:
      return []


  def getPiece(self, piece_hash: str) -> dict:
    """Get piece metadata with piece hash."""
    rows = SQLite3Adapter().selectRows(f"SELECT * FROM Pieces WHERE folder_hash = '{piece_hash}';")
    if rows and type(rows[0]) == dict:
      return rows[0]
    return {}


  def searchPiecesBySubstr(self, keyword: str) -> list:
    """Search for pieces by keyword substring."""
    selected_rows = SQLite3Adapter().selectRows(f"SELECT * FROM Piece_search WHERE context LIKE '%{keyword}%' ORDER BY context;")
    if not SQLite3Adapter().getSqlSelectError(selected_rows):
      for row in selected_rows:
        if type(row) == dict and 'folder_hash' in row.keys():
          piece_metadata = SQLite3Adapter().selectRows(f"SELECT * FROM Pieces WHERE folder_hash = '{row['folder_hash']}';")
          if not SQLite3Adapter().getSqlSelectError():
            row['title'] = piece_metadata[0].get('title', '?!!.')
            row['arranged'] = piece_metadata[0].get('arranged', 0)
      return selected_rows
    else:
      return []


  def getComposerPieces(self, composer_code: str) -> list:
    """Get pieces by a specific composer."""
    rows = SQLite3Adapter().selectRows( \
      f"SELECT * FROM Pieces WHERE composer_code = '{composer_code}' \
        OR arranger_code = '{composer_code}' ORDER BY title;")
    if not SQLite3Adapter().getSqlSelectError(rows):
      return rows
    else:
      return []


  def getComposerPartialPieces(self, composer_code: str, items_per_page: int, page_number: int) -> list:
    """Get pieces by a specific composer with pagination."""
    rows = SQLite3Adapter().selectRows( \
      f"SELECT * FROM Pieces WHERE composer_code = '{composer_code}' \
        OR arranger_code = '{composer_code}' ORDER BY title          \
        LIMIT {items_per_page} OFFSET {(page_number-1) * items_per_page} ;")
    if not SQLite3Adapter().getSqlSelectError(rows):
      return rows
    else:
      return []


  def getAllCollections(self) -> list:
    """Get metadata of all collections from DB."""
    rows = SQLite3Adapter().selectRows("SELECT * FROM Collections ORDER BY title;")
    if not SQLite3Adapter().getSqlSelectError(rows):
      return rows
    else:
      return []


  def getPartialCollections(self, items_per_page: int, page_number: int) -> list:
    """Get metadata of partial (paginated) collections from DB."""
    rows = SQLite3Adapter().selectRows( \
      f"SELECT * FROM Collections ORDER BY title \
        LIMIT {items_per_page} OFFSET {(page_number-1) * items_per_page} ;")
    if not SQLite3Adapter().getSqlSelectError(rows):
      return rows
    else:
      return []


  def getCollection(self, collection_code: str) -> dict:
    """Get collection metadata with collection code."""
    rows = SQLite3Adapter().selectRows(f"SELECT * FROM Collections WHERE code = '{collection_code}';")
    if rows and type(rows[0]) == dict:
      return rows[0]
    return {}


  def getCollectionPieces(self, collection_code: str) -> list:
    """Get pieces in a specific collection."""
    rows = SQLite3Adapter().selectRows( \
      f"SELECT * FROM Pieces WHERE collection_code LIKE '%{collection_code}%' ORDER BY title;")
    if not SQLite3Adapter().getSqlSelectError(rows):
      return rows
    else:
      return []


  def getComposerCollections(self, composer_code: str) -> list:
    """Get collections related to a specific composer."""
    rows = SQLite3Adapter().selectRows( \
      f"SELECT * FROM Collections WHERE composer_code = '{composer_code}' ORDER BY title;")
    if not SQLite3Adapter().getSqlSelectError(rows):
      return rows
    else:
      return []


  def countComposers(self, listed_only=True) -> int:
    """Get total number of composers in DB."""
    if listed_only:
      count = SQLite3Adapter().countRows("SELECT COUNT(*) FROM Composers WHERE listed != 0;")
    else:
      count = SQLite3Adapter().countRows("SELECT COUNT(*) FROM Composers;")
    return count


  def countPieces(self) -> int:
    """Get total number of pieces in DB."""
    count = SQLite3Adapter().countRows("SELECT COUNT(*) FROM Pieces;")
    return count


  def countCollections(self) -> int:
    """Get total number of collections in DB."""
    count = SQLite3Adapter().countRows("SELECT COUNT(*) FROM Collections;")
    return count


  def countComposerPieces(self, composer_code: str) -> int:
    """Get number of pieces by a specific composer."""
    count = SQLite3Adapter().countRows(f"SELECT COUNT(*) FROM Pieces WHERE composer_code = '{composer_code}';")
    return count


  def countComposerCollections(self, composer_code: str) -> int:
    """Get number of collections related to a specific composer."""
    count = SQLite3Adapter().countRows( \
      f"SELECT COUNT(*) FROM Collections WHERE composer_code = '{composer_code}';")
    if count < 0:
      return 0
    return count


  def composerExists(self, composer_code: str) -> bool:
    """Check if a composer with the given code exists in DB."""
    count = SQLite3Adapter().countRows( \
      f"SELECT COUNT(*) FROM Composers WHERE code = '{composer_code}';")
    return count > 0


  def pieceExists(self, piece_hash: str) -> bool:
    """Check if a piece with the given hash exists in DB."""
    count = SQLite3Adapter().countRows( \
      f"SELECT COUNT(*) FROM Pieces WHERE folder_hash = '{piece_hash}';")
    return count > 0


  def collectionExists(self, collection_code: str) -> bool:
    """Check if a collection with the given code exists in DB."""
    count = SQLite3Adapter().countRows( \
      f"SELECT COUNT(*) FROM Collections WHERE code = '{collection_code}';")
    return count > 0


  def composerHasPieces(self, composer_code: str) -> bool:
    """Check if a composer has pieces in DB."""
    count = SQLite3Adapter().countRows( \
      f"SELECT COUNT(*) FROM Pieces WHERE composer_code = '{composer_code}';")
    return count > 0

  def collectionHasPiece(self, collection_code: str, piece_hash: str) -> bool:
    """Check if a piece is in collection in DB."""
    count = SQLite3Adapter().countRows( \
      f"SELECT COUNT(*) FROM Collections WHERE \
        code = '{collection_code}' AND list_pieces LIKE '%{piece_hash}%';")
    return count > 0


###############################################################################


class SQLiteMetadataWriter(metaclass=SingletonMeta):
  """Metadata WRITE interface for SQLITE database."""

  def __generateComposerCode(self, knownas_name: str) -> str:
    code = ""
    clean_name = toAscii(knownas_name)
    clean_name = clean_name.lower() \
      .replace('-',' '  ).replace('.',' ').replace('van ','') \
      .replace('de ','' ).replace('da ','').replace('di ','') \
      .replace('dos ','').replace('von ','').replace("l’","").replace("d’","")
    namelist = clean_name.split(' ')
    code += namelist.pop()
    firstletter = [x[0] for x in namelist]
    code += '_' + '_'.join(firstletter)
    return code


  def __generatePieceHash(self, piece_information: str) -> str:
    sha1hash = hashlib.sha1()
    sha1hash.update(piece_information.encode('utf-8'))
    piece_hash = sha1hash.hexdigest()
    return piece_hash


  def __generateCollectionCode(self, collection_information: str) -> str:
    md5hash = hashlib.md5()
    md5hash.update(collection_information.encode('utf-8'))
    code = md5hash.hexdigest()[0:10]
    return code


  def __checkComposerExist(self, composer_code: str) -> bool:
    count = SQLite3Adapter().countRows( \
      f"SELECT COUNT(*) FROM Composers WHERE code = '{composer_code}';")
    return count > 0


  def __checkPieceExists(self, piece_hash: str) -> bool:
    count = SQLite3Adapter().countRows( \
      f"SELECT COUNT(*) FROM Pieces WHERE folder_hash = '{piece_hash}';")
    return count > 0


  def __checkCollectionExists(self, collection_code: str) -> bool:
    count = SQLite3Adapter().countRows( \
      f"SELECT COUNT(*) FROM Collections WHERE code = '{collection_code}';")
    return count > 0

  def __checkPieceInCollection(self, piece_hash: str, collection_code: str) -> bool:
    count = SQLite3Adapter().countRows( \
      f"SELECT COUNT(*) FROM Collections WHERE code = '{collection_code}' \
        AND list_pieces LIKE '%{piece_hash}%';")
    return count > 0


  def createComposer(self, firstname: str, lastname: str, knownas_name: str, bornyear=-1, diedyear=-1) -> str:
    """Insert composer metadata into DB."""
    code = self.__generateComposerCode(knownas_name)
    if self.__checkComposerExist(code):
      return f"Composer with code {code} already exists in DB."
    err = SQLite3Adapter().updateRows( \
      f"INSERT INTO Composers (code, firstname, lastname, knownas_name, bornyear, diedyear) \
        VALUES ('{code}', '{firstname}', '{lastname}', '{knownas_name}', {bornyear}, {diedyear});")
    if err:
      return err
    return code


  def hideComposer(self, composer_code: str) -> str:
    """Hide composer in DB by setting a flag. Hidden composer will not be returned in getAllComposers()."""
    if not self.__checkComposerExist(composer_code):
      return f"Composer '{composer_code}' does not exist in DB."
    err = SQLite3Adapter().updateRows(f"UPDATE Composers SET listed = 0 WHERE code = '{composer_code}';")
    return err


  def unhideComposer(self, composer_code: str) -> str:
    """Unhide composer in DB by setting the 'listed' flag."""
    if not self.__checkComposerExist(composer_code):
      return f"Composer '{composer_code}' does not exist in DB."
    err = SQLite3Adapter().updateRows(f"UPDATE Composers SET listed = 1 WHERE code = '{composer_code}';")
    return err


  def createPiece(self, composer_code: str, title: str, subtitle="", subsubtitle="", \
                  opus="", dedicated="", arranger_code="", arranger_name="", \
                  collection_code="", year="?", instruments="", comment="") -> str:
    """Insert piece metadata into DB."""
    is_arranged = 0
    if arranger_code or arranger_name:
      is_arranged = 1
    all_information = [composer_code, title, subtitle, subsubtitle, opus, dedicated, str(is_arranged), \
                       arranger_code, arranger_name, collection_code, year, instruments, comment]
    piece_hash = self.__generatePieceHash('-'.join(all_information))
    if self.__checkPieceExists(piece_hash):
      return f"Piece '{piece_hash}' already exists in DB."
    
    err = ""
    if self.__checkComposerExist(composer_code):
      err = SQLite3Adapter().updateRows( \
        f"INSERT INTO Pieces \
        (folder_hash, composer_code, title, subtitle, subsubtitle, opus, dedicated_to, \
         arranged, arranger_code, arranger_name, collection_code, composed_year, instruments, comment) \
        VALUES ('{piece_hash}', '{composer_code}', '{title}', '{subtitle}', '{subsubtitle}', '{opus}', \
                '{dedicated}', {is_arranged}, '{arranger_code}', '{arranger_name}', \
                '{collection_code}', '{year}', '{instruments}', '{comment}'); ")
      # Get composer information and write to DB 'Piece_Search' table
      selected_rows = SQLite3Adapter().selectRows(f"SELECT * FROM Composers WHERE code = '{composer_code}';")
      err += SQLite3Adapter().getSqlSelectError(selected_rows)
      if not err:
        composer = selected_rows[0]
        composerfullname = composer['firstname'] + " " + composer['lastname']
        author = composerfullname + arranger_code + " " + arranger_name
        context = f"{title} {subtitle} {subsubtitle} {dedicated} \
                    {composerfullname} {arranger_name} {arranger_code}"
        context = toAscii(context)
        author = toAscii(author)
        err += SQLite3Adapter().updateRows( \
          f"INSERT INTO Piece_Search \
            (context, author, composer_code, opus, composed_year, instruments, folder_hash) \
            VALUES ('{context}', '{author}', '{composer_code}', '{opus}', \
                    '{year}', '{toAscii(instruments)}', '{piece_hash}') ;")
    else:
      err = f"Composer '{composer_code}' does not exist in DB. Cannot create piece."

    if err:
      return err
    return piece_hash


  def createCollection(self, title: str, subtitle="", subsubtitle="", editor="", \
                       composer_code="", opus="", volume="", instruments="", description="") -> str:
    """Insert collection metadata into DB."""
    information = [title, subtitle, subsubtitle, editor, composer_code, opus, volume]
    collection_code = self.__generateCollectionCode('-'.join(information))
    if self.__checkCollectionExists(collection_code):
      return f"Collection '{collection_code}' already exists in DB."
    err = SQLite3Adapter().updateRows( \
      f"INSERT INTO Collections \
      (code,title,subtitle,subsubtitle,editor,composer_code,opus,volume,instruments,description_text) \
        VALUES ('{collection_code}', '{title}', '{subtitle}', '{subsubtitle}', '{editor}', \
                '{composer_code}', '{opus}', '{volume}', '{instruments}', '{description}');")
    if err:
      return err
    return collection_code


  def updateComposer(self, composer_code: str, firstname="", lastname="", \
                     knownas_name="", bornyear="", diedyear="") -> str:
    """Update composer metadata in DB."""
    if not self.__checkComposerExist(composer_code):
      return f"Composer with code {composer_code} does not exist in DB."
    err = SQLite3Adapter().updateRows( \
      f"UPDATE Composers SET \
          firstname    = COALESCE('{firstname}', firstname),       \
          lastname     = COALESCE('{lastname}', lastname),         \
          knownas_name = COALESCE('{knownas_name}', knownas_name), \
          bornyear     = COALESCE({bornyear}, bornyear),           \
          diedyear     = COALESCE({diedyear}, diedyear)            \
        WHERE code = '{composer_code}';")
    return err


  def updatePiece(self, piece_hash: str, title="", subtitle="", subsubtitle="", opus="", \
                  dedicated="", collection_code="", year="", instruments="", comment="") -> str:
    """Update piece metadata in DB."""
    if not self.__checkPieceExists(piece_hash):
      return f"Piece '{piece_hash}' does not exist in DB."
    # update Piece_Search table
    try:
      rows = SQLite3Adapter().selectRows(f"SELECT composer_code FROM Pieces WHERE folder_hash = '{piece_hash}';")
      composer_code = "x"
      composer = {}
      if not SQLite3Adapter().getSqlSelectError(rows):
        composer_code = rows[0]['composer_code']
        rows_ = SQLite3Adapter().selectRows(f"SELECT * FROM Composers WHERE code = '{composer_code}';")
        if not SQLite3Adapter().getSqlSelectError(rows_):
          composer = rows_[0]
      composerfullname = composer['firstname'] + " " + composer['lastname']
      author = composerfullname + " " + collection_code
      context = f"{title} {subtitle} {subsubtitle} {dedicated} {composerfullname} {collection_code}"
      err = SQLite3Adapter().updateRows( \
        f"UPDATE Piece_Search SET                                           \
            context       = COALESCE('{toAscii(context)}', context),        \
            author        = COALESCE('{toAscii(author)}', author),          \
            opus          = COALESCE('{opus}', opus),                       \
            composed_year = COALESCE('{year}', composed_year),              \
            instruments   = COALESCE('{toAscii(instruments)}', instruments) \
          WHERE folder_hash = '{piece_hash}';")
    except IndexError:
      return f"Piece '{piece_hash}' does not have a valid composer code in DB. Cannot update piece."
    #
    # Update Pieces table
    err += SQLite3Adapter().updateRows( \
      f"UPDATE Pieces SET                                                     \
          title             = COALESCE('{title}', title),                     \
          subtitle          = COALESCE('{subtitle}', subtitle),               \
          subsubtitle       = COALESCE('{subsubtitle}', subsubtitle),         \
          opus              = COALESCE('{opus}', opus),                       \
          dedicated_to      = COALESCE('{dedicated}', dedicated_to),          \
          collection_code   = COALESCE('{collection_code}', collection_code), \
          composed_year     = COALESCE('{year}', composed_year),              \
          instruments       = COALESCE('{instruments}', instruments),         \
          comment           = COALESCE('{comment}', comment)                  \
        WHERE folder_hash = '{piece_hash}';")
    return err


  def updateCollection(self, collection_code: str, title="", subtitle="", subsubtitle="", \
                       editor="", opus="", volume="", instruments="", description="") -> str:
    """Update collection metadata in DB."""
    if not self.__checkCollectionExists(collection_code):
      return f"Collection '{collection_code}' does not exist in DB."
    err = SQLite3Adapter().updateRows( \
      f"UPDATE Collections SET \
          title            = COALESCE('{title}', title),                 \
          subtitle         = COALESCE('{subtitle}', subtitle),           \
          subsubtitle      = COALESCE('{subsubtitle}', subsubtitle),     \
          editor           = COALESCE('{editor}', editor),               \
          opus             = COALESCE('{opus}', opus),                   \
          volume           = COALESCE('{volume}', volume),               \
          instruments      = COALESCE('{instruments}', instruments),     \
          description_text = COALESCE('{description}', description_text) \
        WHERE code = '{collection_code}';")
    return err


  def deleteComposer(self, composer_code: str, deleted_associated_works=False) -> str:
    """Delete composer from DB. This will also delete all pieces and collections related to the composer."""
    if not self.__checkComposerExist(composer_code):
      return f"Composer '{composer_code}' does not exist in DB."    
    err = SQLite3Adapter().updateRows(f"DELETE FROM Composers WHERE code = '{composer_code}';")
    if deleted_associated_works:
      err += SQLite3Adapter().updateRows(f"DELETE FROM Pieces WHERE composer_code = '{composer_code}';")
      err += SQLite3Adapter().updateRows(f"DELETE FROM Piece_Search WHERE composer_code = '{composer_code}';")
      err += SQLite3Adapter().updateRows(f"DELETE FROM Collections WHERE composer_code = '{composer_code}';")
    return err


  def deletePiece(self, piece_hash: str) -> str:
    """Delete piece from DB."""
    if not self.__checkPieceExists(piece_hash):
      return f"Piece '{piece_hash}' does not exist in DB."
    err =  SQLite3Adapter().updateRows(f"DELETE FROM Pieces WHERE folder_hash = '{piece_hash}';")
    err += SQLite3Adapter().updateRows(f"DELETE FROM Piece_Search WHERE folder_hash = '{piece_hash}';")
    # Delete piece_hash from collections
    rows = SQLite3Adapter().selectRows(f"SELECT * FROM Collections WHERE list_pieces LIKE '%{piece_hash}%';")
    if rows and not SQLite3Adapter().getSqlSelectError(rows):
      for collection in rows:
        if type(collection) == dict:
          collection_code = collection.get('code', '?')
          err += self.rmPieceFromCollection(piece_hash, collection_code)
    return err


  def deleteCollection(self, collection_code: str) -> str:
    """Delete collection from DB."""
    if not self.__checkCollectionExists(collection_code):
      return f"Collection '{collection_code}' does not exist in DB."    
    err = SQLite3Adapter().updateRows(f"DELETE FROM Collections WHERE code = '{collection_code}';")
    return err


  def addPieceToCollection(self, piece_hash: str, collection_code: str) -> str:
    """Add a piece to a collection."""
    if not self.__checkPieceExists(piece_hash):
      return f"Piece '{piece_hash}' does not exist in DB."
    if not self.__checkCollectionExists(collection_code):
      return f"Collection '{collection_code}' does not exist in DB."
    #
    err = ""
    # Nothing to do if piece already in collection
    if not self.__checkPieceInCollection(piece_hash, collection_code):
    # Append piece_hash to collection's list_piece
      current_pieces = ""
      rows = SQLite3Adapter().selectRows( \
        f"SELECT * FROM Collections WHERE code = '{collection_code}';")
      if rows and not SQLite3Adapter().getSqlSelectError(rows):
        current_pieces = rows[0].get('list_pieces', '')
      new_listpieces = ','.join([p for p in current_pieces.split(',') if p != piece_hash])
      new_listpieces += f",{piece_hash}"
      # Update in Collection table
      err = SQLite3Adapter().updateRows( \
          f"UPDATE Collections SET list_pieces = '{new_listpieces}' WHERE code = '{collection_code}';")
    return err


  def rmPieceFromCollection(self, piece_hash: str, collection_code: str) -> str:
    """Remove a piece from a collection."""
    if not self.__checkPieceExists(piece_hash):
      return f"Piece '{piece_hash}' does not exist in DB."
    if not self.__checkCollectionExists(collection_code):
      return f"Collection '{collection_code}' does not exist in DB."
    #
    err = ""
    # Nothing to do if piece not in collection
    if self.__checkPieceInCollection(piece_hash, collection_code):
      # Remove piece from collection table's list_pieces
      current_pieces = ""
      rows = SQLite3Adapter().selectRows(f"SELECT * FROM Collections WHERE code = '{collection_code}';")
      if rows and not SQLite3Adapter().getSqlSelectError(rows):
        current_pieces = rows[0].get('list_pieces', '')
      new_listpieces = ','.join([p for p in current_pieces.split(',') if p != piece_hash])
      # Update in Collection table
      err = SQLite3Adapter().updateRows( \
        f"UPDATE Collections SET list_pieces = '{new_listpieces}' WHERE code = '{collection_code}';")
    return err


  def addComposerImslpLink(self, composer_code: str, imslp_link: str) -> str:
    """Add IMSLP link to a composer in DB."""
    if not self.__checkComposerExist(composer_code):
      return f"Composer '{composer_code}' does not exist in DB."
    err = SQLite3Adapter().updateRows( \
      f"UPDATE Composers SET imslp_url = '{imslp_link}' WHERE code = '{composer_code}';")
    return err


  def addComposerWikiLink(self, composer_code: str, wiki_link: str) -> str:
    """Add Wiki link to a composer in DB."""
    if not self.__checkComposerExist(composer_code):
      return f"Composer '{composer_code}' does not exist in DB."
    err = SQLite3Adapter().updateRows( \
      f"UPDATE Composers SET wikipedia_url = '{wiki_link}' WHERE code = '{composer_code}';")
    return err
