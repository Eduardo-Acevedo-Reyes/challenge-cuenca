.PHONY: help install test run down clean

help:
	@echo "make install  => Instala dependencias"
	@echo "make run      => Ejecuta el servidor y servicios en Docker"
	@echo "make test     => Ejecuta las pruebas"
	@echo "make down     => Detiene contenedores Docker"
	@echo "make clean    => Elimina contenedores e imágenes"

install:
	pip install -r requirements.txt

test:
	pytest tests/

run:
	docker-compose up --build

down:
	docker-compose down

clean:
	docker-compose down -v --remove-orphans
