# ----- PROD -----
build-prod:
	@echo "generating project requirements..."
	@poetry export --without-hashes --format=requirements.txt > app/requirements.txt
	@echo "building images with compose...";
	@docker compose build

push:
	@echo "pushing images with compose...";
	@docker compose push

run-prod:
	@docker compose -f docker-compose.yml up
# ----------------

# ----- DEV ------
install:
	@sudo apt-get install pipx
	@pipx ensurepath
	@pipx install poetry==2.0.1
	@poetry install

update-deps:
	@poetry lock
	@poetry install

run-payment-processor:
	@cd payment-processor; docker compose up

build-dev:
	@echo "generating project requirements..."
	@poetry export --without-hashes --format=requirements.txt > app/requirements.txt
	@echo "building images with compose...";
	@docker compose -f docker-compose.yml -f docker-compose.dev.yml build

run-dev:
	@docker compose -f docker-compose.yml -f docker-compose.dev.yml up

run-local:
	@cd app; uwsgi --http-socket 0.0.0.0:9999 --ini uwsgi.ini
# ----------------