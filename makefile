# Nom du projet
PROJECT_NAME=carburant_etl

# Commandes Docker
up:
	docker-compose up --build -d

down:
	docker-compose down -v

restart: down up

logs:
	docker-compose logs --follow

ps:
	docker-compose ps

bash-airflow:
	docker exec -it airflow-webserver bash

bash-postgres:
	docker exec -it postgres bash

# Tests unitaires (si tu ajoutes pytest)
# test:
# 	pytest tests/

# Nettoyage local
clean:
	rm -rf airflow/data/*.csv airflow/data/*.xml

# Reset Airflow
reset-airflow:
	rm -rf airflow/logs airflow/data airflow/plugins
	mkdir -p airflow/data airflow/logs airflow/plugins
	docker-compose down -v
	docker-compose up --build

