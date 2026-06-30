#include "../sqlite3_interface.hpp"
#include <cstdlib>
#include <string>
#include <future>
#include <chrono>
#include <iostream>

#define ACTIVE_USERS 100
#define N_ROUNDS 1000

using namespace hymnus;

int read_something(SQLite3_Interface * __interface) {
  std::vector<RowEntry> __rows;
  __interface->runSqlRead("SELECT * FROM A_Test_Table ORDER BY col1;", __rows, 3, 2);
  return 0;
}

int write_something(SQLite3_Interface * __interface, const std::string& random_value) {
  //std::string random_value = std::to_string(std::rand());
  int count = __interface->runSqlCount("SELECT COUNT(*) FROM A_Test_Table WHERE col2 = \'hello" + random_value + "\';");
  if (count == 0) {
    __interface->runSqlWrite("INSERT INTO A_Test_Table (col1,col2,col3) VALUES(\'test" + random_value + "\', \'hello" + random_value + "\'," + random_value + ");");
  }
  // __interface->runSqlWrite("DELETE FROM A_Test_Table WHERE col2 = \'hello" + random_value + "\';");
  return 0;
}

int main() {
  SQLite3_Interface s_read[ACTIVE_USERS];
  SQLite3_Interface s_write[ACTIVE_USERS];

  int count = 0;
  std::string count_s;
  auto t_start = std::chrono::steady_clock::now();
  while(count++ < N_ROUNDS) {
    int random_worker = std::rand() % 100;
    count_s = std::to_string(count);
    std::future<int> a1 = std::async(std::launch::async, write_something, &s_write[random_worker], count_s);
    std::future<int> a2 = std::async(std::launch::async, read_something, &s_read[random_worker]);
  }
  auto t_end = std::chrono::steady_clock::now();
  auto elapsed = t_end - t_start;
  auto elapsed_ms = std::chrono::duration_cast<std::chrono::milliseconds>(elapsed).count();
  std::cout << "Elapsed time: " << elapsed_ms << " ms\n";

  return 0;
}
