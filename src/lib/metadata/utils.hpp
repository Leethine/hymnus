#pragma once

#ifndef METADATA_UTILS_HPP
#define METADATA_UTILS_HPP

#include <string>

#define ERROR_MALLOC       1
#define ERROR_ICONV_OPEN   2
#define ERROR_INVALID_CHAR 3

namespace hymnus {
namespace utils {

std::string sha1hash(const std::string&);

int iconv_utf8_to_ascii(const std::string&, std::string&);

} // namespace utils
} // namespace hymnus

#endif