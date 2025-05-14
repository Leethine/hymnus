import os, hashlib

HYMNUS_USERS=""

if 'HYMNUS_USERS' in os.environ.keys():
  HYMNUS_USERS = os.environ['HYMNUS_USERS']

def validateUserPassword(user: str, password: str):
  userfile = f'{HYMNUS_USERS}/{user}'
  if os.path.exists(userfile):
    with open(userfile, 'r') as f:
      m = hashlib.sha1()
      m.update(password.encode())
      if m.hexdigest() == f.read():
        return True
  return False
