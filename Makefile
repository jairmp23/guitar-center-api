DOCKER_COMPOSE = docker-compose
ALEMBIC = $(DOCKER_COMPOSE) run --rm app alembic

.PHONY: build
build:
	$(DOCKER_COMPOSE) up --build -d

.PHONY: clean
clean:
	$(DOCKER_COMPOSE) down -v

.PHONY: restart
restart: clean start

.PHONY: start
start:
	$(DOCKER_COMPOSE) up -d

.PHONY: stop
stop:
	$(DOCKER_COMPOSE) down
