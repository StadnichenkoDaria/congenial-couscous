FROM python:3.12

WORKDIR /code

COPY ./pyproject.toml /code/pyproject.toml

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-ansi --no-cache

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "localhost", "--port", "80"]
