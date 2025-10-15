from database import Database
from unidecode import unidecode

class Metadata():
  """This class handles the metadata of composers, collections and pieces."""
  def __init__(self):
    pass
  

  def __assertOneRowData(self, rows: list, keylist: list):
    assert len(rows) == 1
    assert type(rows[0]) is dict
    for key in keylist:
      assert key in rows[0].keys()


  def getAbbrName(self, name: str) -> str:
    name_clean = name.replace('-', ' ').replace('von ', '').replace('van ', '') \
    .replace('de ', '').replace('da ', '').replace('di ', '').replace('dos ', '') \
    .replace('the ', '').replace('le ', '').replace('la ', '').replace('los ', '') \
    .replace(' I', '').replace(' II', '').replace(' III', '').replace(' Jr.', '')

    namelist = name_clean.split(' ')
    if len(namelist) > 1:
      first = ' '.join([x[0] for x in namelist[:-1]])
      last = namelist[-1]
      return f"{first} {last}"
    else:
      return name


  def composerExists(self, composer_code: str) -> bool:
    count = Database().countRows(f"SELECT COUNT(*) FROM Composers WHERE code = '{composer_code}';")
    if count > 0:
      return True
    else:
      return False


  def getComposerMetadata(self, composer_code: str) -> dict:
    composer = {"code": "N/A", "ShortName": "N/A",
                "AbbrName": "N/A", "LongName": "N/A", "Year": "N/A"}
    if composer_code and self.composerExists(composer_code):
      rows = Database().selectAllRows(f"SELECT * FROM Composers WHERE code = '{composer_code}';")
      self.__assertOneRowData(rows, ["firstname", "lastname", "knownas_name",
                                     "code", "bornyear", "diedyear"])
      composer["code"] = composer_code
      composer["ShortName"] = rows[0]["knownas_name"]
      composer["AbbrName"] = self.getAbbrName(composer["ShortName"])
      composer["LongName"] = rows[0]["firstname"] + " " + rows[0]["lastname"]
      composer["Year"] = str(rows[0]["bornyear"]) + " - " + str(rows[0]["diedyear"])
    return composer


  def getComposerCodeNameList(self) -> list:
    QUERY = """SELECT code, knownas_name AS name FROM Composers
               WHERE code != 'zzz_unknown' ORDER BY code ASC;"""
    composerlist = Database().selectAllRows(QUERY)
    for c in composerlist:
      c["code"] = unidecode(c["code"])
      # Reverse full name, J S Bach ==> Bach, J S
      name = unidecode(c["name"])
      c["name"] = name.split(' ')[-1] + ", " + ' '.join(name.split(' ')[:-1])
    return composerlist


  def composerHasWorks(self, composer_code: str) -> bool:
    count = Database().countRows(f"SELECT COUNT(*) FROM Pieces WHERE composer_code = '{composer_code}';")
    if count > 0:
      return True
    return False


  def pieceExists(self, folder_hash: str) -> bool:
    count = Database().countRows(f"SELECT COUNT(*) FROM Pieces WHERE folder_hash = '{folder_hash}';")
    if count > 0:
      return True
    else:
      return False


  def getPieceMetadata(self, folder_hash: str) -> dict:
    keylist = ["composer_code", "arranged", "arranger_code",
               "collection_code", "title", "subtitle",
               "subsubtitle", "dedicated_to", "opus",
               "instruments", "folder_hash", "comment"]
    piece = {}
    for key in keylist:
      piece[key] = "N/A"
    piece["arranged_by"] = "N/A"
    piece["composer"] = "N/A"

    if folder_hash and self.pieceExists(folder_hash):
      rows = Database().selectAllRows(f"SELECT * FROM Pieces WHERE folder_hash = '{folder_hash}';")
      self.__assertOneRowData(rows, keylist)
      for key in rows[0].keys():
        if rows[0][key] and str(rows[0][key]).replace(' ','') != "":
          piece[key] = str(rows[0][key])
      
      if self.composerExists(piece["composer_code"]):
        piece["composer"] = self.getComposerMetadata(piece["composer_code"])["ShortName"]
      if piece["arranged"] == "1" and self.composerExists(piece["arranger_code"]):
        piece["arranged_by"] = self.getComposerMetadata(piece["arranger_code"])["AbbrName"]

    return piece


  def collectionExists(self, collection_code: str) -> bool:
    count = Database().countRows(f"SELECT COUNT(*) FROM Collections WHERE code = '{collection_code}';")
    if count > 0:
      return True
    else:
      return False


  def getCollectionMetadata(self, collection_code: str):
    keylist = ["composer_code", "code", "title",
               "subtitle", "subsubtitle", "opus", "description_text",
               "volume", "instruments", "editor"]
    collection = {}
    for key in keylist:
      collection[key] = "N/A"
    collection["composer"] = "N/A"

    if collection_code and self.collectionExists(collection_code):
      rows = Database().selectAllRows(f"SELECT * FROM Collections WHERE code = '{collection_code}';")
      self.__assertOneRowData(rows, keylist)
      for key in rows[0].keys():
        if rows[0][key] and str(rows[0][key]).replace(' ','') != "":
          collection[key] = str(rows[0][key])

      if self.composerExists(collection["composer_code"]):
        collection["composer"] = self.getComposerMetadata(collection["composer_code"])["ShortName"]
    
    return collection


  def getCollectionPieces(self, collection_code: str):
    QUERY = f"SELECT * FROM Pieces WHERE collection_code LIKE '%{collection_code}%' ORDER by Opus;"
    
    pieces = []
    if self.collectionExists(collection_code):
      pieces = Database().selectAllRows(QUERY)

    return pieces


  def collectionHasPieces(self, collection_code: str):
    QUERY = f"SELECT COUNT(*) FROM Pieces WHERE collection_code = '{collection_code}';"
    if Database().countRows(QUERY) > 0:
      return True
    return False


# Test
if __name__ == '__main__':
  m = Metadata()
  print(m.getComposerMetadata('bach_j_s'))
  print(m.getCollectionMetadata('974739fce84e0f22a2b0fbc37b6b54f6'))
  print(m.getPieceMetadata('78a01866520f6c9075badce6b691bb75cfca7094'))
