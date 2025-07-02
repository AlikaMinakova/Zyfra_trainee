FROM python:3.9-slim

RUN mkdir /app

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app

RUN pip install -r /app/requirements.txt --no-cache-dir

COPY . .

CMD ["python", "manage.py", "runserver", "0:8000"]
