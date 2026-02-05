# =====================================================
# Justfile Settings
# =====================================================
# Load environment variables from .env file into justfile context
# This allows justfile recipes to reference variables using ${VAR_NAME} syntax
set dotenv-load := true

# Export all loaded environment variables to child processes
# This makes variables available to all commands executed within recipes
# (e.g., docker compose, shell scripts, and other external tools)
set export := true


# =====================================================
# Environment Setup
# =====================================================
# Create local environment configuration file from template
# Copy .env.example to .env for initial project setup
# After copying, edit .env file to set your specific configuration values
copy-env:
    cp .env.example .env


# =====================================================  
# Redis ACL & Permissions Management  
# =====================================================  
# Make Redis ACL generation script executable  
# Grants execute permissions to the script that dynamically creates Redis user ACL rules  
make-x:  
    chmod +x app/initialization/generate-redis-acl.sh

# Generate Redis ACL configuration file  
# Executes the ACL script to produce 01-create-users.acl based on current .env settings  
# Output file will be mounted into the Redis container for authentication and access control  
gen-acl:  
    ./app/initialization/generate-redis-acl.sh


# =====================================================
# Redis Docker Compose Management
# =====================================================
# Start local Redis server in detached mode
redis-up:  
    docker compose --env-file .env up -d  

# Stop and remove Redis container
redis-down:
    docker compose --env-file .env down

# =====================================================
# Redis Interactive Shell Access (Celery Redis)
# =====================================================
# !!! For development convenience only — using .env file password variables directly in CLI commands !!!
# This approach exposes secrets in process lists and command history; never use in production

# Launch Redis CLI for Celery Redis based on user type
# Usage: just redis-shell [admin]
#   admin: Optional flag to connect as superuser instead of application user

redis-shell user="app":
    #!/usr/bin/env bash
    if [ "{{ user }}" = "admin" ]; then
        # Launch Redis CLI as admin user with full privileges
        docker compose \
            --env-file .env \
            exec redis-client \
            redis-cli \
                --user "$REDIS_ADMIN_USERNAME" \
                --pass "$REDIS_ADMIN_PASSWORD" \
                -h redis-server \
                -p "$CELERY_REDIS_INTERNAL_PORT"
    else
        # Launch Redis CLI as application user
        docker compose \
            --env-file .env \
            exec redis-client \
            redis-cli \
                --user "$CELERY_REDIS_USERNAME" \
                --pass "$CELERY_REDIS_PASSWORD" \
                -h redis-server \
                -p "$CELERY_REDIS_INTERNAL_PORT"
    fi