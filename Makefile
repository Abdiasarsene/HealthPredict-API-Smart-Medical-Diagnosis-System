# Nom du projet (juste informatif)
PROJECT_NAME=HealthPredict

# Lancer tous les tests avec pytest
test:
	pytest -v test/

# Lancer les tests avec couverture
coverage:
	pytest --cov=src --cov-report=term-missing test/

# Formatter le code avec black
format:
	black src test

# Linter le code avec ruff
lint:
	ruff check src test

# Démarrer l'API localement (assume que main.py est à la racine)
run:
	uvicorn main:app --reload --port 8000

# Supprimer les fichiers __pycache__ et .pytest_cache
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +; rm -rf .pytest_cache .coverage

# Tout tester + lint + format (pipeline local)
ci:
	make format && make lint && make coverage
