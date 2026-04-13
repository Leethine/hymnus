from metadata import Metadata
from filemanager import FileManager
from flask import render_template
from config import COMPOSERS_PER_PAGE, COLLECTIONS_PER_PAGE, PIECES_PER_PAGE
import math, os


def render_composer_list(page=1, items_per_page=COMPOSERS_PER_PAGE):
  composer_list = Metadata().reader().getPartialComposers(items_per_page=items_per_page, page_number=page, listed_only=True)
  total_composers = Metadata().reader().countComposers(listed_only=True)
  total_pages = int(math.ceil(total_composers / float(items_per_page)))
  return render_template("list_composers.html", \
                          composer_list=composer_list, \
                          current_page=page, \
                          total_pages=total_pages)


def render_collection_list(page=1, items_per_page=COLLECTIONS_PER_PAGE):
  collection_list = Metadata().reader().getPartialCollections(items_per_page=items_per_page, page_number=page)
  total_collections = Metadata().reader().countCollections()
  total_pages = int(math.ceil(total_collections / float(items_per_page)))
  composer_code_dict = Metadata().reader().getComposerCodeNameDict()
  return render_template("list_collections.html", \
                          collection_list=collection_list, \
                          composer_code_dict=composer_code_dict, \
                          current_page=page, \
                          total_pages=total_pages)


def render_piece_list(page=1, items_per_page=PIECES_PER_PAGE):
  piece_list = Metadata().reader().getPartialPieces(items_per_page=items_per_page, page_number=page)
  total_pieces = Metadata().reader().countPieces()
  total_pages = int(math.ceil(total_pieces / float(items_per_page)))
  composer_code_dict = Metadata().reader().getComposerCodeNameDict()
  return render_template("list_all_pieces.html", \
                          piece_list=piece_list, \
                          composer_code_dict=composer_code_dict, \
                          current_page=page, \
                          total_pages=total_pages)


def render_composer_piece_list(composer_code, page=1, items_per_page=PIECES_PER_PAGE):
  piece_list = Metadata().reader().getComposerPartialPieces(composer_code, items_per_page=items_per_page, page_number=page)
  total_pieces = Metadata().reader().countComposerPieces(composer_code)
  total_pages = int(math.ceil(total_pieces / float(items_per_page)))
  composer = Metadata().reader().getComposer(composer_code)
  if not composer:
    return ""

  # Get abbr name, e.g. "Johann Sebastian Bach" ==> "J S Bach"
  composer['knownas_name'] = composer.get('knownas_name', 'Unknown')
  abbr_name = [l[0] for l in composer['knownas_name'].split(' ')[:-1]] + [composer['knownas_name'].split(' ')[-1]]
  abbr_name = ' '.join(abbr_name)
  print(abbr_name)
  return render_template("list_composer_pieces.html", \
                          piece_list=piece_list, \
                          composer_dict=composer, \
                          composer_abbr=abbr_name, \
                          current_page=page, \
                          total_pages=total_pages)


def render_collection_piece_list(collection_code):
  piece_list = Metadata().reader().getCollectionPieces(collection_code)
  collection = Metadata().reader().getCollection(collection_code)
  if not collection:
    return ""

  composer_name = ""
  if 'composer_code' in collection:
    composer = Metadata().reader().getComposer(collection['composer_code'])
    composer_name = "???"
    if composer and 'knownas_name' in composer:
      composer_name = composer['knownas_name']
  
  # Optional, show N/A for fields where info is missing
  for k in collection.keys():
    if not collection[k]:
      collection[k] = "N/A"

  return render_template("list_collection_pieces.html", \
                          piece_list=piece_list, \
                          collection_dict=collection, \
                          composer_name=composer_name)


def render_piece_files(folder_hash: str) -> str:
  piece = Metadata().reader().getPiece(folder_hash)
  if not piece:
    return ""
  
  # Set arranger name
  arranger_name = "Original"
  # Try to get arranger name from DB if code exists
  if 'arranger_code' in piece and piece['arranger_code']:
    arranger = Metadata().reader().getComposer(piece['arranger_code'])
    if arranger and 'knownas_name' in arranger:
      arranger_name = arranger['knownas_name']
  # Try to get arranger name from DB directly in case the user provided
  # only the arranger name without code when creating the piece
  if 'arranger_name' in piece and piece['arranger_name'] and arranger_name == "Original":
    arranger_name = piece['arranger_name']

  composer_name = "!??"
  composer = Metadata().reader().getComposer(piece.get('composer_code', ""))
  if composer and 'knownas_name' in composer.keys():
    composer_name = composer['knownas_name']
  

  file_list = FileManager().getPieceFileListDB(folder_hash)
  warning = ""
  if not FileManager().verifyFileList(folder_hash):
    warning = "File list in the file system does not match the metadata in DB."
  
  # Optional, show N/A for fields where info is missing
  for k in piece.keys():
    if not piece[k]:
      piece[k] = "N/A"
  if 'opus' in piece and piece['opus'] == "N/A":
    piece['opus'] = "" # No need for 'opus'

  return render_template("list_piece_files.html", \
                          piece_metadata=piece, \
                          file_metadata_list=file_list, \
                          composer_name=composer_name, \
                          arranger_name=arranger_name, \
                          warning=warning)


def get_download_file_path(folder_hash: str, filename: str) -> str:
  file_path = FileManager().getPieceFilePathDB(folder_hash, filename)
  if file_path and os.path.isfile(file_path):
    return os.path.abspath(file_path)
  else:
    return ""


def get_download_file_blob(folder_hash: str, filename: str) -> bytes:
  return FileManager().downloadFile(folder_hash, filename)


def get_search_page():
  return render_template("search.html", \
                          search_results=[], \
                          composer_dict={})


def render_search_result(req_args):
  composer_code_name_dict = Metadata().reader().getComposerCodeNameDict()
  if req_args and 'keywords' in req_args and 'radio-select' in req_args:
    keyword = req_args['keywords']
    method = req_args['radio-select']
    if method == "substring":
      search_res = Metadata().reader().searchPiecesBySubstr(keyword)
      return render_template("search.html", \
                              search_results=search_res, \
                              composer_dict=composer_code_name_dict)
    #TODO add other search methods ( instrument search, fuzzy search)
  return render_template("search.html", \
                          search_results=[], \
                          composer_dict=composer_code_name_dict)