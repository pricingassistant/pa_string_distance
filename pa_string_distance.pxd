
cdef extern from "jaro.h":
	extern double jaro_winkler(const Py_UNICODE *str1, int len1, const Py_UNICODE *str2, int len2, int long_tolerance);
