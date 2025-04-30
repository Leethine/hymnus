-- Table to store composers --
DROP TABLE IF EXISTS composers;
CREATE TABLE composers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  code TEXT NOT NULL,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  knownas_name TEXT UNIQUE NOT NULL,
  bornyear INTEGER,
  diedyear INTEGER
);

-- Table to store collections --
DROP TABLE IF EXISTS collections;
CREATE TABLE collections (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  code TEXT NOT NULL,
  title TEXT NOT NULL,
  subtitle TEXT,
  subsubtitle TEXT,
  opus TEXT,
  description_text TEXT,
  volume INTEGER,
  composer_id INTEGER,
  composer_code TEXT,
  instruments TEXT,
  editor TEXT
);

-- Table to store single pieces --
DROP TABLE IF EXISTS pieces;
CREATE TABLE pieces (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  composer_id INTEGER,
  composer_code TEXT,
  arranged BOOLEAN,
  arranger_id INTEGER,
  arranger_code TEXT,
  collection_id INTEGER,
  collection_code TEXT,
  title TEXT NOT NULL,
  subtitle TEXT,
  subsubtitle TEXT,
  dedicated_to TEXT,
  opus TEXT,
  instrument TEXT,
  folder_hash TEXT NOT NULL CHECK (LENGTH(folder_hash) = 40),
  comment TEXT
);

/*
-- Table to store single (arranged) pieces --
DROP TABLE IF EXISTS arranged_pieces;
CREATE TABLE arranged_pieces (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  original_piece_id INTEGER,
  composer_id INTEGER,
  composer_code TEXT,
  arranger_id INTEGER,
  arranger_code TEXT,
  arranger_name TEXT,
  title TEXT NOT NULL,
  subtitle TEXT,
  subsubtitle TEXT,
  opus TEXT,
  instrument TEXT,
  folder_hash TEXT
);

-- Table to store item in collection --
DROP TABLE IF EXISTS items;
CREATE TABLE items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  original_piece_id INTEGER,
  composer_id INTEGER,
  composer_code TEXT,
  composer_name TEXT,
  collection_id INTEGER,
  serie_number INTEGER,
  title TEXT NOT NULL,
  subtitle TEXT,
  subsubtitle TEXT,
  opus TEXT,
  instrument TEXT,
  folder_hash TEXT
);
*/
