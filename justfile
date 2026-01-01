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
# Docker Compose: Redis Server Initialization  
# =====================================================  
# Start local Redis server in detached mode
redis-up:  
    docker compose -f docker-compose.yml --env-file .env up -d  

# !!! For development convenience only — using .env file password variables directly in CLI commands !!!  
# This approach exposes secrets in process lists and shell history; never use in production environments  

# Launch Redis CLI as application user
redis-shell:
    docker compose \
        -f docker-compose.yml \
        --env-file .env \
        exec redis-client \
        redis-cli \
            --user "$CELERY_REDIS_USERNAME" \
            --pass "$CELERY_REDIS_PASSWORD" \
            -h redis-server \
            -p "$CELERY_REDIS_INTERNAL_PORT"

# Launch Redis CLI as admin user with full privileges
redis-shell-admin:
    docker compose \
        -f docker-compose.yml \
        --env-file .env \
        exec redis-client \
        redis-cli \
            --user "$REDIS_ADMIN_USERNAME" \
            --pass "$REDIS_ADMIN_PASSWORD" \
            -h redis-server \
            -p "$CELERY_REDIS_INTERNAL_PORT"

# Stop and remove Redis container
redis-down:
    docker compose -f docker-compose.yml --env-file .env down