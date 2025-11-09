from unidecode import unidecode
from datetime import datetime
from flask import request
import os

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

def saveMessage(req_form):
  msg = {}
  msg['time']  = str(datetime.now()).replace(':','-').replace(' ','__')
  msg['mail']  = ""
  msg['phone'] = ""
  msg['body']  = ""
  if 'your-email' in req_form:
    msg['mail'] = req_form['your-email']
  if 'your-email' in req_form:
    msg['phone'] = req_form['your-phone']
  if 'mail-subject' in req_form:
    msg['body'] = req_form['mail-subject']
  if msg['mail']  == "" and msg['phone']  == "":
    return createAlertBox("Must provide phone number or email address!")
  if msg['body']  == "":
    return createAlertBox("Message must not be empty!")
  with open(os.environ['HOME'] + f"/message/{msg['time']}", "w+") as f:
    f.write(msg['mail'])
    f.write("\n")
    f.write(msg['phone'])
    f.write("\n")
    f.write(msg['body'])
    f.write("\n")
  return '<h3>Message saved, thank you for messaging!</h3> \
          <h3>Return to <a href="/index">home page</a></h3>'
