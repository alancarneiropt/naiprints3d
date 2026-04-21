#!/bin/sh
set -e

SQLITE_FILE="${SQLITE_PATH:-/app/media/db.sqlite3}"
SQLITE_DIR="$(dirname "$SQLITE_FILE")"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

fail() {
  log "ERRO: $1"
  exit 1
}

run_step() {
  DESCRIPTION="$1"
  shift
  log "INICIO: $DESCRIPTION"
  if "$@"; then
    log "OK: $DESCRIPTION"
  else
    fail "$DESCRIPTION"
  fi
}

log "BOOT: Iniciando preflight do container"
log "CONFIG: PORT=${PORT:-8001} | SQLITE_PATH=$SQLITE_FILE | REQUIRE_SQLITE_FILE=${REQUIRE_SQLITE_FILE:-True}"

run_step "Verificar diretorio do SQLite ($SQLITE_DIR)" test -d "$SQLITE_DIR"

if [ ! -d "$SQLITE_DIR" ]; then
  log "DEBUG: Conteudo de /app:"
  ls -la /app || true
fi

if [ "${REQUIRE_SQLITE_FILE:-True}" = "True" ]; then
  run_step "Verificar ficheiro SQLite ($SQLITE_FILE)" test -f "$SQLITE_FILE"
else
  log "AVISO: REQUIRE_SQLITE_FILE=False, o sistema pode criar novo ficheiro SQLite."
fi

run_step "Verificar permissao de escrita em /app/media" test -w /app/media
run_step "Verificar configuracao Django (check --deploy)" sh -c "python manage.py check --deploy || python manage.py check"
run_step "Aplicar migracoes" python manage.py migrate --noinput
run_step "Coletar ficheiros estaticos" python manage.py collectstatic --noinput
run_step "Healthcheck interno (/healthz logico)" python manage.py shell -c "import os; from django.conf import settings; assert os.path.isfile(settings.SQLITE_PATH), 'sqlite_missing'; assert os.access(settings.MEDIA_ROOT, os.W_OK), 'media_not_writable'; print('health_preflight_ok')"

log "BOOT: Preflight concluido. Subindo aplicacao..."
exec "$@"
