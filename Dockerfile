FROM python:3.13-slim

WORKDIR /api

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./api .

RUN mkdir -p /api/data
RUN echo "{}" > /api/data/tokens.json
RUN echo "[]" > /api/data/alerts.json

CMD ["python", "main.py"]