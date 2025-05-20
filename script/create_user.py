#!/usr/bin/python3

import os, hashlib
from getpass import getpass

if __name__ == '__main__':
  if 'HYMNUS_USERS' not in os.environ.keys():
    print("'HYMNUS_USERS' env variable not defined.")
    exit(1)

  os.chdir(os.environ['HYMNUS_USERS'])
  
  username = input('Enter user name: ')
  if username in os.listdir():
    username = input('User exists, choose another name: ')
  if username in os.listdir():
    username = input('User exists, choose another name: ')
  if username in os.listdir():
    username = input('User exists, choose another name: ')
  if username in os.listdir():
    print("Failed!")
    exit(1)


  password1 = getpass('Enter password:')
  password2 = getpass('Confirm password: ')
  
  if password1 != password2:
    print("Type password again!")
    password1 = getpass('Enter password:')
    password2 = getpass('Confirm password: ')

  if password1 != password2:
    print("Type password again!")
    password1 = getpass('Enter password:')
    password2 = getpass('Confirm password: ')

  if password1 != password2:
    print("Type password again!")
    password1 = getpass('Enter password:')
    password2 = getpass('Confirm password: ')
  
  if password1 != password2:
    print("Failed!")
    exit(1)
  
  m = hashlib.sha1()
  m.update(password1.encode())

  with open(username, 'w') as f:
    f.write(m.hexdigest())
  
  os.chmod(username, 400)
  
  print(f"User created: {username}")