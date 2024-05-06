all: dir scraper compare

dir:
	-mkdir data

scraper:
	python3 conservative_fundraiser.py
