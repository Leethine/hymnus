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
  wikipedia_url TEXT,
  imslp_url TEXT
);

INSERT INTO composers
(code,firstname,lastname,knownas_name,bornyear,diedyear)
VALUES ('zzz_unknown', ' ', ' ', 'U', -1, -1);

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
  editor TEXT
);

-- Table to store single pieces --
DROP TABLE IF EXISTS pieces;
CREATE TABLE pieces (
  composer_code TEXT,
  arranged BOOLEAN,
  arranger_code TEXT,
  collection_code TEXT,
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
