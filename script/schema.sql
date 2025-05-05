-- Table to store composers --
DROP TABLE IF EXISTS composers;
CREATE TABLE composers (
  code TEXT UNIQUE NOT NULL,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  knownas_name TEXT UNIQUE NOT NULL,
  bornyear INTEGER,
  diedyear INTEGER,
  wikipedia_url TEXT,
  imslp_url TEXT
);

-- Table to store collections --
DROP TABLE IF EXISTS collections;
CREATE TABLE collections (
  code TEXT UNIQUE NOT NULL,
  composer_code TEXT,
  title TEXT NOT NULL,
  subtitle TEXT,
  subsubtitle TEXT,
  opus TEXT,
  description_text TEXT,
  volume INTEGER,
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
  instruments TEXT,
  folder_hash TEXT NOT NULL
    CHECK (LENGTH(folder_hash) = 40),
  comment TEXT
);
