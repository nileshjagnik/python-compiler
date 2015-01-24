all: build

build:
	python compile.py "./tests/test1.py"

clean:
	rm *.pyc
	find . -name "*.s" -type f -delete
	find . -name "*~" -type f -delete
