#include <cstddef>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <stdlib.h>
#include <iconv.h>
#include <locale.h>

std::string testConv(const std::string& val) {
  iconv_t cd = iconv_open("ASCII//TRANSLIT", "UTF-8");
  if (cd == (iconv_t) - 1) {
    fprintf(stderr, "iconv_open failed");
    return "";
  }
  
  char * input_str = (char*) malloc(val.size() * sizeof(char));
  char * output_str = (char*) malloc((val.size() + 101) * sizeof(char));
  if (input_str == NULL || output_str == NULL) {
    fprintf(stderr, "malloc failed");
    //free(input_str);
    free(output_str);
    return "";
  }
  strcpy(input_str, val.c_str());
  char * inptr = input_str;
  char * outptr = output_str;

  size_t in_bytes = strlen(input_str);
  size_t out_bytes = val.size() + 100;
  size_t result = iconv(cd, &inptr, &in_bytes, &outptr, &out_bytes);
  
  if (result == (size_t)-1) {
    if (errno == E2BIG) {
      fprintf(stderr, "Error: Output buffer too small.\n");
    }
    else if (errno == EILSEQ) {
      fprintf(stderr, "Error: Invalid character sequence found.\n");
    }
    else if (errno == EINVAL) {
      fprintf(stderr, "Error: Incomplete multi-byte sequence at string end.\n");
    }
    iconv_close(cd);
    return "";
  }

  *outptr = '\0';

  std::string s_converted (output_str);
  free(input_str);
  free(output_str);

  return s_converted;
}

int main(int argc, char ** argv) {

  setlocale(LC_CTYPE, "");

  if (argc > 1) {
    std::string s (argv[1]);
    std::cout << testConv(s) << "\n";
  }
  else {
    std::cout << testConv(u8"Caféà") << "\n";
  }

  return 0;
}