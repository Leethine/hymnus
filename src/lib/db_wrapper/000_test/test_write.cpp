#include "../sqlite3_interface.hpp"
#include <stdexcept>

using namespace hymnus;

int main(int argc, char ** argv) {

  SQLite3_Interface s;

  if (argc > 1) {
    std::string str (argv[1]);
    std::string str2;
    int n = 0;
    if (argc > 2) {
      str2 = std::string(argv[2]);
    }

    if (str == "d" || str == "del") {
      s.runSqlWrite("DELETE FROM A_Test_Table;");
    }
    else if (str2 == "d" || str2 == "del") {
      s.runSqlWrite("DELETE FROM A_Test_Table WHERE col1 = \'test" + str + "\';");
    }
    else {
      try {
        n = std::stoi(str);
        s.runSqlWrite("INSERT INTO A_Test_Table (col1,col2,col3) VALUES(\'test" + str + "\', \'hello" + str + "\'," + str + ");");
      }
      catch (std::invalid_argument const& ex) {
      }
      catch (std::out_of_range const& ex) {
      }
    }
  }

  return 0;
}