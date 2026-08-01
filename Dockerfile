FROM python:3.12-slim AS builder

ENV POETRY_VERSION=2.1.3 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PIP_NO_CACHE_DIR=1

RUN pip install "poetry==${POETRY_VERSION}"

WORKDIR /build
COPY pyproject.toml poetry.lock README.md ./
COPY src ./src
RUN poetry install --only main --no-ansi


FROM python:3.12-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    APP_VERSION=0.2.0 \
    PORT=8080

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn

EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "--workers", "2", "--access-logfile", "-", "simpleapp.app:app"]
