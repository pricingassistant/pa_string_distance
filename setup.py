from distutils.core import setup
from distutils.extension import Extension
import os

if os.path.isfile("pa_string_distance.c"):

    ext_modules = [
        Extension(
            "pa_string_distance",
            ["pa_string_distance.c", "jaro.c"]
        )
    ]

else:

    from Cython.Build import cythonize

    ext_modules = cythonize([
        Extension(
            "pa_string_distance",
            ["pa_string_distance.pyx", "jaro.c"],
            include_dirs=[os.path.abspath("./")]
        )
    ])


setup(
    name="pa_string_distance",
    version="0.1",
    ext_modules=ext_modules
)
