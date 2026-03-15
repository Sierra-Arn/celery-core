# app/task_queue/exchange.py
from kombu import Exchange
from .config import celery_config


tasks_exchange = Exchange(
    celery_config.exchange_name,
    type=celery_config.exchange_type,
)
"""
Shared Kombu exchange instance configured via application settings.

This exchange serves as the single routing point for all task queues,
directing messages to the appropriate queue based on the routing key
provided by the producer at the time of task dispatch.
"""