from typing import Any, Dict
from celery import Celery
import random
import time

from pydantic import BaseModel

from app.core.config import settings

# Celery configuration
celery_app = Celery("worker", broker=settings.redis_url, backend=settings.redis_url)

task_store: Dict[str, Dict[str, Any]] = {}


class TaskResult(BaseModel):
    task_id: str
    status: str
    verified: bool = None
    error: str = None


@celery_app.task
def process_audio_task(audio_bytes, task_id):
    """Simulates processing audio and returns True or False."""

    # Simulating processing time
    time.sleep(3)  # Simulate some heavy processing

    # Simulated result (randomly True or False)
    result = random.choice([True, False])

    return {"task_id": task_id, "status": "success", "verified": result}


def process_audio_background(audio_bytes, task_id):
    try:
        # Set status to running
        task_store[task_id] = {"status": "RUNNING"}

        # Process audio
        time.sleep(3)

        # Simulated result (randomly True or False)
        result = random.choice([True, False])

        # Store the result
        task_store[task_id] = {
            "status": "SUCCESS",
            "result": {"task_id": task_id, "status": "success", "verified": result},
        }

        return {"task_id": task_id, "status": "success", "verified": result}
    except Exception as e:
        # Store the error
        task_store[task_id] = {"status": "FAILURE", "error": str(e)}
        return {"task_id": task_id, "status": "error", "error": str(e)}
