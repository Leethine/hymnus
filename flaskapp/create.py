from database import Database

class Composer:
  def __init__(self, code="", firstname="",
               lastname="", knownas="",
               bornyear=-1, diedyear=-1,
               wikipedia_url="",
               imslp_url=""):
    pass

class Piece:
  def __init__(self, composer="", arranger="", collection="",
               title="", subtitle="", subsubtitle="",
               dedicated_to="", opus="", year="",
               instruments="", comment="", folderhash=""):
    pass

class Collection:
  def __init__(self, code="", composer="",
               title="", subtitle="", subsubtitle="",
               description="", opus="", volume="",
               instruments="", editor=""):
    pass
