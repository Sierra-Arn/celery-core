# **Application Structure**

*This README provides a high-level architectural overview of the project: what each component is for and why it exists. For implementation details refer to the docstrings and comments inside each file.*

## I. **`shared/base_config.py`**

Provides a base configuration class built with Pydantic, designed for inheritance by other configuration classes to enable consistent loading of settings from `.env` with strict validation and module-specific prefixes.

## II. **`db/`**

Database layer. Contains Redis configuration and bootstrapping scripts for ACL and user permissions.

### i. **`config.py`**

Provides Redis configuration singleton built with Pydantic, loaded from `.env` with strict validation. Defines settings for connection, authentication, and client behavior.

### ii. **`initialization/`**

Bootstrapping scripts and configuration for Redis ACL and user permissions.

1. **`01-create-users.acl`**  
    Defines multiple Redis users and assigns minimal necessary permissions to each, following the principle of least privilege.

2. **`generate-redis-acl.sh`**  
    Shell script that generates the `01-create-users.acl` file by injecting Redis credentials from `.env` — bypassing the ACL format's lack of environment variables support.

3. **`README.md`**  
    Documents the role-based access control (RBAC) model used in this project. It explains:
    - which Redis users exist,
    - what permissions each one holds,
    - why those specific permissions are granted.

## III. **`task_queue/`**

Task queue layer. Contains Celery configuration, exchange and queue definitions, worker management, and mock task implementations.

### i. **`config.py`**

Provides Celery configuration singleton built with Pydantic, loaded from `.env` with strict validation. Defines settings for broker, result backend, serialization, queue names, and other Celery-specific parameters.

### ii. **`exchange.py`**

Provides the shared Kombu exchange instance used for routing messages to task queues. A single direct exchange is used for all queues following the standard direct exchange pattern.

### iii. **`queue.py`**

Defines the CPU-bound and I/O-bound task queues, each bound to the shared exchange via a direct routing key matching the queue name.

### iv. **`instance.py`**

Provides the main Celery application instance singleton, pre-configured from validated settings with registered queues and exchange, ready to define and execute tasks.

### v. **`tasks/__init__.py`**

Provides mock task implementations that demonstrate CPU-bound and I/O-bound workload patterns, including retry policies and queue routing.

### vi. **`workers/`**

Contains worker configuration and management logic.

1. **`schema.py`**  
    Defines the Pydantic configuration schema for individual Celery worker instances (name, queue, pool, concurrency, etc.).

2. **`cli.py`**  
    Provides a shared CLI argument parser for launching workers with runtime-configurable parameters.

3. **`instance.py`**  
    Provides a generic worker class that encapsulates the logic for starting and managing a Celery worker process with a given configuration.

4. **`cpu_bound.py`**  
    Entry point for the CPU-bound worker, pre-configured to use the prefork pool for parallel multiprocessing execution.

5. **`io_bound.py`**  
    Entry point for the I/O-bound worker, pre-configured to use the gevent pool for cooperative multitasking during I/O waits.