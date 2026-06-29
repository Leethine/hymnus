#include "sqlite3_interface.hpp"
#include <iostream>

using namespace hymnus;

int main() {

  SQLite3_Interface s;

  std::vector<RowEntry> rows;
  size_t val = s.runSqlCount("SELECT COUNT(*) FROM Composers WHERE lastname = 'Bach';");
  std::cout << "COUNT: " << val << "\n";

  return 0;
}