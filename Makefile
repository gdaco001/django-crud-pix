lint:
	poetry run pre-commit install && poetry run pre-commit run -a -v

update-precommit:
	poetry run pre-commit autoupdate

test:
	poetry run pytest -sx

add-random-data-to-db-in-docker:
	docker compose --env-file .dev.env -f pix_api/composes/pix-api-dev/docker-compose.yml run --rm api python manage.py generate_data $(amount)

# Run like this: make add-random-data-to-db amount=30
add-random-data-to-db:
	python pix_api/manage.py generate_data $(amount)

add-default-data-to-db:
	python pix_api/manage.py loaddata data.json

build-api:
	docker build -f Dockerfile -t pix_api:1.0 .

deploy-api:
	docker compose --env-file .dev.env -f pix_api/composes/pix-api-dev/docker-compose.yml up -d

shutdown-api:
	docker compose --env-file .dev.env -f pix_api/composes/pix-api-dev/docker-compose.yml down
