FROM python:3.9

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

RUN apt-get update
RUN apt-get install vim -y
RUN apt-get install postgresql-client -y

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

