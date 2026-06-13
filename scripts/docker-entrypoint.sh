#!/bin/bash
set -e

# Load environment variables from the appropriate .env file
if [ -f ".env.${APP_ENV}" ]; then
    echo "Loading environment from .env.${APP_ENV}"
    set -a && source ".env.${APP_ENV}" && set +a
fi

# Check required sensitive environment variables
required_vars=(
    "OPENROUTER_API_KEY"
    "POSTGRES_PASSWORD"
    "LANGFUSE_PUBLIC_KEY"
    "LANGFUSE_SECRET_KEY"
)
missing_vars=()

for var in "${required_vars[@]}"; do
    if [[ -z "${!var}" ]]; then
        missing_vars+=("$var")
    fi
done

# Check JWT key files exist
if [[ -n "$JWT_PRIVATE_KEY_PATH" ]] && [[ ! -f "$JWT_PRIVATE_KEY_PATH" ]]; then
    missing_vars+=("JWT_PRIVATE_KEY_PATH (file not found: $JWT_PRIVATE_KEY_PATH)")
fi
if [[ -n "$JWT_PUBLIC_KEY_PATH" ]] && [[ ! -f "$JWT_PUBLIC_KEY_PATH" ]]; then
    missing_vars+=("JWT_PUBLIC_KEY_PATH (file not found: $JWT_PUBLIC_KEY_PATH)")
fi

if [[ ${#missing_vars[@]} -gt 0 ]]; then
    echo ""
    echo "========================================================================"
    echo " ERROR: Missing required environment variables"
    echo "========================================================================"
    echo ""
    for var in "${missing_vars[@]}"; do
        echo "  - $var"
    done

    cat <<EOF

  ── How to Fix ──────────────────────────────────────────────────────

  Option 1: Create a .env file from the example:
    cp .env.example .env
    # Then edit .env and fill in your secrets

  Option 2: Export variables directly (for quick testing):
    export OPENROUTER_API_KEY="sk-or-v1-xxxxxxxx"
    export POSTGRES_PASSWORD="your-strong-password"
    export LANGFUSE_PUBLIC_KEY="pk-lf-xxxx"
    export LANGFUSE_SECRET_KEY="sk-lf-xxxx"

EOF

    # Additional help for JWT key file issues
    if [[ -n "$JWT_PRIVATE_KEY_PATH" ]] || [[ -n "$JWT_PUBLIC_KEY_PATH" ]]; then
        cat <<EOF
  ── JWT Key Files ───────────────────────────────────────────────────

  This project uses asymmetric RS256 JWT keys. If the key files are
  missing, generate them:
    mkdir -p security
    openssl genpkey -algorithm RSA -out security/jwt_private.pem -pkeyopt rsa_keygen_bits:2048
    openssl rsa -pubout -in security/jwt_private.pem -out security/jwt_public.pem

EOF
    fi

    cat <<EOF
  ── Docker ──────────────────────────────────────────────────────────

  For Docker, pass variables via --env-file:
    docker run --env-file .env ...

  Or use docker-compose (recommended):
    docker-compose up -d

======================================================================

EOF

    exit 1
fi

exec "$@"