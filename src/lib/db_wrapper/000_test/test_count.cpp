#include "../sqlite3_interface.hpp"
#include <iostream>

using namespace hymnus;

int main(int argc, char ** argv) {

  SQLite3_Interface s;

  size_t val = 0;
  if (argc > 1) {
    const char * arg1 = argv[1];
    std::string str (arg1);
    val = s.runSqlCount("SELECT COUNT(*) FROM A_Test_Table WHERE col1 = \'test" + str + "\';");
  }
  else {
    val = s.runSqlCount("SELECT COUNT(*) FROM A_Test_Table;");
  }

  std::cout << val;
  return 0;
}