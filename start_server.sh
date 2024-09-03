#!/bin/bash

CORES=$(nproc)
WORKERS_PER_CORE=${WORKERS_PER_CORE:-1}
WORKERS=$(($WORKERS_PER_CORE * $CORES))
USE_LOGLEVEL=${LOG_LEVEL:-"info"}

echo "WORKERS_PER_CORE: ${WORKERS_PER_CORE}"
echo "CORES: ${CORES}"
echo "WORKERS: ${WORKERS}"

exec gunicorn -w $WORKERS -b 0.0.0.0:8000 --max-requests 1000 --max-requests-jitter 50 -k uvicorn.workers.UvicornWorker main:app --log-level $USE_LOGLEVEL

