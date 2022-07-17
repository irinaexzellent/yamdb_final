FROM python:3.7-slim

WORKDIR /app

COPY ./api_yamdb/requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "yamdb_final.wsgi:application", "--bind", "0:8000" ]