start:
	docker-compose up -d

stop:
	docker-compose down

dev:
	docker-compose up

destroy:
	docker-compose down --volumes

init:
	./bin/init.sh

build:
	./bin/build-custom-airflow.sh

clean:
	docker builder prune --all

db_conn:
	airflow connections add 'my_prod_db' --conn-uri 'mssql://sa:Iamnotsecure4sure@host:port/TEST_DB'
