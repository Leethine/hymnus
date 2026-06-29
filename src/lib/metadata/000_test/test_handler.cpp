#include "metadata_handler.hpp"
#include <string>
#include <iostream>

namespace hymnus {

class MetadataHandlerTest : public MetadataHandler {

public:

  virtual void clear() {}

  virtual bool isValid() const { return true; }

  virtual bool isExistsInDB() const { return true; }

  virtual int pushToDB() const { return 1; }

  virtual int pullFromDB() const { return 1; }

  MetadataHandlerTest() {
  }

  void test1() {
    std::cout <<
    MetadataHandler::fmtSqlInsertion("Composers", "TII",
      "Name", "Someone", "Born", 1111, "Died", 1111)
    << "\n";
  }

  void test2() {
    std::cout <<
    MetadataHandler::fmtSqlInsertion("Composers", "TIR",
      "Name", "Someone", "Born", 1111, "Score", 16.2)
    << "\n";
  }

  void test3() {
    std::cout <<
    MetadataHandler::fmtSqlUpdate("Composers", "Name = \'bach\'", "TIR",
      "Name", "Johann", "Born", 1234, "Score", 99.8)
    << "\n";
  }

};
} // namespace hymnus

int main() {

  hymnus::MetadataHandlerTest t;
  t.test1();
  t.test2();
  t.test3();

  return 0;
}