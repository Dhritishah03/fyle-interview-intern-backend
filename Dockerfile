# Use an official Python image as the base image
FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV FLASK_APP=core/server.py

EXPOSE 5000

RUN rm -f core/store.sqlite3
RUN flask db upgrade -d core/migrations/

RUN chmod +x run.sh

ENTRYPOINT ["bash", "run.sh"]
