from unidecode import unidecode

def normalizeStr(inputstr=""):
  return unidecode(inputstr)

def toAscii(inputstr=""):
  return unidecode(inputstr)

def createAlertBox(message: str, level="Warning") -> str:
  HTML = "<!DOCTYPE html><html><body>"
  HTML += "<h2>{level}</h2><script>\n"
  HTML += 'alert("' + message + '");'
  HTML += 'history.back()'
  HTML += "</script></body></html>"
  return HTML