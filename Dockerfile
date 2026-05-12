FROM python:alpine

WORKDIR /app

COPY ./pyproject.toml .

RUN pip install .

COPY ./app .

CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "80"]