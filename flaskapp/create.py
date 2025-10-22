from database import Database
from metadata import Metadata
import re

class Composer:
  def __init__(self,
               firstname, lastname, knownas,
               bornyear=-1, diedyear=-1,
               code = "",
               wikipedia_url="", imslp_url=""):
    self.__code = code
    self.__firstname = firstname
    self.__lastname  = lastname
    self.__knownas   = knownas
    self.__bornyear  = bornyear
    self.__diedyear  = diedyear
    self.__wiki_url  = wikipedia_url
    self.__imslp_url = imslp_url
  
  def formatInput(self):
    self.__firstname = re.sub(' +', ' ', self.__firstname)
    self.__firstname = re.sub('\s+-', '-', self.__firstname)
    self.__firstname = re.sub('-\s+', '-', self.__firstname)
    self.__lastname  = re.sub(' +', ' ', self.__lastname)
    self.__lastname  = re.sub('\s+-', '-', self.__lastname)
    self.__lastname  = re.sub('-\s+', '-', self.__lastname)
    self.__knownas   = re.sub(' +', ' ', self.__knownas)
    self.__knownas = re.sub('\s+-', '-', self.__knownas)
    self.__knownas = re.sub('-\s+', '-', self.__knownas)

    self.__firstname = self.__firstname.title()
    self.__lastname  = self.__lastname.title()
    self.__knownas   = self.__knownas.title()
    
  def generateCode(self):
    code = ""
    if self.__code == "":
      clean_name = self.__knownas.lower() \
        .replace('-',' ').replace('.',' ').replace('van ','') \
        .replace('de ','').replace('da ','') \
        .replace('di ','').replace('dos ','') \
        .replace('von ','').replace("l'","") \
        .replace(' ii','').replace("d'","") \
        .replace(' iii','').replace(' jr','')
      namelist = clean_name.split(' ')
      code += namelist.pop()
      firstletter = [x[0] for x in namelist]
      code += '_' + '_'.join(firstletter)
    self.__code = code

  def checkExist(self):
    meta = Metadata()
    if meta.composerExists(self.__code) or \
       meta.composerKnownAsNameExists(self.__knownas):
      return True
    return False

  def getError(self):
    if not self.__code:
      return "<h1>Code must not be empty</h1>"
    if not self.__lastname:
      return "<h1>Last Name must not be empty</h1>"
    if not self.__knownas:
      return "<h1>Known-as Name (Full Name) must be empty</h1>"
    if self.checkExist():
      return f"<h1>Composer \"{self.__knownas}\" ({self.__code}) already exist</h1>"
    return ""
  
  def insertComposer(self):
    SQL_INSERTION = \
      "INSERT INTO Composers " \
    + "(code, firstname, lastname, knownas_name, bornyear, diedyear) " \
    + f"VALUES('{self.__code}','{self.__firstname}','{self.__lastname}', \
      '{self.__knownas}','{self.__bornyear}','{self.__diedyear}');"
    
    err = Database().executeInsertion(table_name="Composers", SQL_STATEMENT=SQL_INSERTION)
    if err == "":
      return f"Created composer: {self.__knownas}"
    else:
      return err
  
  def getSubmissionPage(self):
    pass

class Piece:
  def __init__(self, composer="", arranger="", collection="",
               title="", subtitle="", subsubtitle="",
               dedicated_to="", opus="", year="",
               instruments="", comment="", folderhash=""):
    pass
  
  def checkExist(self):
    pass

class Collection:
  def __init__(self, code="", composer="",
               title="", subtitle="", subsubtitle="",
               description="", opus="", volume="",
               instruments="", editor=""):
    pass
  
  def checkExist(self):
    pass