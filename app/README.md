# **Application Structure**

*This README provides a high-level architectural overview of the project: what each component is for and why it exists. For implementation details refer to the docstrings and comments inside each file.*

## **I. `task_queue/` — the Task Queue Layer**

1. **`shared/base_config.py`**  
    Provides a base configuration class built with Pydantic, designed for inheritance by other configuration classes to enable consistent loading of settings from `.env` with strict validation and module-specific prefixes.

2. **`config.py`**  
    Provides Celery configuration singleton built with Pydantic, loaded from `.env` with strict validation. Defines settings for broker, result backend, serialization, queues, and other Celery-specific parameters.

3. **`instance.py`**  
    Provides the main Celery application instance singleton, pre-configured from validated settings and ready to define and execute tasks.

4. **`workers/`**  
    Contains worker-specific configuration and management logic.
    - **`config.py`** — Defines configuration schema for individual Celery worker instances (name, queue, pool, concurrency, etc.).
    - **`worker.py`** — Provides a generic worker class that encapsulates the logic for starting and managing a Celery worker process with a given configuration.
    - **`cpu_bound.py`** — Pre-configured worker instance optimized for CPU-intensive tasks using the 'prefork' pool.
    - **`io_bound.py`** — Pre-configured worker instance optimized for I/O-intensive tasks using the 'gevent' pool.

## **II. `services/` — the Business Logic Layer**

1. **`__init__.py`**  
    Provides mock task service implementations that demonstrate how to define and execute Celery tasks for different workload types (CPU-bound and I/O-bound), including retry policies and queue routing.

## **III. `initialization/` — Bootstrapping Redis**

1. **`01-create-users.acl`**  
    Defines multiple Redis users and assigns minimal necessary permissions to each, following the principle of least privilege.

2. **`generate-redis-acl.sh`**  
    Shell script that generates the `01-create-users.acl` file by injecting Redis credentials from `.env` — bypassing the ACL format's lack of environment variables support.

3. **`README.md`**  
    Documents the role-based access control (RBAC) model used in this project. It explains: 
    - which Redis users exist,
    - what permissions each one holds,
    - why those specific permissions are granted.