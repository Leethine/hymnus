import os, sys, argparse
import common_defs

def getParsedArgs():
  parser = argparse.ArgumentParser(description='Usage: ')
  parser.add_argument('search_criteria', metavar='List of token to search', type=str, nargs='*', help='List of search criteria', default=[])
  parser.add_argument('-c' ,'--code', nargs=1, help="Search by composer code", metavar='_name_initial', required=False, type=str, dest='code')
  parser.add_argument('-s' ,'--style', help="Optional, list of styles, leave blank if unknown", nargs="+", required=False, type=str, default=[], dest='style')
  parser.add_argument('-t' ,'--tags', help="Optional, list of tags, can be anything", nargs="+", required=False, type=str, default=[], dest='tags')
  return parser.parse_args()

if __name__ == '__main__':
  arg = getParsedArgs()
  print(arg.search_criteria)
  print(arg.code)
  print(arg.style)
  print(arg.tags)