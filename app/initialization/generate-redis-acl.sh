#!/bin/bash

# =====================================================
# Strict Mode Flags:
#   -e: Exit immediately if any command exits with non-zero status
#   -u: Treat unset variables as an error
# =====================================================
set -eu

# Load .env file
if [[ -f .env ]]; then
    source .env
else
    echo "Error: .env file not found."
    exit 1
fi

# Generate ACL file using environment variables
cat > app/initialization/01-create-users.acl << EOF
user ${REDIS_ADMIN_USERNAME} on >${REDIS_ADMIN_PASSWORD} ~* &* +@all
user ${CELERY_REDIS_USERNAME} on >${CELERY_REDIS_PASSWORD} ~* &* +@all -@dangerous -@admin
user default off nopass
EOF