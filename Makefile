all: build

build:
	python compile.py "./tests/assign_lhs_stack2.py"

zip:
	mkdir zipfolder
	cp *.py zipfolder
	cp tests/* zipfolder
	#zip hw.zip zipfolder/*
	#rm -rf zipfolder

clean:
	rm *.pyc
	find . -name "*.s" -type f -delete
	find . -name "*~" -type f -delete
	find . -name "*.exe" -type f -delete
