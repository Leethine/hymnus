from flask import render_template, request
from database import Database
from metadata import Metadata
import re, hashlib

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
    self.__firstname = re.sub(r'\s+-', '-', self.__firstname)
    self.__firstname = re.sub(r'-\s+', '-', self.__firstname)
    self.__firstname = self.__firstname.replace("'","’")
    
    self.__lastname  = re.sub(' +', ' ', self.__lastname)
    self.__lastname  = re.sub(r'\s+-', '-', self.__lastname)
    self.__lastname  = re.sub(r'-\s+', '-', self.__lastname)
    self.__lastname = self.__lastname.replace("'","’")
    
    self.__knownas   = re.sub(' +', ' ', self.__knownas)
    self.__knownas = re.sub(r'\s+-', '-', self.__knownas)
    self.__knownas = re.sub(r'-\s+', '-', self.__knownas)
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
      return "<h1>Known-as Name (Full Name) must not be empty</h1>"
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


class NewPieceCreator:
  def __init__(self):
    self.__title         = ""
    self.__subtitle      = ""
    self.__subsubtitle   = ""
    self.__dedicated_to  = ""
    self.__opus          = ""
    self.__year          = ""
    self.__instruments   = ""
    self.__comment       = ""
    self.__composer_code = ""
    self.__is_arranged   = 0
    self.__arranger_name = ""
    self.__arranger_code = ""
    self.__collection    = ""
    self.__hash          = ""
    self.__SQL_INSERTION = ""
  
  def __getHtmlFormError(self, req_form: request):
    keylist = ['new-piece-title', 'new-piece-subtitle', 'new-piece-subsubtitle',
               'new-piece-dedicated', 'new-piece-year', 'new-piece-opus',
               'select-composer', 'arranger-name',
               'new-piece-instrument', 'new-piece-comment']
    err = ""
    for key in keylist:
      if key not in req_form:
        err += f"Cannot find keyword: '{key}'\n"
    
    # Then verify the arranger selection
    if 'check-is-arranged-piece' not in req_form and \
       'check-is-not-arranged-piece' not in req_form:
      err += "Cannot find keyword: 'check-is-arranged-piece' \
              and 'check-is-not-arranged-piece'\n"
    if 'check-is-arranged-piece' in req_form and \
       'check-is-not-arranged-piece' in req_form:
      err += "Both keywords in form: 'check-is-arranged-piece' \
              and 'check-is-not-arranged-piece'\n"
    if 'check-is-arranged-piece' in req_form and 'select-arranger' not in req_form:
      err += "Arranger toggled but 'select-arranger' not in the form\n"
    
    return err
  
  def __setValueFromHtmlForm(self, req_form: request):
    self.__title         = req_form['new-piece-title']
    self.__subtitle      = req_form['new-piece-subtitle']
    self.__subsubtitle   = req_form['new-piece-subsubtitle']
    self.__dedicated_to  = req_form['new-piece-dedicated']
    self.__year          = req_form['new-piece-year']
    self.__opus          = req_form['new-piece-opus']
    self.__composer_code = req_form['select-composer']
    self.__arranger_name = req_form['arranger-name']
    self.__instruments   = req_form['new-piece-instrument']
    self.__comment       = req_form['new-piece-comment']
    
    if 'check-is-arranged-piece' in req_form and \
       'check-is-not-arranged-piece' not in req_form:
      self.__is_arranged = 1
      self.__arranger_code = req_form['select-arranger']
    else:
      self.__is_arranged = 0
      self.__arranger_code = ""
      self.__arranger_name = ""
  
  def __checkExist(self):
    meta = Metadata()
    if meta.pieceExists(self.__hash):
      return True
    return False

  def __getErrorBeforeInsert(self):
    meta = Metadata()
    if not self.__hash:
      return "<h1>Folder Hash must not be empty</h1>"
    if not self.__title:
      return "<h1>Title must not be empty</h1>"
    if not self.__composer_code:
      return "<h1>Composer must not be empty</h1>"
    if not meta.composerExists(self.__composer_code):
      return f"<h1>Composer not in database: {self.__composer_code}</h1>"
    if self.__arranger_code and not meta.composerExists(self.__arranger_code):
      return f"<h1>Composer (arranger) not in database: {self.__arranger_code}</h1>"
    if self.__checkExist():
      return f"<h1>Hash Conflict: \"{self.__hash}\"</h1>"
    return ""

  def __generateHash(self):
    keywordlist = [self.__composer_code, self.__title, self.__subsubtitle,\
                   self.__opus, str(self.__is_arranged), self.__collection, \
                   self.__instruments, self.__year]
    sha1hash = hashlib.sha1()
    sha1hash.update('-'.join(keywordlist).encode('utf-8'))
    self.__hash = sha1hash.hexdigest()

  def __insertPiece(self):
    self.__SQL_INSERTION = """
      INSERT INTO Pieces
         (title, subtitle, subsubtitle, opus, composed_year, 
          dedicated_to, composer_code, arranged, arranger_code,
          arranger_name, instruments, comment, folder_hash) 
      """
    self.__SQL_INSERTION += f" VALUES(\
      '{self.__title}','{self.__subtitle}','{self.__subsubtitle}','{self.__opus}','{self.__year}',\
      '{self.__dedicated_to}','{self.__composer_code}',{self.__is_arranged},'{self.__arranger_code}',\
      '{self.__arranger_name}','{self.__instruments}','{self.__comment}','{self.__hash}');"
    
    err = Database().executeInsertion(SQL_STATEMENT=self.__SQL_INSERTION)
    return err
  
  def getCreationPage(self):
    meta = Metadata()
    return render_template("new_piece.html",\
                            composerlist=meta.getComposerCodeNameList())
  
  def submitHtmlForm(self, req_form) -> str:
    err = ""
    # Check HTLK form integrity
    err = self.__getHtmlFormError(req_form)
    if err:
      return err
    self.__setValueFromHtmlForm(req_form)
    self.__generateHash()
    
    # Check input values
    err = self.__getErrorBeforeInsert()
    if err:
      return err
    
    count_before = Database().countRows("SELECT COUNT(*) FROM Pieces")
    err = self.__insertPiece()
    if err:
      return err
    
    # Verify the insertion
    count_after = Database().countRows("SELECT COUNT(*) FROM Pieces")
    if count_after - count_before == 1:
      return render_template("creation_ended.html", status="Created",
              head1="Created new piece:",\
              head2=f"<a href=\"/file/{self.__hash}\">{self.__title}, {self.__opus}</a>")
    else:
      return render_template("creation_ended.html", status="Warning",
                              head1="SQL insertion done, but verification failed.",
                              head2=self.__SQL_INSERTION)


class NewCollectionCreator:
  def __init__(self):
    self.__code          = ""
    self.__composer_code = ""
    self.__title         = ""
    self.__subtitle      = ""
    self.__subsubtitle   = ""
    self.__opus          = ""
    self.__description   = ""
    self.__volume        = ""
    self.__instruments   = ""
    self.__editor        = ""
  
  def __checkExist(self):
    meta = Metadata()
    if meta.collectionExists(self.__code):
      return True
    return False
  
  def __checkHtmlForm(self, req_form: request) -> str:
    keylist = \
      ['new-collection-title', 'new-collection-subtitle', 'new-collection-subsubtitle',\
       'new-collection-editor', 'new-collection-opus', 'new-collection-volume',\
       'new-collection-instrument', 'new-collection-description']
    err = ""
    for key in keylist:
      if key not in req_form:
        err += f"Cannot find Keyword '{key}'\n"
    return err
  
  def __setValueFromHtmlForm(self, req_form: request):
    self.__title = req_form['new-collection-title']
    self.__subtitle = req_form['new-collection-subtitle']
    self.__subsubtitle = req_form['new-collection-subsubtitle']
    self.__editor = req_form['new-collection-editor']
    self.__opus = req_form['new-collection-opus']
    self.__volume = req_form['new-collection-volume']
    self.__instruments = req_form['new-collection-instrument']
    self.__description = req_form['new-collection-description']
    if 'collection-has-composer' in req_form and 'select-composer' in req_form:
      self.__composer_code = req_form['select-composer']
  
  def __getErrorBeforeSubmit(self) -> str:
    meta = Metadata()
    if self.__title == "":
      return "<h1>Title must not be empty</h1>"
    if self.__composer_code != "" and not meta.composerExists(self.__composer_code):
      return "<h1>Chosen composer not exist in DB</h1>"
    if self.__code == "":
      return "<h1>Collection code/hash must not be empty</h1>"
    if meta.collectionExists(self.__code):
      return f"<h1>Hash collision: {self.__code}</h1>"
    return ""
  
  def __generateCode(self):
    seed = f"{self.__composer_code}-{self.__title}-{self.__subtitle}-\
             {self.__subsubtitle}-{self.__opus}-{self.__volume}-\
             {self.__editor}-{self.__instruments}-{self.__description}"
    md5hash = hashlib.md5()
    md5hash.update(seed.encode('utf-8'))
    self.__code = md5hash.hexdigest()[0:10]

  def __insertCollection(self):
    SQL_INSERT = """
    INSERT INTO collections (code,
     title, subtitle, subsubtitle, opus, composer_code,
     editor, volume, instruments, description_text) 
    """
    SQL_INSERT += f" VALUES('{self.__code}',\
      '{self.__title}','{self.__subtitle}','{self.__subsubtitle}',\
      '{self.__opus}','{self.__composer_code}','{self.__editor}',\
      '{self.__volume}','{self.__instruments}','{self.__description}');"
    err = Database().executeInsertion(SQL_INSERT)
    return err
  
  def getSubmitPage(self) -> str:
    meta = Metadata()
    return render_template("new_collection.html",\
                            composerlist=meta.getComposerCodeNameList())
  
  def submitHtmlForm(self, req_form: request) -> str:
    err = ""
    # Check HTLK form integrity
    err = self.__checkHtmlForm(req_form)
    if err:
      return err
    self.__setValueFromHtmlForm(req_form)
    self.__generateCode()
    
    # Check input values
    err = self.__getErrorBeforeSubmit()
    if err:
      return err
    
    count_before = Database().countRows("SELECT COUNT(*) FROM Collections")
    err = self.__insertCollection()
    if err:
      return err
    
    # Verify the insertion
    count_after = Database().countRows("SELECT COUNT(*) FROM Collections")
    if count_after - count_before == 1:
      return render_template("creation_ended.html", status="Created",
              head1="Created new collection:",\
              head2=f"<a href=\"/collection-at/{self.__code}\">{self.__title}, {self.__opus}</a>")
    else:
      return render_template("creation_ended.html", status="Warning",
                              head1="SQL insertion done, but verification failed.",
                              head2=self.__SQL_INSERTION)
