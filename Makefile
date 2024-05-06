all: dir scraper

dir:
	-mkdir data

scraper:
	python3 conservative_fundraiser.py
