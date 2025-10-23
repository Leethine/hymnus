from flask import render_template, request
from database import Database
from metadata import Metadata
import re

class NewComposerCreator:
  def __init__(self,
               firstname="", lastname="", knownas="",
               bornyear=-1, diedyear=-1,
               code = "",
               wikipedia_url="", imslp_url=""):
    self.__code = code
    self.__firstname = firstname
    self.__lastname  = lastname
    self.__knownas   = knownas
    self.__bornyear  = bornyear
    self.__diedyear  = diedyear
    self.__listed    = 0
    self.__wiki_url  = wikipedia_url
    self.__imslp_url = imslp_url
    self.__SQL_INSERTION = ""
  
  def __checkHtmlForm(self, req_form):
    err = ""
    formkeys = ['firstname', 'lastname', 'knownas', 'bornyear', 'diedyear']
    for key in formkeys:
      if key not in req_form:
        err += f"Cannot find keyword '{key}'\n"      
    return err
  
  def __setValueFromHtmlForm(self, req_form):
    self.__firstname = req_form['firstname']
    self.__lastname  = req_form['lastname']
    self.__knownas   = req_form['knownas']
    self.__bornyear  = req_form['bornyear']
    self.__diedyear  = req_form['diedyear']
    if 'hide-composer' in req_form:
      self.__listed = 0
    else:
      self.__listed = 1
  
  def __formatInput(self):
    self.__firstname = re.sub(' +', ' ', self.__firstname)
    self.__firstname = re.sub('\s+-', '-', self.__firstname)
    self.__firstname = re.sub('-\s+', '-', self.__firstname)
    self.__firstname = self.__firstname.replace("'","’")
    
    self.__lastname  = re.sub(' +', ' ', self.__lastname)
    self.__lastname  = re.sub('\s+-', '-', self.__lastname)
    self.__lastname  = re.sub('-\s+', '-', self.__lastname)
    self.__lastname = self.__lastname.replace("'","’")
    
    self.__knownas   = re.sub(' +', ' ', self.__knownas)
    self.__knownas = re.sub('\s+-', '-', self.__knownas)
    self.__knownas = re.sub('-\s+', '-', self.__knownas)
    self.__knownas = self.__knownas.replace("'","’")

    self.__firstname = self.__firstname.title()
    self.__lastname  = self.__lastname.title()
    self.__knownas   = self.__knownas.title()
    
  def __generateCode(self):
    code = ""
    if self.__code == "":
      clean_name = self.__knownas.lower() \
        .replace('-',' ').replace('.',' ').replace('van ','') \
        .replace('de ','').replace('da ','') \
        .replace('di ','').replace('dos ','') \
        .replace('von ','').replace("l’","") \
        .replace(' ii','').replace("d’","") \
        .replace(' iii','').replace(' jr','')
      namelist = clean_name.split(' ')
      code += namelist.pop()
      firstletter = [x[0] for x in namelist]
      code += '_' + '_'.join(firstletter)
    self.__code = code

  def __checkExist(self):
    meta = Metadata()
    if meta.composerExists(self.__code) or \
       meta.composerKnownAsNameExists(self.__knownas):
      return True
    return False

  def __getErrorBeforeInsert(self):
    if not self.__code:
      return "<h1>Code must not be empty</h1>"
    if not self.__lastname:
      return "<h1>Last Name must not be empty</h1>"
    if not self.__knownas:
      return "<h1>Known-as Name (Full Name) must be empty</h1>"
    if self.__checkExist():
      return f"<h1>Composer \"{self.__knownas}\" ({self.__code}) already exist</h1>"
    return ""
  
  def __insertComposer(self):
    self.__SQL_INSERTION = "INSERT INTO Composers " \
      + "(code, firstname, lastname, knownas_name, bornyear, diedyear, listed) " \
      + f"VALUES('{self.__code}','{self.__firstname}','{self.__lastname}', \
         '{self.__knownas}','{self.__bornyear}','{self.__diedyear}', {self.__listed});"
    
    err = Database().executeInsertion(SQL_STATEMENT=self.__SQL_INSERTION)
    return err
  
  def getCreationPage(self):
    return render_template("new_composer.html")
  
  def submitHtmlForm(self, req_form) -> str:
    err = ""
    # Check HTLK form integrity
    err = self.__checkHtmlForm(req_form)
    if err:
      return err
    
    self.__setValueFromHtmlForm(req_form)
    self.__generateCode()
    
    # Check HTML form input values
    err = self.__getErrorBeforeInsert()
    if err:
      return err
    
    count_before = Database().countRows("SELECT COUNT(*) FROM Composers")
    err = self.__insertComposer()
    if err:
      return err
    
    # Verify the insertion
    count_after = Database().countRows("SELECT COUNT(*) FROM Composers")
    if count_after - count_before == 1:
      return render_template("creation_ended.html", status="Created",
              head1="Created composer:",\
              head2=f"<a href=\"/browse/works-by/{self.__code}\">{self.__knownas}</a>")
    else:
      return render_template("creation_ended.html", status="Warning",
                              head1="SQL insertion done, but verification failed.",
                              head2=self.__SQL_INSERTION)


class NewPiece:
  def __init__(self, composer="", arranger="", collection="",
               title="", subtitle="", subsubtitle="",
               dedicated_to="", opus="", year="",
               instruments="", comment="", folderhash=""):
    pass
  
  def checkExist(self):
    pass


class NewCollection:
  def __init__(self, code="", composer="",
               title="", subtitle="", subsubtitle="",
               description="", opus="", volume="",
               instruments="", editor=""):
    pass
  
  def checkExist(self):
    pass