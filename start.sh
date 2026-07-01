#!/bin/bash

# Ensure script exits if any background process fails or if configured role finishes.
set -e

# Print role
echo "Starting container in role: ${CONTAINER_ROLE:-web}..."

if [ "${CONTAINER_ROLE}" = "worker" ]; then
    # Run Celery Worker
    echo "Running Celery Worker..."
    exec celery -A app.core.celery_app worker --loglevel=info
else
    # Run Web server (Next.js + FastAPI + Nginx)
    
    # Start Next.js frontend
    echo "Starting Next.js frontend on port 3000..."
    cd /app/frontend
    npm run start -- -p 3000 &
    NEXT_PID=$!

    # Start FastAPI backend
    echo "Starting FastAPI backend on port 8000..."
    cd /app
    uvicorn app.main:app --host 127.0.0.1 --port 8000 &
    API_PID=$!

    # Start Nginx
    echo "Starting Nginx reverse proxy on port 80..."
    nginx -g "daemon off;" &
    NGINX_PID=$!

    # Helper function to stop all processes on signal
    cleanup() {
        echo "Stopping all processes..."
        kill -TERM "$NEXT_PID" "$API_PID" "$NGINX_PID" 2>/dev/null
        exit 0
    }
    trap cleanup SIGINT SIGTERM

    # Monitor processes
    while true; do
        if ! kill -0 "$NEXT_PID" 2>/dev/null; then
            echo "Next.js frontend process died."
            exit 1
        fi
        if ! kill -0 "$API_PID" 2>/dev/null; then
            echo "FastAPI backend process died."
            exit 1
        fi
        if ! kill -0 "$NGINX_PID" 2>/dev/null; then
            echo "Nginx process died."
            exit 1
        fi
        sleep 2
    done
fi
