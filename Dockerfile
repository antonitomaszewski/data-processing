FROM python:3.12-alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./tests /code/tests

ENV PYTHONPATH=/code
CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000", "--reload"]