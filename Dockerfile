###########
# BUILDER #
###########
FROM python:3.11 AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock /app/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

###########
## IMAGE ##
###########
FROM python:3.11-slim

WORKDIR /home/appuser/app

RUN groupadd -r appgroup && \
    useradd -r -g appgroup appuser && \
    chown -R appuser:appgroup /home/appuser/app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

COPY . /home/appuser/app

RUN chmod +x /home/appuser/app/start_app.sh

USER appuser

CMD ["sh", "./start_app.sh"]
