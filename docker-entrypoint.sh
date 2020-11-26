#!/bin/sh

echo "Waiting for DB"
while ! nc -z db 5432; do
    sleep 1
done

echo "Starting app"
exec "$@"
