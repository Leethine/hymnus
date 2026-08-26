from unidecode import unidecode
from datetime import datetime
import os, time

''' Singleton meta class. '''
class SingletonMeta(type):
  _instances = {}

  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      instance = super().__call__(*args, **kwargs)
      cls._instances[cls] = instance
    return cls._instances[cls]
  

def toAscii(inputstr) -> str:
  return unidecode(inputstr)


def createHtmlAlertBox(message: str, level="Warning") -> str:
  HTML = "<!DOCTYPE html><html><body>"
  HTML += f"<h2>{level}</h2><script>\n"
  HTML += f"alert('{message}');"
  HTML += "history.back()"
  HTML += "</script></body></html>"
  return HTML


def logUserActivity(username: str, action: str) -> None:
  with open("user_activities.log", "a+") as f:
    f.write("[" + str(datetime.now()) + "]\n")
    f.write(username)
    f.write("\n")
    f.write(action)
    f.write("\n================\n")


def verifyFormKeys(form, required_keys: list) -> bool:
  for key in required_keys:
    if key not in form.keys():
      return False
  return True
