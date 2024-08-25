FROM arm64v8/python:3.11-slim

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY ./ ./code

WORKDIR /code

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "--reload", "app.main:app"]

EXPOSE 8000