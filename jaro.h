#ifndef _JELLYFISH_H_
#define _JELLYFISH_H_

#include <stdlib.h>
#include <Python.h>

double jaro_winkler(const Py_UNICODE *str1, int len1, const Py_UNICODE *str2, int len2, int long_tolerance);

#endif