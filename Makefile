.ONESHELL:

share-env:
	conda env export --from-history > environment.yml
	pip list --format=freeze > requirements.txt

load-env:
	conda env create -f environment.yml
	pip install -r requirements.txt

clean:
	rm -Ir data
