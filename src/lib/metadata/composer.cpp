#include "composer.hpp"
#include "metadata_handler.hpp"
#include "../db_wrapper/sqlite3_interface.hpp"
#include <iterator>
#include <list>
#include <algorithm>
#include <cctype>
#include <iconv.h>
#include <vector>

namespace hymnus {

Composer::Composer(MetadataHandlerMode __mode) :
  _mode( __mode ),
  _code (), _firstname (), _lastname (), _knownas (),
  _code_new (), _listed ( 0 ), _born ( -1 ), _died ( -1 ),
  _db_interface ( nullptr ) {
  if (_mode != MetadataHandlerMode::Unknown) {
    _db_interface = new SQLite3_Interface();
  }
}

Composer::Composer() : Composer(MetadataHandlerMode::Read) {
}

Composer::Composer(const std::string& __first, const std::string& __last,
                   const std::string& __knownas, const int __born, const int __died,
                   bool __listed) : Composer(MetadataHandlerMode::Create) {
  _firstname = __first;
  _lastname  = __last;
  _knownas   = __knownas;
  _born      = __born;
  _died      = __died;
  if (__listed) {
    _listed = 1;
  }
  else {
    _listed = 0;
  }
}

Composer::Composer(const std::string& __code, MetadataHandlerMode __mode): Composer(__mode) {
  _code = __code;
}

Composer::Composer(const std::string& __code,
                   const std::string& __first, const std::string& __last,
                   const std::string& __knownas, const int __born, const int __died,
                   bool __listed) : Composer(MetadataHandlerMode::Update) {
  _firstname = __first;
  _lastname  = __last;
  _knownas   = __knownas;
  _born      = __born;
  _died      = __died;
  if (__listed) {
    _listed = 1;
  }
  else {
    _listed = 0;
  }
  _code = __code;
}

Composer::~Composer() {
  delete _db_interface;
}

std::string Composer::calculateCode() {
  std::list<std::string> name_list;
  std::string remaining(_knownas);
  size_t space_pos = remaining.find(' ');
  if (space_pos == std::string::npos) {
     name_list.push_back(_knownas);
  }
  else {
    while (space_pos != std::string::npos) {
      name_list.push_back(remaining.substr(0,space_pos));
      if (space_pos+1 < remaining.size()) {
        remaining = remaining.substr(space_pos+1);
      }
      else {
        remaining = "";
      }
      space_pos = remaining.find(' ');
    }
  }
  // Extract
  _code_new = name_list.back();
  name_list.pop_back();
  _code_new.push_back('_');
  while (!name_list.empty()) {
    std::string n = name_list.front();
    if (!n.empty()) {
      _code_new.push_back(n.front());
      _code_new.push_back('_');
    }
    name_list.pop_front();
  }
  // to lower-case
  std::transform(_code_new.begin(), _code_new.end(), _code_new.begin(),
    [](unsigned char c) { return std::tolower(c); });
  return _code_new;
}

void Composer::clear() {
  if (_mode == MetadataHandlerMode::Read) {
    _code_new.clear();
    _firstname.clear();
    _lastname.clear();
    _knownas.clear();
    _code.clear();
    _listed = 0;
    _born = -1;
    _died = -1;
  }
  else {
    _code_new.clear();
  }
}

bool Composer::isValid() const {
  if (_db_interface == nullptr) {
    return false;
  }
  if (_mode == MetadataHandlerMode::Read && _code.empty()) {
    return false;
  }
  else if (_mode == MetadataHandlerMode::Create && 
    (_code_new.empty() || _knownas.empty() || _lastname.empty())) {
    return false;
  }
  else if (_mode == MetadataHandlerMode::Update &&
    (_code.empty() || _knownas.empty() || _lastname.empty())) {
    return false;
  }
  else if (_mode == MetadataHandlerMode::Delete && _code.empty()) {
    return false;
  }

  return true;

}

bool Composer::isExistsInDB() const {
  size_t count = 0;
  std::string sql ("SELECT COUNT(*) FROM Composers WHERE code = \'");
  if ((_mode == MetadataHandlerMode::Read || _mode == MetadataHandlerMode::Update)
    && !_code.empty()) {
    sql += _code + "\';";
    count = _db_interface->runSqlCount(sql);
  }
  else if (_mode == MetadataHandlerMode::Create && !_code_new.empty()) {
    sql += _code_new + "\';";
    count = _db_interface->runSqlCount(sql);
  }
  return count > 0;
}

int Composer::pushToDB() {
  int result = -1;
  if (_mode == MetadataHandlerMode::Create && Composer::isValid()) {
    Composer::calculateCode();
    std::string sql =
    MetadataHandler::fmtSqlInsertion("Composers", "TTTTIII", 
      "code", _code_new.c_str(), "firstname", _firstname.c_str(),
      "lastname", _lastname.c_str(), "knownas_name", _knownas.c_str(),
      "bornyear", _born, "diedyear", _died, "listed", _listed);
    result = _db_interface->runSqlWrite(sql);
  }
  else if (_mode == MetadataHandlerMode::Update && Composer::isValid()) {
    std::string condition = "code = \'" + _code + "\'";
    std::string sql =
    MetadataHandler::fmtSqlUpdate("Composers", 
      condition.c_str(), "I", "listed", _listed);
    result = _db_interface->runSqlWrite(sql);
  }
  else if (_mode == MetadataHandlerMode::Delete && Composer::isValid()) {
    std::string sql = "DELETE FROM Composers WHERE code = \'" + _code + "\'";
    result = _db_interface->runSqlWrite(sql);
  }
  return result;
}

int Composer::pullFromDB() {
  int result = -1;
  if (_mode == MetadataHandlerMode::Read && Composer::isExistsInDB()) {
    std::string sql = "SELECT * FROM Composers WHERE code = \'" + _code + "\';";
    std::vector<RowEntry> rows;
    result = _db_interface->runSqlRead(sql, rows);
    if (rows.size() == 1) {
      RowEntry& data = rows.front();
      _firstname = data.at("firstname");
      _lastname  = data.at("lastname");
      _born      = std::stoi(data.at("bornyear"));
      _died      = std::stoi(data.at("diedyear"));
      _listed    = std::stoi(data.at("listed"));
    }
  }
  return result;
}

} // namespace hymnus