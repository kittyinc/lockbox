lint:
	@ruff check $(shell git diff --diff-filter=ACM --name-only HEAD | grep '\.py$$' )

stampreqs:
	poetry export --without-hashes --format=requirements.txt > requirements.txt

test:
	pytest --cov=. --cov-report term-missing
