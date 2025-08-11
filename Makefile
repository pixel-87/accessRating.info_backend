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
	cd backend && flake8 --exclude venv,migrations apps/
	cd backend && isort --check --line-length 79 apps/

format: ## Format code
	cd backend && black --line-length 79 apps/
	cd backend && isort --line-length 79 apps/

clean: ## Clean up cache files
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +

check: test lint ## Run tests and linting

build: ## Build for production
	docker-compose -f docker/docker-compose.prod.yml build

deploy: ## Deploy to production
	./scripts/deploy.sh

# Production Commands
prod-up: ## Start production services
	docker-compose -f docker/docker-compose.prod.yml up -d

prod-down: ## Stop production services
	docker-compose -f docker/docker-compose.prod.yml down

prod-logs: ## View production logs
	docker-compose -f docker/docker-compose.prod.yml logs -f

prod-restart: ## Restart production services
	docker-compose -f docker/docker-compose.prod.yml restart

prod-migrate: ## Run migrations in production
	docker-compose -f docker/docker-compose.prod.yml run --rm web python manage.py migrate --settings=accessibility_api.prod_settings

prod-shell: ## Access Django shell in production
	docker-compose -f docker/docker-compose.prod.yml run --rm web python manage.py shell --settings=accessibility_api.prod_settings

prod-collectstatic: ## Collect static files in production
	docker-compose -f docker/docker-compose.prod.yml run --rm web python manage.py collectstatic --noinput --settings=accessibility_api.prod_settings
