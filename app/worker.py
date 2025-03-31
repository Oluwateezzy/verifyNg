from celery import Celery
import random
import time

from app.core.config import settings

# Celery configuration
celery_app = Celery("worker", broker=settings.redis_url, backend=settings.redis_url)


@celery_app.task
def process_audio_task(audio_bytes, task_id):
    """Simulates processing audio and returns True or False."""

    # Simulating processing time
    time.sleep(3)  # Simulate some heavy processing

    # Simulated result (randomly True or False)
    result = random.choice([True, False])

    return {"task_id": task_id, "status": "success", "verified": result}
