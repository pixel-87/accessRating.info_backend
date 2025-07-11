.PHONY: help install test run migrate clean lint format

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	cd backend && pip install -r requirements.txt

install-dev: ## Install development dependencies
	cd backend && pip install -r requirements.txt
	cd backend && pip install pytest-cov black flake8 isort

test: ## Run all tests
	cd backend && python -m pytest

test-django: ## Run Django tests (alternative method)
	cd backend && python manage.py test --settings=accessibility_api.test_settings

test-cov: ## Run tests with coverage
	cd backend && python -m pytest --cov=apps --cov-report=html --cov-report=term

run: ## Run development server
	cd backend && python manage.py runserver

migrate: ## Run database migrations
	cd backend && python manage.py migrate

makemigrations: ## Create new migrations
	cd backend && python manage.py makemigrations

superuser: ## Create superuser
	cd backend && python manage.py createsuperuser

shell: ## Open Django shell
	cd backend && python manage.py shell

db-up: ## Start PostgreSQL database
	docker-compose up -d

db-down: ## Stop PostgreSQL database
	docker-compose down

db-reset: ## Reset database (WARNING: destroys all data)
	docker-compose down -v
	docker-compose up -d
	sleep 5
	cd backend && python manage.py migrate

lint: ## Run linting
	cd backend && flake8 apps/
	cd backend && isort --check-diff apps/

format: ## Format code
	cd backend && black apps/
	cd backend && isort apps/

clean: ## Clean up cache files
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +

check: test lint ## Run tests and linting

build: ## Build for production (placeholder)
	@echo "Production build not implemented yet"

deploy: ## Deploy to production (placeholder) 
	@echo "Production deployment not implemented yet"
