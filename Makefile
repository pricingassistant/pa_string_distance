PWD=$(pwd)

clean:
	python setup.py clean
	rm -rf *.so *.o *.html pa_string_distance.c

build: clean
	venv/bin/cython -a pa_string_distance.pyx -I.
	python setup.py build
	cp build/lib*/*.so ./

test: build
	venv/bin/pytest test.py --profile

virtualenv:
	rm -rf venv
	virtualenv --python=python2.7 venv
	venv/bin/pip install -r requirements.txt
