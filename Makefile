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
