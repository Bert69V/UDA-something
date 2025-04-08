FROM python:3.8

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip

RUN pip install kafka-python psycopg2-binary grpcio grpcio-tools

RUN pip install -r requirements.txt

CMD ["python", "producer.py"]
