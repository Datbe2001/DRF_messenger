## How to set up project

### Requires:

- Using python `3.6 <= python <= 3.11.4`
- Install [Docker](https://docs.docker.com/get-docker/).
- Using `Virtualenv` or Python environment, etc.
  <br></br>
- `Step 1`: Run Database

```commandline
cd database/
docker-compose up --build -d
```

- `Step 2`: Go to visit on the website Pgadmin local (http://localhost:8080)

## The way to run project

- Step 1: pip install poetry
- Step 2: poetry install
- Step 3: `python manage.py makemigrations`
- Step 4: `python manage.py migrate`
- Step 5: `python manage.py runserver`
- Step 5: `python manage.py start_consumer`
- Step 6: Go to visit on the website api -> http://127.0.0.1:8000/