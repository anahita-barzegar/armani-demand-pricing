# ==============================
#  Armani Middle East Trading
#  Data Science Assessment
# ==============================

.PHONY: help up down restart logs db-shell pgadmin clean ps rebuild init-db

GREEN  := \033[0;32m
YELLOW := \033[0;33m
NC     := \033[0m

help: ## Show this help
	@echo ""
	@echo "Available commands:"
	@echo "  make up          → Start all services (PostgreSQL 18 + pgAdmin)"
	@echo "  make down        → Stop all services"
	@echo "  make restart     → Restart services"
	@echo "  make logs        → Follow logs"
	@echo "  make ps          → Show container status"
	@echo "  make db-shell    → Open PostgreSQL shell"
	@echo "  make pgadmin     → Show pgAdmin login info"
	@echo "  make init-db     → Re-run init.sql"
	@echo "  make clean       → Remove containers + volumes (DATA LOSS)"
	@echo "  make rebuild     → Rebuild and restart"
	@echo ""

up: ## Start services
	@echo "$(GREEN)Starting services (PostgreSQL 18 + pgAdmin)...$(NC)"
	docker compose up -d
	@echo "$(GREEN)Services are up!$(NC)"
	@echo "PostgreSQL → localhost:5432"
	@echo "pgAdmin    → http://localhost:5050"

down: ## Stop services
	@echo "$(YELLOW)Stopping services...$(NC)"
	docker compose down

restart: ## Restart services
	@echo "$(YELLOW)Restarting services...$(NC)"
	docker compose down
	docker compose up -d

logs: ## Show logs
	docker compose logs -f

ps: ## Container status
	docker compose ps

db-shell: ## Open psql shell
	docker compose exec db psql -U armani -d armani_trading

pgadmin: ## Show pgAdmin credentials
	@echo ""
	@echo "pgAdmin URL : http://localhost:5050"
	@echo "Email       : admin@armani.com"
	@echo "Password    : admin123"
	@echo ""

init-db: ## Run init.sql again
	docker compose exec db psql -U armani -d armani_trading -f /docker-entrypoint-initdb.d/init.sql

clean: ## Remove everything (including data)
	@echo "$(YELLOW)Removing containers and volumes...$(NC)"
	docker compose down -v
	@echo "$(GREEN)Cleaned.$(NC)"

rebuild: ## Rebuild from scratch
	docker compose down
	docker compose build --no-cache
	docker compose up -d
