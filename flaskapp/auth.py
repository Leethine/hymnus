import os, hashlib

class AuthWeak():
  def __init__(self):
    self.HYMNUS_USERS = ""
    if 'HYMNUS_USERS' in os.environ.keys():
      self.HYMNUS_USERS = os.environ['HYMNUS_USERS']

  def validateUserPassword(self, user: str, password: str):
    userfile = f'{self.HYMNUS_USERS}/{user}'
    if os.path.exists(userfile):
      with open(userfile, 'r') as f:
        m = hashlib.sha1()
        m.update(password.encode())
        if m.hexdigest() == f.read().replace("\n", ""):
          return True
    return False
