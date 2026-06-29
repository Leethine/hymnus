#include "sqlite3_interface.hpp"
#include "db_interface.hpp"
#include <string>
#include <cstddef>
#include <cstdlib>
#include <chrono>
#include <thread>
#include <sqlite3.h>

// wait time (in ms)
#define SQLITE_WRITE_WAIT_TIME 10
// total timeout (in ms)
#define SQLITE_WRITE_TIMEOUT 10000

namespace hymnus {

using namespace std::chrono_literals;

static int get_column_anytype(sqlite3_stmt * stmt, int iCol, std::string& oData) {
  int column_type = sqlite3_column_type(stmt, iCol);
  oData.clear();
  if (column_type == SQLITE_INTEGER) {
    int res = sqlite3_column_int(stmt, iCol);
    oData = std::to_string(res);
  }
  else if (column_type == SQLITE3_TEXT) {
    const unsigned char * res = sqlite3_column_text(stmt, iCol);
    oData = std::string(reinterpret_cast<const char *>(res));
  }
  else if (column_type == SQLITE_NULL) {
    oData.clear();
  }
  else if (column_type == SQLITE_FLOAT) {
    double res = sqlite3_column_double(stmt, iCol);
    oData = std::to_string(res);
  }
  else {
    return DBERROR_FAILED_TO_READ_DATA;
  }

  return DBERROR_OK;
}

int SQLite3_Interface::setDbPath(const std::string& __dbpath) noexcept {
  int rc;
  sqlite3 * db;
  rc = sqlite3_open_v2(__dbpath.c_str(), &db, SQLITE_OPEN_READONLY, NULL);
  if (rc != SQLITE_OK) {
    sqlite3_close(db);
    return DBERROR_FAILED_TO_OPEN_DB;
  }
  else {
    DB_Interface::setDbPath(__dbpath);
    sqlite3_close(db);
    _initialized = true;
    return DBERROR_OK;
  }
}

std::string SQLite3_Interface::getDbPath() noexcept {
  return DB_Interface::getDbPath();
}

bool SQLite3_Interface::isType(const int __dbtype) noexcept {
  return DB_Interface::isType(__dbtype);
}

SQLite3_Interface::SQLite3_Interface(): DB_Interface(DBTYPE_SQLITE3) {
  const char * dbpath = std::getenv(HYMNUS_DB);
  if (dbpath != NULL) {
    std::string path_str(dbpath);
    int ok;
    ok = SQLite3_Interface::setDbPath(path_str);
    if (ok == DBERROR_OK) {
      _initialized = true;
    }
  }
}

SQLite3_Interface::SQLite3_Interface(const std::string& __db_path): DB_Interface(DBTYPE_SQLITE3) {
  int ok;
  ok = SQLite3_Interface::setDbPath(__db_path);
  if (ok == DBERROR_OK) {
    _initialized = true;
  }
}

SQLite3_Interface::~SQLite3_Interface() {
}

int SQLite3_Interface::runSqlRead(const std::string& __sql,
                                  std::vector<RowEntry>& __rows) {
  if (!_initialized) {
    return DBERROR_NOT_INITIALIZED;
  }

  __rows.clear();
  std::string dbpath = SQLite3_Interface::getDbPath();
  sqlite3 * db;
  int rc;
  rc = sqlite3_open_v2(dbpath.c_str(), &db, SQLITE_OPEN_READONLY, NULL);
  if (rc != SQLITE_OK) {
    sqlite3_close(db);
    return DBERROR_FAILED_TO_OPEN_DB;
  }
  sqlite3_stmt* stmt;
  rc = sqlite3_prepare_v2(db, __sql.c_str(), -1, &stmt, NULL);
  if (rc != SQLITE_OK) {
    sqlite3_finalize(stmt);
    sqlite3_close(db);
    if (rc == SQLITE_ERROR) {
      return DBERROR_INVALID_SQL_SYNTAX;
    }
    return DBERROR_FAILED_TO_READ_DATA;
  }
  // do the work
  int total_columns = sqlite3_column_count(stmt);
  std::string col_val;
  RowEntry row;
  while (sqlite3_step(stmt) == SQLITE_ROW) {
    row.clear();
    for (int i = 0; i < total_columns; i++) {
      get_column_anytype(stmt, i, col_val);
      const char *col_name = sqlite3_column_name(stmt, i);
      std::string col_key(col_name);
      row.insert({col_key, col_val});
    }
    __rows.push_back(row);
  }

  sqlite3_finalize(stmt);
  sqlite3_close(db);
  return DBERROR_OK;
}

int SQLite3_Interface::runSqlRead(const std::string& __sql,
                                  std::vector<RowEntry>& __rows,
                                  const size_t __nth_page, const size_t __nbr_of_rows_per_page) {
  if (!_initialized) {
    return DBERROR_NOT_INITIALIZED;
  }

  __rows.clear();
  std::string dbpath = SQLite3_Interface::getDbPath();
  sqlite3 * db;
  int rc;
  rc = sqlite3_open_v2(dbpath.c_str(), &db, SQLITE_OPEN_READONLY, NULL);
  if (rc != SQLITE_OK) {
    sqlite3_close(db);
    return DBERROR_FAILED_TO_OPEN_DB;
  }
  sqlite3_stmt* stmt;
  rc = sqlite3_prepare_v2(db, __sql.c_str(), -1, &stmt, NULL);
  if (rc != SQLITE_OK) {
    sqlite3_finalize(stmt);
    sqlite3_close(db);
    if (rc == SQLITE_ERROR) {
      return DBERROR_INVALID_SQL_SYNTAX;
    }
    return DBERROR_FAILED_TO_READ_DATA;
  }

  // skip the pages
  size_t n_skip = __nth_page * __nbr_of_rows_per_page;
  for(size_t i = 0; i < n_skip; i++) {
    sqlite3_step(stmt);
  }

  // do the work
  int total_columns = sqlite3_column_count(stmt);
  std::string col_val;
  RowEntry row;
  size_t count = 0;
  while (sqlite3_step(stmt) == SQLITE_ROW && count++ < __nbr_of_rows_per_page) {
    row.clear();
    for (int i = 0; i < total_columns; i++) {
      get_column_anytype(stmt, i, col_val);
      const char *col_name = sqlite3_column_name(stmt, i);
      std::string col_key(col_name);
      row.insert({col_key, col_val});
    }
    __rows.push_back(row);
  }

  sqlite3_finalize(stmt);
  sqlite3_close(db);
  return DBERROR_OK;
}

int SQLite3_Interface::runSqlWrite(const std::string& __sql) {
  if (!_initialized) {
    return DBERROR_NOT_INITIALIZED;
  }

  // TODO: set timeout using sqlite3_busy_timeout(XXms) to avoid manually handling timeout
  int elapsed_ms = 0;
  std::string dbpath = SQLite3_Interface::getDbPath();
  sqlite3 * db;
  int rc;
  rc = sqlite3_open_v2(dbpath.c_str(), &db, SQLITE_OPEN_READWRITE, NULL);
  if (rc != SQLITE_OK) {
    sqlite3_close(db);
    return DBERROR_FAILED_TO_OPEN_DB;
  }

  char* errmsg = nullptr;
  while (elapsed_ms < SQLITE_WRITE_TIMEOUT) {
    rc = sqlite3_exec(db, __sql.c_str(), NULL, NULL, &errmsg);
    sqlite3_free(errmsg); // no need error message
    if (rc == SQLITE_OK) {
      break;
    }
    else {
      if (rc == SQLITE_BUSY || rc == SQLITE_LOCKED) {
        std::this_thread::sleep_for(SQLITE_WRITE_WAIT_TIME * 1ms);
        elapsed_ms += SQLITE_WRITE_WAIT_TIME;
      }
      else {
        sqlite3_close(db);
        return DBERROR_FAILED_TO_WRITE_DATA;
      }
    }
  }

  sqlite3_close(db);
  return DBERROR_OK;
}

size_t SQLite3_Interface::runSqlCount(const std::string& __sql) {
  if (!_initialized) {
    return 0;
  }
  std::string dbpath = SQLite3_Interface::getDbPath();
  sqlite3 * db;
  int rc;
  rc = sqlite3_open_v2(dbpath.c_str(), &db, SQLITE_OPEN_READONLY, NULL);
  if (rc != SQLITE_OK) {
    sqlite3_close(db);
    return 0;
  }
  sqlite3_stmt* stmt;
  rc = sqlite3_prepare_v2(db, __sql.c_str(), -1, &stmt, NULL);
  if (rc != SQLITE_OK) {
    sqlite3_finalize(stmt);
    sqlite3_close(db);
    return 0;
  }

  rc = sqlite3_step(stmt);
  if (rc == SQLITE_ROW && sqlite3_column_type(stmt, 0) == SQLITE_INTEGER) {
    size_t value = (size_t) sqlite3_column_int(stmt, 0);
    sqlite3_finalize(stmt);
    sqlite3_close(db);
    return value;
  }

  sqlite3_finalize(stmt);
  sqlite3_close(db);
  return 0;
}

} // namespace hymnus