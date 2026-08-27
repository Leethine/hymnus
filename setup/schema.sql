-- Table to store composers --
DROP TABLE IF EXISTS composers;
CREATE TABLE composers (
  code          TEXT UNIQUE NOT NULL,
  firstname     TEXT NOT NULL,
  lastname      TEXT NOT NULL,
  knownas_name  TEXT UNIQUE NOT NULL,
  bornyear      INTEGER,
  diedyear      INTEGER,
  listed        INTEGER DEFAULT 0,
  wikipedia_url TEXT DEFAULT '',
  imslp_url     TEXT DEFAULT ''
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
  code             TEXT UNIQUE NOT NULL,
  composer_code    TEXT DEFAULT 'zzz_unknown',
  title            TEXT NOT NULL,
  subtitle         TEXT DEFAULT '',
  subsubtitle      TEXT DEFAULT '',
  opus             TEXT DEFAULT '',
  description_text TEXT DEFAULT '',
  volume           TEXT DEFAULT '',
  instruments      TEXT DEFAULT '',
  editor           TEXT DEFAULT '',
  -- list of hash of pieces this collection
  list_pieces      TEXT DEFAULT '',
  -- the serie how the pieces are presented
  -- e.g. num (1,2,3) or roman (I, II, III, IV) ... 
  list_series      TEXT DEFAULT ''
);

-- Table to store single pieces --
DROP TABLE IF EXISTS pieces;
CREATE TABLE pieces (
  composer_code TEXT DEFAULT 'zzz_unknown',
  arranged      BOOLEAN NOT NULL DEFAULT 0,
  arranger_code TEXT DEFAULT '',
  arranger_name TEXT DEFAULT '',
  title         TEXT NOT NULL,
  subtitle      TEXT DEFAULT '',
  subsubtitle   TEXT DEFAULT '',
  dedicated_to  TEXT DEFAULT '',
  opus          TEXT DEFAULT '',
  composed_year TEXT DEFAULT '?',
  instruments   TEXT DEFAULT '',
  folder_hash   TEXT UNIQUE NOT NULL
    CHECK (LENGTH(folder_hash) = 40),
  comment       TEXT DEFAULT ''
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
  file_description TEXT DEFAULT '',
  created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
  last_modified    DATETIME DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS piece_search;
CREATE TABLE piece_search (
  context         TEXT DEFAULT '',
  author          TEXT DEFAULT '',
  composer_code   TEXT NOT NULL DEFAULT 'zzz_unknown',
  opus            TEXT DEFAULT '',
  composed_year   TEXT DEFAULT '?',
  instruments     TEXT DEFAULT '',
  folder_hash     TEXT UNIQUE NOT NULL
    CHECK (LENGTH(folder_hash) = 40)
);

