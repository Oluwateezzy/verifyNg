from celery import Celery
import random
import time

from app.core.config import settings

# Celery configuration
celery_app = Celery(
    "worker",
    broker="redis://default:LP1uVzR2tbS0DK80j6kpvS1iDBt4qFDX@redis-10493.c270.us-east-1-3.ec2.redns.redis-cloud.com:10493",
    backend="redis://default:LP1uVzR2tbS0DK80j6kpvS1iDBt4qFDX@redis-10493.c270.us-east-1-3.ec2.redns.redis-cloud.com:10493",
)


@celery_app.task
def process_audio_task(audio_bytes, task_id):
    """Simulates processing audio and returns True or False."""

    # Simulating processing time
    time.sleep(3)  # Simulate some heavy processing

    # Simulated result (randomly True or False)
    result = random.choice([True, False])

    return {"task_id": task_id, "status": "success", "verified": result}
