import os, sys, argparse
import common_defs

def getParsedArgs():
  parser = argparse.ArgumentParser(description='Usage: ')
  parser.add_argument('-c' ,'--code', nargs=1, help="Composer code", metavar='_name_initial', required=True, type=str, dest='code')
  parser.add_argument('-gn' ,'--given-name', help="List of given names, can be separated by space", required=True, nargs="+", type=str, dest='gname')
  parser.add_argument('-fn' ,'--family-name', help="Family name, can be separated by space", required=True, nargs="+", type=str, dest='fname')
  parser.add_argument('-by' ,'--born-year', help="Optional, leave blank if unknown", nargs=1, required=False, type=str, default=[], dest='born')
  parser.add_argument('-dy' ,'--died-year', help="Optional, leave blank if unknown", nargs=1, required=False, type=str, default=[], dest='died')
  parser.add_argument('-s' ,'--style', help="Optional, list of styles, leave blank if unknown", nargs="+", required=False, type=str, default=[], dest='style')
  parser.add_argument('-t' ,'--tags', help="Optional, list of tags, can be anything", nargs="+", required=False, type=str, default=[], dest='tags')
  return parser.parse_args()

def composeInfoText(args):
  infotext = ""
  nl = "\n"
  if type(args.fname) == list and len(args.fname) > 0:
    infotext += "Family Name: "
    infotext += ' '.join(args.fname) + nl
  else:
    return ""
  if type(args.gname) == list and len(args.gname) > 0:
    infotext += "Given Name: "
    infotext += ' '.join(args.gname) + nl
  else:
    return ""
  
  if type(args.code) == list and len(args.code) == 1:
    infotext += "Composer Code: " + args.code[0] + nl
  else:
    return ""
  
  if type(args.born) == list and len(args.born) == 1:
    infotext += "Born: " + args.born[0] + nl
  elif len(args.born) == 0:
    infotext += "Born: " + "?" + nl
  else:
    return ""

  if type(args.died) == list and len(args.died) == 1:
    infotext += "Died: " + args.died[0] + nl
  elif len(args.died) == 0:
    infotext += "Died: " + "?" + nl
  else:
    return ""
  
  if type(args.style) == list:
    infotext += "Style: "
    infotext += ' '.join(args.style) + nl
  else:
    return ""
  
  if type(args.tags) == list:
      infotext += "Tag: "
      infotext += ' '.join(args.tags) + nl
  else:
    return ""
  
  return infotext

def createInfoFile(args, dir_path: str):
  if os.path.exists(dir_path):
    with open(dir_path + "/" + args.code[0] + ".info", "w+") as f:
      f.write(composeInfoText(args))
  else:
    print("Invalid file path: {}".format(dir_path))

def createNewComposer(db_root_path: str):
  if not common_defs.validate_dir(db_root_path):
    print("Invalid DB structure: {}".format(db_root_path))
    return
  
  arg = getParsedArgs()
  createInfoFile(arg, db_root_path + "/composer_info")
  
  common_defs.safe_create_dir(db_root_path + "/composer_pieces/" + arg.code[0])
  common_defs.safe_create_dir(db_root_path + "/collections/" + arg.code[0])
  common_defs.safe_create_dir(db_root_path + "/arrangements/" + arg.code[0])
  
if __name__ == '__main__':
  dbroot = common_defs.get_db_root()
  createNewComposer("test_db")
  