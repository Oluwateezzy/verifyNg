import io
import uuid
from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
    requests,
    status,
    BackgroundTasks,
)
from pydantic import Field
from app.utils.result.base_result import BaseResult
import soundfile as sf
from app.worker import process_audio_task
from celery.result import AsyncResult

router = APIRouter()

MAX_FILE_SIZE = 10 * 1024 * 1024


@router.post("/verify", summary="Verify an audio file with")
async def verify_audio(backgroundTask: BackgroundTasks, file: UploadFile = File(...)):
    audio_bytes = await file.read()
    audio_data, sample_rate = sf.read(io.BytesIO(audio_bytes))

    # Calculate duration
    duration = len(audio_data) / sample_rate

    if duration > 5:
        raise HTTPException(
            status_code=400, detail="Audio file must be less than 5 seconds"
        )

    # Generate a unique task ID
    task_id = str(uuid.uuid4())

    # Send to Celery queue
    task = process_audio_task.apply_async(args=[audio_bytes, task_id])

    return BaseResult(
        status=status.HTTP_200_OK, message="Message Sent to queue", data={task.id}
    )


@router.get("/status/{task_id}")
async def get_audio_status(task_id: str):
    """Fetches the processing status."""

    task_result = AsyncResult(task_id)
    if task_result.state == "PENDING":
        return {"status": "Processing..."}
    elif task_result.state == "SUCCESS":
        return {"status": "Completed", "result": task_result.result}
    elif task_result.state == "FAILURE":
        return {"status": "Failed", "error": str(task_result.result)}

    return {"status": "Unknown"}
