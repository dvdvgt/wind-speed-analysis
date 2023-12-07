.ONESHELL:

share-env:
	conda env export --from-history > environment.yml

load-env:
	conda env create -f environment.yml

clean:
	rm -Ir data