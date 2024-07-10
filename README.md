## How to set up project

### Requires:

- Using python `3.6 <= python <= 3.11.4`
- Using `Virtualenv` or Python environment, etc.
  <br></br>

## The way to run project

- Step 1: `pip install poetry`
- Step 2: `poetry install`
- Step 3: `python manage.py makemigrations`
- Step 4: `python manage.py migrate`
- Step 5: `python manage.py collectstatic --noinput`
- Step 6: `uvicorn message_be.asgi:application --port 8080 --host 0.0.0.0 --reload`
- `Visit website`: Go to visit on the website api local: http://127.0.0.1:8080/docs
- `Visit admin`: Go to visit on the website Pgadmin local: http://localhost:8080/admin