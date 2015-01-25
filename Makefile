all: build

build:
	python compile.py "./tests/pandaPANDAlargeTest.py"

clean:
	rm *.pyc
	find . -name "*.s" -type f -delete
	find . -name "*~" -type f -delete
	find . -name "*.exe" -type f -delete
