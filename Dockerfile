FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x docker-entrypoint.sh

EXPOSE 8001

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["sh", "-c", "gunicorn naiprints3d.wsgi:application --bind 0.0.0.0:${PORT:-8001} --workers 3 --timeout 120 --access-logfile - --error-logfile - --capture-output --log-level info"]
