#pragma once

#ifndef COMPOSER_HPP
#define COMPOSER_HPP

#include <string>
#include "metadata_handler.hpp"

namespace hymnus {

class DB_Interface;

class Composer : protected MetadataHandler {

private:

  MetadataHandlerMode _mode;

  std::string _code;

  std::string _firstname;

  std::string _lastname;

  std::string _knownas;

  std::string _code_new;

  int _listed;

  int _born;

  int _died;

protected:

  DB_Interface * _db_interface;

  inline void setFirstName(const std::string& __name) {
    _firstname = __name;
  }

  inline void setLastName(const std::string& __name) {
    _lastname = __name;
  }

  inline void setKnownAsName(const std::string& __name) {
    _knownas = __name;
  }

  inline void setCode(const std::string& __code) {
    _code = __code;
  }

  inline void setNewCode(const std::string& __code) {
    _code_new = __code;
  }

  inline void setListed(const int __listed) {
    _listed = __listed;
  }

  inline void setBornYear(const int __year) {
    _born = __year;
  }

  inline void setDiedYear(const int __year) {
    _died = __year;
  }

public:

  Composer(MetadataHandlerMode __mode);

  Composer();

  Composer(const std::string& __first, const std::string& __last, const std::string& __knownas,
           const int __born, const int __died, bool __listed = false);

  Composer(const std::string& __code, MetadataHandlerMode __mode = MetadataHandlerMode::Read);

  Composer(const std::string& __code, const std::string& __first, const std::string& __last,
           const std::string& __knownas, const int __born, const int __died, bool __listed = false);

  ~Composer();

  inline std::string getFirstName() const {
    return _firstname;
  }

  inline std::string getLastName() const {
    return _lastname;
  }

  inline std::string getKnownAsName() const {
    return _knownas;
  }

  inline std::string getCode() const {
    return _code;
  }

  inline std::string getNewCode() const {
    return _code_new;
  }

  inline int getListed() const {
    return _listed;
  }

  inline int getBornYear() const {
    return _born;
  }

  inline int getDiedYear() const {
    return _died;
  }

  inline bool isListed() const {
    return _listed > 0;
  }

  inline std::string getBornYearStr() const {
    if (_born > 0) {
      return std::to_string(_born);
    }
    else {
      return "?";
    }
  }

  inline std::string getDiedYearStr() const {
    if (_born > 0) {
      return std::to_string(_died);
    }
    else {
      return "?";
    }
  }

  virtual std::string calculateCode();

  virtual void clear();

  virtual bool isValid() const;

  virtual bool isExistsInDB() const;

  virtual int pushToDB();

  virtual int pullFromDB();

};

} // namespace hymnus

#endif