# **Celery Core**

*An educational project showcasing how to use Celery with synchronous, multiprocessing and cooperative multitasking approaches.*

## **Project Structure**

```bash
celery-core/
├── app/                        # Main application code
├── docker-compose.yml          # Docker Compose configuration for Redis broker
├── .env.example                # Example environment variables file
├── justfile                    # Project-specific commands using Just
├── pixi.lock                   # Locked dependency versions for reproducible environments
├── pixi.toml                   # Pixi project configuration: environments, dependencies, and platforms
└── playground-testing.ipynb    # Jupyter notebook for playground Celery testing
```

`app/` directory includes its own `README.md` with detailed information about its contents and usage, and every file (except `docker-compose.yml`) contains comprehensive inline comments to explain the code.

## **Redis as Message Broker**

Redis was chosen as the message broker due to its simplicity, reliability, and familiarity from the previous [redis-core](https://github.com/Sierra-Arn/redis-core) project. Since the primary focus here is on demonstrating Celery's capabilities, the `docker-compose.yml` file contains a minimal configuration for the Redis broker, omitting the more detailed comments found in the `redis-core` project's compose files.

## **Dependencies Overview**

- [celery](https://github.com/celery/celery) — 
a distributed task queue framework for Python supporting multiple execution models: synchronous, multiprocessing, and cooperative multitasking.

- [pydantic-settings](https://github.com/pydantic/pydantic-settings) — 
a Pydantic-powered library for managing application configuration and environment variables with strong typing, validation, and seamless `.env` support.

- [redis-py](https://github.com/redis/redis-py) — 
the official Python client for Redis, used here as a message broker for Celery task queues.

- [gevent](https://github.com/gevent/gevent) — 
a coroutine-based Python networking library that uses greenlets to provide a high-level synchronous API on top of the libev event loop, used here for efficient I/O-bound task processing in Celery workers.

- [just](https://github.com/casey/just) — 
a lightweight, cross-platform command runner that replaces complex shell scripts with clean, readable, and reusable project-specific recipes. [^1]

[^1]: Despite using `pixi`, there are issues with `pixi tasks` regarding environment variable handling from `.env` files and caching mechanism that is unclear and causes numerous errors. In contrast, `just` provides predictable, transparent execution without the complications encountered with `pixi tasks` system. I truly hope `pixi tasks` have been improved by the time you're reading this! <33

### **Testing & Development Dependencies**

- [JupyterLab](https://github.com/jupyterlab/jupyterlab) — 
a next-generation web-based interactive development environment for Jupyter notebooks; used here to create interactive documents for testing and verifying code execution.


## **Quick Start**

### **I. Prerequisites**

- [Docker and Docker Compose](https://docs.docker.com/engine/install/).
- [Pixi](https://pixi.sh/latest/) package manager.

> **Platform note**: All development and testing were performed on `linux-64`.  
> If you're using a different platform, you’ll need to:
> 1. Update the `platforms` list in the `pixi.toml` accordingly.
> 2. Ensure that platform-specific scripts are compatible with your operating system or replace them with equivalents.

### **II. Initial Setup**

1. **Clone the repository**

    ```bash
    git clone git@github.com:Sierra-Arn/celery-core.git
    cd celery-core
    ```

2. **Install dependencies**

    ```bash
    pixi install --all
    ```

3. **Activate pixi environment**

    ```bash
    pixi shell
    ```

4. **Setup environment configuration**

    ```bash
    just copy-env
    just make-x
    just gen-acl
    ```

5. **Start Redis database**

    ```bash
    just redis-up
    ```

6. **Start Celery workers** (each in a separate terminal)
    
    ```bash
    pixi run just worker-cpu
    ```
    
    ```bash
    pixi run just worker-io
    ```

    > **Note:**  
    It's normal to see red error messages in the CPU-bound worker logs — tasks are designed to randomly fail to verify Celery's error handling behavior in the absence of retry logic. For the I/O-bound worker, failed tasks will automatically be retried — this is expected behavior.

### **III. Testing**

Once the broker and Celery workers are ready, you can run and test the Celery implementation with the interactive Jupyter notebook `playground-testing.ipynb`. It demonstrates all core functionality — including task dispatch via `delay`, `apply_async`, `apply`, and result retrieval with `get()`.

1. **Launch JupyterLab**

    ```bash
    pixi run -e test jupyter lab
    ```

2. **Test the Celery implementation**
    - JupyterLab should open automatically in your browser at the default address.
    - Open the notebook and run the cells interactively.

3. **(Optional) Verify database manually**  
You can open a Redis shell to manually verify that everything is working correctly:

    ```bash
    just redis-shell
    ```

### **IV. Cleanup**

When you finish testing:

1. **Stop JupyterLab**  
   In the terminal where JupyterLab is running, press `Ctrl+C` to shut it down.

2. **Stop Celery workers**  
   In each terminal where a celery worker is running, press `Ctrl+C` to shut it down.

3. **Stop Redis**

    ```bash
    just redis-down
    ```

## **License**

This project is licensed under the [BSD-3-Clause License](LICENSE).
