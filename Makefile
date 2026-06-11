PYTHONPATH_APP=PYTHONPATH=app/backend
VENV_PY=.venv/bin/python

.PHONY: install-backend test lint docs migrate seed up demo

install-backend:
	python3 -m venv .venv
	$(VENV_PY) -m pip install --upgrade pip
	$(VENV_PY) -m pip install -r app/backend/requirements.txt

test:
	$(PYTHONPATH_APP) $(VENV_PY) -m pytest tests
	$(PYTHONPATH_APP) $(VENV_PY) -m pytest app/backend/tests

lint:
	npx markdownlint-cli2 "**/*.md"
	$(VENV_PY) -m py_compile app/backend/app/*.py app/backend/app/api/*.py app/backend/app/providers/*.py app/backend/app/services/*.py scripts/*.py

docs:
	$(VENV_PY) -m mkdocs build

migrate:
	$(PYTHONPATH_APP) $(VENV_PY) -m alembic upgrade head

seed:
	$(PYTHONPATH_APP) $(VENV_PY) -m app.seed

up:
	docker compose up --build

demo:
	docker compose up --build -d
	docker compose run --rm backend python -m app.backend.app.seed
