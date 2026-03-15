# app/task_queue/workers/cli.py
import argparse


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for worker configuration.

    Returns
    -------
    argparse.Namespace
        Parsed arguments with worker configuration parameters.

    Notes
    -----
    `parse_args()` returns argparse.Namespace whose attributes are dynamically set,
    so IDE may highlight them as unresolved. This is expected behavior.
    """

    parser = argparse.ArgumentParser(
        description="Start Celery worker with custom configuration"
    )
    parser.add_argument(
        "--name",
        type=str,
        default="celery_worker",
        dest="name",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=1,
        dest="concurrency",
    )
    parser.add_argument(
        "--prefetch-multiplier",
        type=int,
        default=1,
        dest="prefetch_multiplier",
    )
    parser.add_argument(
        "--loglevel",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        dest="loglevel",
    )

    return parser.parse_args()