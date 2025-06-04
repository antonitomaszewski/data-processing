# data-processing

alterdata.io

## Uruchamianie

```bash
git clone git@github.com:antonitomaszewski/data-processing.git
cd data-processing
docker compose build
docker compose up -d
```

* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* pgAdmin: [http://localhost:5052/browser/](http://localhost:5052/browser/)

## Architektura

* FastAPI
* Pydantic
* PostgreSQL
* SQLAlchemy
* Docker

## Funkcjonalności

* Podstawowe operacje na transakcjach
* Schemat bazy: jedna tabela `Transactions` z 8 kolumnami (w tym własne `id` oraz `transaction_id`)

## Struktura projektu

Kod w folderze `app` podzielony na moduły: `models`, `schemas`, `services`, `routes`

## Testowanie

```bash
docker compose exec app sh
pytest tests/ --cov=app --cov-report=term-missing
```

## Kompromisy

* Pominięcie bonusowych zadań

