import os, hashlib
from utilities import SingletonMeta
from utilities import createHtmlAlertBox, verifyFormKeys
from config import USER_PASSWORDS_PATH

class AuthWeak(metaclass=SingletonMeta):
  """ A simple authentication class that validates user credentials.
      The password files are stored in a specified directory. """
  
  def getUserPwdDir(self):
    if 'HYMNUS_USERS' in os.environ.keys():
      return os.path.abspath(os.environ['HYMNUS_USERS'])
    elif os.path.isdir(USER_PASSWORDS_PATH):
      return os.path.abspath(USER_PASSWORDS_PATH)
    else:
      return "./"


  def validateUserPassword(self, user: str, password: str):
    userfile = f'{self.getUserPwdDir()}/{user}'
    if os.path.exists(userfile):
      with open(userfile, 'r') as f:
        m = hashlib.sha1()
        m.update(password.encode())
        if m.hexdigest() == f.read().replace("\n", ""):
          return True
    return False
  

  def verifyReqFormUserPassword(self, req_form) -> str:
    # validate user name and password
    if verifyFormKeys(req_form, ['user', 'password']):
      if not req_form['user'] or not req_form['password']:
        return createHtmlAlertBox("Please provide a username and password.", "Error")
      elif not AuthWeak().validateUserPassword(req_form['user'], req_form['password']):
        return createHtmlAlertBox("Invalid username or password.", "Error")
    else:
      return createHtmlAlertBox("Usename or password fields missing. Please try again.", "Error")


  def createUser(self, user: str, password: str) -> str:
    userfile = os.path.join(self.getUserPwdDir(), user)
    if os.path.exists(userfile):
      return "Error. User already exists."
    else:
      m = hashlib.sha1()
      m.update(password.encode())
      with open(userfile, 'w') as f:
        f.write(m.hexdigest())
      os.chmod(userfile, 400)
    return "User created successfully."
