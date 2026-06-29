#include "utils.hpp"
#include "tiny_sha1.hpp"
#include <utility>
#include <iconv.h>
#include <locale.h>

std::string sha1hash(const std::string& __input) {

  return "";
}

int iconv_utf8_to_ascii(const std::string& __src, std::string& __dest) {
  __dest.clear();

  iconv_t cd = iconv_open("ASCII//TRANSLIT", "UTF-8");
  if (cd == (iconv_t) - 1) {
    return ERROR_ICONV_OPEN;
  }
  
  char * input_str = (char*) malloc(__src.size() * sizeof(char));
  if (input_str == NULL) {
    return ERROR_MALLOC;
  }
  char * output_str = (char*) malloc((__src.size() * 2 + 1) * sizeof(char));
  if (output_str == NULL) {
    return ERROR_MALLOC;
  }

  strcpy(input_str, __src.c_str());
  char * inptr = input_str;
  char * outptr = output_str;

  size_t in_bytes = strlen(input_str);
  size_t out_bytes = __src.size() * 2;
  size_t result = iconv(cd, &inptr, &in_bytes, &outptr, &out_bytes);
  
  if (result == (size_t)-1) {
    if (errno == EILSEQ) {
      return ERROR_INVALID_CHAR;
    }
    iconv_close(cd);
    return -1;
  }

  *outptr = '\0';

  std::string s_converted (output_str);
  free(input_str);
  free(output_str);
  __dest = std::move(s_converted);

  return 0;
}