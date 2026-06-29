#pragma once

#ifndef METADATA_HANDLER_HPP
#define METADATA_HANDLER_HPP

#include <string>
#include <cstdarg>

namespace hymnus {

enum class MetadataHandlerMode {
  Read,
  Create,
  Update,
  Delete,
  Unknown
};

class MetadataHandler {

protected:

  virtual void clear() = 0;

  virtual bool isValid() const = 0;

  virtual bool isExistsInDB() const = 0;

  virtual int pushToDB() const = 0;

  virtual int pullFromDB() const = 0;

  inline std::string fmtSqlInsertion(const char * __table, const char* __types, ...) {
    if (__types == nullptr || __table == nullptr) {
      return "";
    }

    va_list args;
    va_start(args, __types);

    std::string column_names(" (");
    std::string value_names(" VALUES (");

    while (*__types != '\0') {
      const char* name = va_arg(args, const char *);
      column_names += name;
      column_names += ",";

      if (*__types == 'i' || *__types == 'I') {
        int val = va_arg(args, int);
        value_names += std::to_string(val);
      }
      else if (*__types == 'r' || *__types == 'R') {
        double val = va_arg(args, double);
        value_names += std::to_string(val);
      }
      else if (*__types == 't' || *__types == 'T') {
        const char* val = va_arg(args, const char *);
        value_names.push_back('\'');
        value_names += val;
        value_names.push_back('\'');
      }
      value_names.push_back(',');
      ++__types;
    }
    va_end(args);

    // remove "," and add ")"
    column_names.pop_back();
    column_names += ") ";
    value_names.pop_back();
    value_names += ") ;";

    std::string table_name(__table);
    std::string sql = "INSERT INTO " + table_name + column_names + value_names;

    return sql;
  }


  inline std::string fmtSqlUpdate(const char * __table, const char * __cond, const char* __types, ...) {
    if (__types == nullptr || __table == nullptr) {
      return "";
    }

    va_list args;
    va_start(args, __types);

    std::string set_columns = " SET ";

    while (*__types != '\0') {
      const char* name = va_arg(args, const char *);
      set_columns += name;
      set_columns += " = ";

      if (*__types == 'i' || *__types == 'I') {
        int val = va_arg(args, int);
        set_columns += std::to_string(val);
      }
      else if (*__types == 'r' || *__types == 'R') {
        double val = va_arg(args, double);
        set_columns += std::to_string(val);
      }
      else if (*__types == 't' || *__types == 'T') {
        const char* val = va_arg(args, const char *);
        set_columns.push_back('\'');
        set_columns += val;
        set_columns.push_back('\'');
      }
      set_columns.push_back(',');
      ++__types;
    }
    va_end(args);

    set_columns.pop_back(); // remove ","

    std::string condition;
    if (__cond) {
      std::string s (__cond);
      if (!s.empty()) {
        condition = " WHERE " + s;
      }
    }
    condition.push_back(';');
    std::string table_name(__table);
    std::string sql = "UPDATE " + table_name + set_columns + condition;

    return sql;
  }

  inline std::string fmtSqlUpdate(const char * __table, const char * __cond) {
    if (__table == nullptr || __cond == nullptr) {
      return "";
    }
    std::string table_name(__table);
    std::string condition(__cond);
    if (table_name.empty() || condition.empty()) {
      return "";
    }
    std::string sql = "DELETE FROM " + table_name + " WHERE " + condition + " ;";
    return sql;
  }

};

} // namespace hymnus

#endif