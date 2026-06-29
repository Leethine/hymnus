#include "sqlite3_interface.hpp"
#include <iostream>

using namespace hymnus;

int main() {

  SQLite3_Interface s;

  std::vector<RowEntry> rows;
  s.runSqlRead("SELECT * FROM Composers ORDER BY code;", rows, 2, 3);

  for (auto it = rows.begin(); it != rows.end(); it++) {
    for (auto it2 = it->begin(); it2 != it->end(); it2++) {
      std::cout << it2->first << ": " << it2->second << ", ";
    }
    std::cout << "\n";
  }

  return 0;
}