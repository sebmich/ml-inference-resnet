FROM python:3.12-slim

WORKDIR /app

COPY dispatcher/dispatcher.py /app/dispatcher.py
COPY requirements.txt /app/requirements.txt
COPY load_tester/images /app/images

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install prometheus_fastapi_instrumentator

CMD ["python", "dispatcher.py"]

