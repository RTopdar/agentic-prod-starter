.PHONY: help install dev docker-up docker-down test lint format clean logs psql generate-jwt-keys

help:           ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:        ## Install all dependencies (main + dev + test)
	uv sync
	uv sync --group dev
	uv sync --group test

dev:            ## Start the FastAPI dev server with hot-reload
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

docker-up:      ## Start all services (db, app, prometheus, grafana, cadvisor)
	docker-compose up -d

docker-down:    ## Stop and remove all containers
	docker-compose down

docker-logs:    ## Tail logs from all services
	docker-compose logs -f

test:           ## Run all tests
	pytest

lint:           ## Run ruff linter check
	ruff check app/

format:         ## Format code with ruff
	ruff format app/

check:          ## Run linter + formatter check (CI gate)
	ruff check app/ && ruff format --check app/

generate-jwt-keys:  ## Generate RS256 JWT key pair for auth
	mkdir -p security
	openssl genpkey -algorithm RSA -out security/jwt_private.pem -pkeyopt rsa_keygen_bits:2048
	openssl rsa -pubout -in security/jwt_private.pem -out security/jwt_public.pem
	chmod 600 security/jwt_private.pem
	@echo "Generated: security/jwt_private.pem, security/jwt_public.pem"

clean:          ## Remove Python cache and artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .ruff_cache .pytest_cache

psql:           ## Connect to the PostgreSQL database
	@read -p "User: " u; read -p "Database: " d; \
		PGPASSWORD=$$(grep POSTGRES_PASSWORD .env.dev | cut -d= -f2) \
		psql -h localhost -U $$u -d $$d