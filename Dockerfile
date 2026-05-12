FROM python:alpine

WORKDIR /app

# dependencies
COPY ./pyproject.toml .
RUN pip install .

# app
COPY ./app app

# entrypoint script
COPY ./docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]