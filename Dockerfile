# Dockerfile for The Digital Saathi (FastAPI backend + Next.js frontend)
# Supports running as web server (with Nginx) or celery worker.

# Define build arguments
ARG SOURCE_TYPE=local
ARG NEXT_PUBLIC_API_URL=/api/v1

# ==============================================================================
# STAGE: source-git (Clones the repository)
# ==============================================================================
FROM python:3.11-slim AS source-git
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone https://github.com/digitalsaathi12/promptgen.git .

# ==============================================================================
# STAGE: source-local (Uses local build context)
# ==============================================================================
FROM python:3.11-slim AS source-local
WORKDIR /src
COPY . .

# ==============================================================================
# STAGE: source (Determined by SOURCE_TYPE argument)
# ==============================================================================
FROM source-${SOURCE_TYPE} AS source

# ==============================================================================
# STAGE: frontend-builder (Builds the Next.js Frontend)
# ==============================================================================
FROM node:20-slim AS frontend-builder
WORKDIR /app

# Copy dependency configuration and install
COPY --from=source /src/frontend/package*.json ./
RUN npm ci --legacy-peer-deps

# Copy frontend source files
COPY --from=source /src/frontend/ ./

# Pass API URL at build-time (crucial for client-side API requests)
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# Build the Next.js production bundle
RUN npm run build

# ==============================================================================
# STAGE: backend-builder (Compiles Python dependencies to wheels)
# ==============================================================================
FROM python:3.11-slim AS backend-builder
WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Generate python dependency wheels
COPY --from=source /src/requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements.txt

# ==============================================================================
# STAGE: final (Production Runtime Environment)
# ==============================================================================
FROM python:3.11-slim AS final

# Configure environment
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    CONTAINER_ROLE=web \
    PORT=80

# Install Nginx, Node.js, and curl
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    nginx \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy Python wheels and install dependencies
COPY --from=backend-builder /build/wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/* && rm -rf /wheels

# Copy backend files from source
COPY --from=source /src/app /app/app
COPY --from=source /src/static /app/static
COPY --from=source /src/alembic.ini /app/alembic.ini
COPY --from=source /src/requirements.txt /app/requirements.txt

# Copy Next.js frontend code (with dependencies and production build)
COPY --from=frontend-builder /app /app/frontend

# Copy Nginx server configuration
COPY --from=source /src/nginx.conf /etc/nginx/sites-available/default

# Copy startup orchestration script
COPY --from=source /src/start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose HTTP port
EXPOSE 80

# Run entrypoint script
CMD ["/app/start.sh"]
