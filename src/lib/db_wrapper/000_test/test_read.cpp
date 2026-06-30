#include "../sqlite3_interface.hpp"
#include <iostream>

using namespace hymnus;

int main(int argc, char ** argv) {

  SQLite3_Interface s;

  int n_th_page = 0;
  int rows_per_page = 999999; 

  if (argc != 2 && argc != 4) {
    return 0;
  }

  if (argc == 4) {
    try {
      n_th_page     = std::stoi(std::string(argv[2]));
      rows_per_page = std::stoi(std::string(argv[3]));
    }
    catch (std::invalid_argument const& ex) {
    }
    catch (std::out_of_range const& ex) {
    }
  }

  std::vector<RowEntry> rows;
  const char * arg1 = argv[1];
  std::string str (arg1);
  if (str == "*" || str == "all") {
    s.runSqlRead("SELECT * FROM A_Test_Table ORDER BY col1;", rows, n_th_page, rows_per_page);
  }
  else {
    try {
      int n = std::stoi(str);
      s.runSqlRead("SELECT * FROM A_Test_Table ORDER BY col1 WHERE col1 = \'test" + str + "\';", rows, n_th_page, rows_per_page);
    }
    catch (std::invalid_argument const& ex) {
    }
    catch (std::out_of_range const& ex) {
    }
  }
  for (auto it = rows.begin(); it != rows.end(); it++) {
    for (auto it2 = it->begin(); it2 != it->end(); it2++) {
      std::cout << it2->first << ": " << it2->second << ", ";
    }
    std::cout << "\n";
  }

  return 0;
}