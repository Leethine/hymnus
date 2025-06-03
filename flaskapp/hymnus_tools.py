from unidecode import unidecode
from datetime import datetime

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

def logUserActivity(username: str, action: str):
  with open("user_activities.log", "a+") as f:
    f.write("[" + str(datetime.now()) + "]\n")
    f.write(username)
    f.write("\n")
    f.write(action)
    f.write("\n================\n")
