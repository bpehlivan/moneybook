#!/bin/bash
# entrypoint.sh
# this file should be executable before building container image
# chmod +x entrypoint.sh

set -e

host="db"
port=5432
user="postgres"

POSTGRES_PASSWORD=""

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -p $port -U "postgres" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
psql -h $host -p $port -U $user -c "CREATE DATABASE moneybook;" || echo "Database already exists..."

echo "Applying migrations..."
python manage.py migrate

echo "Applying command..."
shift
cmd="$@"
exec $cmd
