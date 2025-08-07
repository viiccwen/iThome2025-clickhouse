.PHONY: setup up down init produce query

setup:
	@echo "Setting up ClickHouse..."
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

up:
	@echo "Starting containers..."
	docker compose up -d

down:
	@echo "Stopping and removing containers..."
	docker compose down -v

init:
	@echo "Initializing ClickHouse..."
	docker exec -it clickhouse clickhouse-client --user=default --password=default --queries-file=/etc/clickhouse-server/create_tables.sql
	@echo "Initializing Successfully"

produce:
	@echo "Producing data to Kafka..."
	python kafka_producer.py

query:
	@echo "Querying ClickHouse..."
	python clickhouse_query.py