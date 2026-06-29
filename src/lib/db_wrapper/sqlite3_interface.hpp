#pragma once

#ifndef SQLITE3_INTERFACE_HPP
#define SQLITE3_INTERFACE_HPP

#include "db_interface.hpp"

#ifndef HYMNUS_DB
#define HYMNUS_DB "HYMNUS_DB"
#endif

namespace hymnus {

class SQLite3_Interface : public DB_Interface {

protected:

  virtual int setDbPath(const std::string& __dbpath) noexcept;

  virtual std::string getDbPath() noexcept;

  virtual bool isType(const int __dbtype) noexcept;

public:

  SQLite3_Interface();

  SQLite3_Interface(const std::string& __db_path);

  virtual ~SQLite3_Interface();

  virtual int runSqlRead(const std::string& __sql,
                         std::vector<RowEntry>& __rows);

  virtual int runSqlRead(const std::string& __sql,
                         std::vector<RowEntry>& __rows,
                         const size_t __nth_page, const size_t __nbr_of_rows_per_page);

  virtual int runSqlWrite(const std::string& __sql);

  virtual size_t runSqlCount(const std::string& __sql);

};

} // namespace hymnus

#endif