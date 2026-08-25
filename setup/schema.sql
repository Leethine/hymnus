-- Table to store composers --
DROP TABLE IF EXISTS composers;
CREATE TABLE composers (
  code TEXT UNIQUE NOT NULL,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  knownas_name TEXT UNIQUE NOT NULL,
  bornyear INTEGER,
  diedyear INTEGER,
  listed INTEGER DEFAULT 0,
  wikipedia_url TEXT DEFAULT '',
  imslp_url TEXT DEFAULT ''
);

INSERT INTO composers
  (code,firstname,lastname,knownas_name,bornyear,diedyear)
VALUES ('zzz_unknown', ' ', ' ', '?', -1, -1);

INSERT INTO composers
  (code,firstname,lastname,knownas_name,bornyear,diedyear)
VALUES ('zzz_anonymous', ' ', ' ', 'Anonymous', -1, -1);

INSERT INTO composers
  (code,firstname,lastname,knownas_name,bornyear,diedyear)
VALUES ('zzz_various', ' ', ' ', 'Various', -1, -1);

-- Table to store collections --
DROP TABLE IF EXISTS collections;
CREATE TABLE collections (
  code TEXT UNIQUE NOT NULL,
  composer_code TEXT DEFAULT 'zzz_unknown',
  title TEXT NOT NULL,
  subtitle TEXT,
  subsubtitle TEXT,
  opus TEXT,
  description_text TEXT,
  volume TEXT,
  instruments TEXT,
  editor TEXT,
  -- list of hash of pieces this collection
  list_pieces TEXT,
  -- the serie how the pieces are presented
  -- e.g. num (1,2,3) or roman (I, II, III, IV) ... 
  list_series TEXT
);

-- Table to store single pieces --
DROP TABLE IF EXISTS pieces;
CREATE TABLE pieces (
  composer_code TEXT,
  arranged BOOLEAN NOT NULL DEFAULT 0,
  arranger_code TEXT,
  arranger_name TEXT,
  title TEXT NOT NULL,
  subtitle TEXT,
  subsubtitle TEXT,
  dedicated_to TEXT,
  opus TEXT,
  composed_year TEXT DEFAULT '?',
  instruments TEXT,
  folder_hash TEXT UNIQUE NOT NULL
    CHECK (LENGTH(folder_hash) = 40),
  comment TEXT
);

-- Table to store file information --
DROP TABLE IF EXISTS piece_files;
CREATE TABLE piece_files (
  folder_hash TEXT NOT NULL
    CHECK (LENGTH(folder_hash) = 40),
  file_path        TEXT NOT NULL,
  file_name        TEXT NOT NULL,
  file_extension   TEXT NOT NULL,
  file_title       TEXT NOT NULL,
  file_description TEXT,
  created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
  last_modified    DATETIME DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS piece_search;
CREATE TABLE piece_search (
  context         TEXT,
  author          TEXT,
  composer_code   TEXT NOT NULL DEFAULT 'zzz_unknown',
  opus            TEXT,
  composed_year   TEXT DEFAULT '?',
  instruments     TEXT,
  folder_hash     TEXT UNIQUE NOT NULL
    CHECK (LENGTH(folder_hash) = 40)
);

