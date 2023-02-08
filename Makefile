lint:
	poetry run pre-commit install && poetry run pre-commit run -a -v

update-precommit:
	poetry run pre-commit autoupdate

test:
	poetry run pytest -sx
