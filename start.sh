#!/usr/bin/env bash
# ------------------------------------------------------------
# DEPRECATED — use `docker-compose up -d` instead.
# Langfuse is now part of the main docker-compose.yml.
# ------------------------------------------------------------

echo "⚠️  start.sh is deprecated. Use 'docker-compose up -d' instead."
echo "   See AGENTS.md for details."
exit 0

set -euo pipefail

# ----------------------- Configuration -----------------------
LANGFUSE_DIR="${HOME}/langfuse"
POSTGRES_PORT=5432
POSTGRES_CONTAINER_NAME="langfuse"

# ------------------------------------------------------------
# Helper: ensure local PostgreSQL is running
# ------------------------------------------------------------
ensure_postgres() {
    echo "🔎 Checking if PostgreSQL is reachable on port ${POSTGRES_PORT} ..."
    if pg_isready -h localhost -p "${POSTGRES_PORT}" > /dev/null 2>&1; then
        echo "✅ PostgreSQL is already running."
        return
    fi

    echo "🚀 Starting local PostgreSQL service ..."
    sudo service postgresql start || true
    sleep 5
    if ! pg_isready -h localhost -p "${POSTGRES_PORT}" > /dev/null 2>&1; then
        echo "❌ Could not start PostgreSQL. Please start it manually."
        exit 1
    fi
    echo "✅ PostgreSQL started."
}

# ------------------------------------------------------------
# Helper: start Langfuse via Docker Compose
# ------------------------------------------------------------
start_langfuse() {
    echo "🔎 Navigating to Langfuse directory ..."
    cd "${LANGFUSE_DIR}"

    echo "🔎 Pulling latest images (optional) ..."
    docker compose pull

    echo "🚀 Starting Langfuse services ..."
    docker compose up -d
    echo "✅ Langfuse started."
}

# ------------------------------------------------------------
# Graceful shutdown – stops everything on SIGINT/SIGTERM
# ------------------------------------------------------------
shutdown() {
    echo "🛑 Received stop signal – shutting down services ..."
    cd "${LANGFUSE_DIR}"
    docker compose down

    echo "👋 All services stopped. Bye!"
    exit 0
}
trap shutdown SIGINT SIGTERM

# ------------------------------------------------------------
# Main – bring everything up
# ------------------------------------------------------------
echo "=== 🚀 Starting required services ==="

ensure_postgres
start_langfuse

echo "🟢 Services are up. Press Ctrl‑C to stop."
while true; do
    sleep 60
done