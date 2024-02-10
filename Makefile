lint:
	@flake8 --config=.flake8 /dev/null $(shell git diff --name-only HEAD | grep '\.py$$' )

stampreqs:
	poetry export --without-hashes --format=requirements.txt > requirements.txt

test:
	pytest --cov=. --cov-report term-missing

testcap:
	pytest --cov=. --cov-report term-missing -s