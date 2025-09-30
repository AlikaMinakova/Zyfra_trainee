FROM python:3.9-slim

RUN mkdir /app

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc=4:14.2.0-1 \
    libpq-dev=17.5-1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app

RUN pip install -r /app/requirements.txt --no-cache-dir

COPY . .

CMD ["python", "manage.py", "runserver", "0:8000"]