# **Redis ACL Configuration for Celery**

This section defines a role-based access control (RBAC) model for Redis, using dedicated users with purpose-driven permissions tailored for Celery's operational requirements.

## **I. Administrative User**

```bash
user ${REDIS_ADMIN_NAME} on >${REDIS_ADMIN_PASSWORD} ~* &* +@all
```

### **Assigned permissions**

- **`~*`**  
    Full access to all keyspaces, enabling management of any data stored in Redis.
- **`&*`**  
    Access to all Pub/Sub channels, necessary for monitoring and broadcasting system-wide events.
- **`+@all`**  
    Grants execution rights to every Redis command category, including administrative and dangerous operations.

### **Role purpose**

Provides full administrative control over the Redis instance.

## **II. Celery User**

```bash
user ${REDIS_USER_NAME} on >${REDIS_USER_PASSWORD} ~* &* +@all -@dangerous -@admin
```

### **Assigned permissions**

- **`~*`**  
    Grants access to all keys in the Redis instance across all database indexes.

- **`&*`**  
    Access to all Pub/Sub channels, necessary for Celery's internal messaging mechanisms and task coordination.

- **`+@all`**  
    Grants execution rights to every Redis command category, providing comprehensive access needed for Celery's complex operations including task queuing, scheduling, result storage, and monitoring.

- **`-@dangerous`**  
    Explicitly revokes access to potentially harmful commands that could compromise data integrity or system stability (e.g., `FLUSHALL`, `FLUSHDB`, `CONFIG SET`). This maintains security while preserving all functional capabilities required by Celery.

- **`-@admin`**  
    Explicitly revokes administrative commands that affect server configuration and management (e.g., `SHUTDOWN`, `BGSAVE`, `ACL`). This ensures the Celery user cannot perform administrative operations that should be reserved for dedicated admin accounts.

### **Role purpose**

This user is designed specifically for Celery's operational needs, which require extensive Redis functionality including:
- Task queuing and message passing.
- Result storage and retrieval.
- Periodic task scheduling (Celery Beat).
- Worker monitoring and coordination.
- Task state management.
- Priority queue operations.

While this configuration is broader than the strictest least-privilege model, it represents a reasonable balance between security best practices and educational purposes of this project.

## **III. Security: Disable the default user**

```bash
user default off nopass
```