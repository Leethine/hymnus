#include <iostream>
#include "tiny_sha1.hpp"

void testSHA1(const std::string& val) {
  sha1::SHA1 s;
	s.processBytes(val.c_str(), val.size());
	uint32_t digest[5];
	s.getDigest(digest);
	char tmp[48];
  snprintf(tmp, 41, "%08x%08x%08x%08x%08x", digest[0], digest[1], digest[2], digest[3], digest[4]);
	//snprintf(tmp, 45, "%08x %08x %08x %08x %08x", digest[0], digest[1], digest[2], digest[3], digest[4]);
	std::cout<<"Calculated : (\""<<val<<"\") = "<<tmp<<std::endl;
}

int main() {

  testSHA1("Hello");
  testSHA1("Hello1");
  testSHA1("Hello2");
  testSHA1("Hello3");
  testSHA1("Hello4");

  return 0;
}