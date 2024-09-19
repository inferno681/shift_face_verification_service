FROM python:3.12-slim

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    libgl1-mesa-glx \
    libglib2.0-dev

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false

RUN poetry install --only main --no-interaction --no-ansi

COPY ./src  ./src

ENV PYTHONPATH=/app/src/

CMD ["python", "src/app/main.py"]
