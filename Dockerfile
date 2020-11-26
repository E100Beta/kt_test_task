FROM python:3.8-slim

EXPOSE 8000
ENV PYTHONOPTIMIZE 2

# to wait on DB
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*
COPY ./docker-entrypoint.sh /

COPY ./requirements.txt /
RUN pip install -U pip && pip install -r /requirements.txt

WORKDIR /usr/src/app
COPY . .

ENTRYPOINT ["/docker-entrypoint.sh"]

# Create (check for) db schema and start server
CMD python init_db.py && /usr/bin/env gunicorn "$APP_MODULE" -b 0.0.0.0:8000 --worker-class aiohttp.GunicornUVLoopWebWorker -w $(nproc)
