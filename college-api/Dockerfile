FROM python:3.11

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ /app/

EXPOSE 8000
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
