runserver:
	docker-compose up

runlocal:
	docker-compose up -d postgres
	uvicorn main:app --host 0.0.0.0 --port 9000

test:
	docker-compose run --rm web-server pytest

migrate:
	docker-compose run --rm web-server alembic -c src/alembic.ini upgrade head

rollback_migrations:
	docker-compose run --rm web-server alembic -c src/alembic.ini downgrade -1