PYTHONPATH_APP=PYTHONPATH=app/backend
VENV_PY=.venv/bin/python

.PHONY: install-backend test lint docs migrate seed up demo turnkey-demo verify-demo agent-self-check verify-repo-surface

install-backend:
	python3 -m venv .venv
	$(VENV_PY) -m pip install --upgrade pip
	$(VENV_PY) -m pip install -r app/backend/requirements.txt

test:
	$(VENV_PY) -m pytest tests
	$(PYTHONPATH_APP) $(VENV_PY) -m pytest app/backend/tests

lint:
	npx markdownlint-cli2 "**/*.md"
	$(VENV_PY) -m py_compile app/backend/app/*.py app/backend/app/api/*.py app/backend/app/providers/*.py app/backend/app/services/*.py scripts/*.py

docs:
	$(VENV_PY) -m mkdocs build

migrate:
	$(PYTHONPATH_APP) $(VENV_PY) -m alembic upgrade head

seed:
	$(VENV_PY) -m app.backend.app.seed

up:
	docker compose up --build

demo:
	docker compose up --build -d
	docker compose run --rm backend python -m app.backend.app.seed

turnkey-demo:
	docker compose up --build -d
	docker compose run --rm backend python -m alembic upgrade head
	docker compose run --rm backend python -m app.backend.app.seed
	@echo "Frontend: http://localhost:3000"
	@echo "API docs: http://localhost:8000/docs"
	@echo "Demo login: demo@example.com / DemoPlatform123"

verify-demo:
	$(PYTHONPATH_APP) $(VENV_PY) scripts/verify_demo.py

agent-self-check:
	$(VENV_PY) scripts/agent_self_check.py

verify-repo-surface:
	$(VENV_PY) scripts/version_consistency_check.py
	$(VENV_PY) -m pytest tests
	$(PYTHONPATH_APP) $(VENV_PY) -m pytest app/backend/tests
