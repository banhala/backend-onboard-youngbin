POETRY = poetry run

run:
	$(POETRY) python manage.py runserver 0.0.0.0:8000

migrate:
	$(POETRY) python manage.py migrate

format:
	$(POETRY) isort .
	$(POETRY) black .

lint:
	$(POETRY) flake8 .

test:
	$(POETRY) pytest -q

hook:
	$(POETRY) pre-commit run --all-files

up:
	docker compose up --build

down:
	docker compose down
