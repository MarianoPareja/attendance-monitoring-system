FROM python:3.11

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential \ 
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app 
COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app

EXPOSE 8001

CMD ["python3", "src/main.py"]