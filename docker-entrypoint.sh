#!/bin/sh
set -e

SQLITE_FILE="${SQLITE_PATH:-/app/data/db.sqlite3}"
SQLITE_DIR="$(dirname "$SQLITE_FILE")"

echo "[preflight] Verificando diretorio do SQLite: $SQLITE_DIR"
if [ ! -d "$SQLITE_DIR" ]; then
  echo "[erro] Diretorio do SQLite nao encontrado: $SQLITE_DIR"
  exit 1
fi

if [ "${REQUIRE_SQLITE_FILE:-True}" = "True" ] && [ ! -f "$SQLITE_FILE" ]; then
  echo "[erro] Ficheiro SQLite nao encontrado em: $SQLITE_FILE"
  echo "[erro] A aplicacao nao sera iniciada sem a base de dados."
  exit 1
fi

echo "[preflight] Validando configuracao Django"
python manage.py check --deploy || python manage.py check

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
