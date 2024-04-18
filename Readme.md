## Project start up:
### git clone git@github.com:Nikolaev3Artem/meduzzen-internature.git
### cd meduzzen-internature

### Create your own .env file using .env.example for example
### docker-compose up -d --build

## Migrations:
## If you don`t use docker:
### alembic upgrade head - To apply all migrations
### alembic downgrade -1 - Downgrade to previous migration
## If you use docker migrations applies in app/entrypoint.sh, but you can manage it manually:
### docker-compose exec api alembic upgrade head
### docker-compose exec api alembic downgrade base

## Testing app:
### docker-compose -f docker-compose-test.yml up -d --build
### pytest tests/

## Docs:
### http://localhost/docs/ or http://127.0.0.1/docs/
