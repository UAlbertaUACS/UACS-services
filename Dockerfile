# syntax=docker/dockerfile:1
FROM python:3.10-slim

WORKDIR /backend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# infinite while loop

CMD ["uvicorn", "app.main:app", "--port", "8000", "--host", "0.0.0.0"]