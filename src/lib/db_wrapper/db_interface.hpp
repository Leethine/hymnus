#pragma once

#ifndef DB_INTERFACE_HPP
#define DB_INTERFACE_HPP

#define DBTYPE_SQLITE3 324
#define DBTYPE_COUCHDB 423
#define DBTYPE_POSTGRE 156

#define DBERROR_OK                   0
#define DBERROR_INVALID_SQL_SYNTAX   1
#define DBERROR_FAILED_TO_OPEN_DB    2
#define DBERROR_FAILED_TO_READ_DATA  3
#define DBERROR_FAILED_TO_WRITE_DATA 4
#define DBERROR_NOT_INITIALIZED      5

#include <string>
#include <vector>
#include <map>

namespace hymnus {

using RowEntry = std::map<std::string,std::string>;

class DB_Interface {

private:

  const int _dbtype;

  std::string _dbpath;

protected:

  bool _initialized;

  inline virtual int setDbPath(const std::string& __dbpath) noexcept {
    _dbpath = __dbpath;
    return 0;
  }

  inline virtual std::string getDbPath() noexcept {
    return _dbpath;
  }

  inline virtual bool isType(const int __dbtype) noexcept {
    if (_dbtype == __dbtype) {
      return true;
    }
    return false;
  }

public:

  inline DB_Interface(const int __db_type) :
    _dbtype ( __db_type ), _dbpath ( "" ), _initialized ( false ) {
  }

  inline virtual ~DB_Interface() {}

  virtual int runSqlRead(const std::string& __sql,
                         std::vector<RowEntry>& __rows) = 0;

  virtual int runSqlRead(const std::string& __sql,
                         std::vector<RowEntry>& __rows,
                         const size_t __nth_page,
                         const size_t __nbr_of_rows_per_page) = 0;

  virtual int runSqlWrite(const std::string& __sql) = 0;

  virtual size_t runSqlCount(const std::string& __sql) = 0;

};

} // namespace hymnus

#endif