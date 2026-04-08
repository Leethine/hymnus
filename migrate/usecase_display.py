from metadata import Metadata
from flask import render_template
from config import COMPOSERS_PER_PAGE, COLLECTIONS_PER_PAGE, PIECES_PER_PAGE
import math

def render_composer_list(page=1, items_per_page=COMPOSERS_PER_PAGE):
  composer_list = Metadata().reader().getPartialComposers(items_per_page=items_per_page, page_number=page, listed_only=False)
  total_composers = Metadata().reader().countComposers(listed_only=False)
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

  composer_name = ""
  if 'composer_code' in collection:
    composer = Metadata().reader().getComposer(collection['composer_code'])
    composer_name = "???"
    if composer and 'knownas_name' in composer:
      composer_name = composer['knownas_name']

  return render_template("list_collection_pieces.html", \
                          piece_list=piece_list, \
                          collection_dict=collection, \
                          composer_name=composer_name)

