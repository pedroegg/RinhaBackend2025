# ----- ANY -----
build:
	@echo "generating project requirements..."
	@poetry export --without-hashes --format=requirements.txt > app/requirements.txt
	@echo "building images with compose...";
	@docker compose build
# ---------------

# ----- PROD -----
push:
	@echo "pushing images with compose...";
	@docker compose push
# ---------------

# ----- DEV -----
install:
	@sudo apt-get install pipx
	@pipx ensurepath
	@pipx install poetry==2.0.1
	@poetry install

update-deps:
	@poetry lock
	@poetry install

run:
	@cd payment-processor; docker compose up
	@docker compose --env-file app/.env -f docker-compose.yml -f docker-compose.dev.yml up
# ---------------