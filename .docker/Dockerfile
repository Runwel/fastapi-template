FROM python:3.10-slim-bullseye
LABEL Boiler Plate

# Install necessary dependencies including Tesseract
RUN apt-get update \
    && apt-get -y install libpq-dev gcc curl procps net-tools tini \
    && apt-get -y install tesseract-ocr \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install gunicorn

# Install Poetry
ENV POETRY_HOME=/tmp/poetry
RUN curl -sSL https://install.python-poetry.org/ | python3 -
ENV PATH=$POETRY_HOME/bin:$PATH
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app
COPY . /app

# Install Python dependencies using Poetry
RUN poetry config virtualenvs.create false \
  && poetry install --only main

# Expose port for FastAPI
EXPOSE 8000
