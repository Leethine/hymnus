import os, sys, argparse

def get_db_root() -> str:
  #TODO replace it with setting
  return "test_db"

def safe_create_dir(fpath: str):
  if not os.path.exists(fpath):
    os.mkdir(fpath)
  else:
    print("Folder already exist: {}".format(fpath))
  
def validate_dir(root_path: str) -> bool:
  if not os.path.exists(root_path):
    return False
  if not os.path.exists(root_path + "/composer_info"):
    return False
  if not os.path.exists(root_path + "/composer_info/photo"):
    return False
  if not os.path.exists(root_path + "/composer_pieces"):
    return False
  if not os.path.exists(root_path + "/composer_various"):
    return False
  if not os.path.exists(root_path + "/collections"):
    return False
  if not os.path.exists(root_path + "/collections_various"):
    return False
  if not os.path.exists(root_path + "/arrangements"):
    return False
  if not os.path.exists(root_path + "/templates"):
    return False
  
  return True

def create_db(root_path: str):
  if not os.path.exists(root_path):
    os.mkdir(root_path)
  if not os.path.exists(root_path + "/composer_info"):
    os.mkdir(root_path + "/composer_info")
  if not os.path.exists(root_path + "/composer_info/photo"):
    os.mkdir(root_path + "/composer_info/photo")
  if not os.path.exists(root_path + "/composer_pieces"):
    os.mkdir(root_path + "/composer_pieces")
  if not os.path.exists(root_path + "/composer_various"):
    os.mkdir(root_path + "/composer_various")
  if not os.path.exists(root_path + "/collections"):
    os.mkdir(root_path + "/collections")
  if not os.path.exists(root_path + "/collections_various"):
    os.mkdir(root_path + "/collections_various")
  if not os.path.exists(root_path + "/arrangements"):
    os.mkdir(root_path + "/arrangements")
  if not os.path.exists(root_path + "/templates"):
    os.mkdir(root_path + "/templates")

if __name__ == '__main__':
  dbroot = get_db_root()
  if not validate_dir(dbroot):
    create_db(dbroot)