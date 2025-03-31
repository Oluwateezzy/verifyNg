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


@router.post("/verify", summary="Verify an audio file")
async def verify_audio(file: UploadFile = File(...)):
    """
    Endpoint to verify an uploaded audio file.
    - Ensures the file is an audio type.
    - Only allows .wav files.
    - Checks if the duration is within the allowed limit (5 seconds).
    - Sends the file to a Celery queue for processing.
    """

    if file.content_type.split("/")[0] != "audio":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not an audio file"
        )

    if file.content_type.split("/")[1] != "wav":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Accepted Audio Type - .wav"
        )

    audio_bytes = await file.read()

    audio_data, sample_rate = sf.read(io.BytesIO(audio_bytes))

    duration = len(audio_data) / sample_rate

    if duration > 5:
        raise HTTPException(
            status_code=400, detail="Audio file must be less than 5 seconds"
        )

    task_id = str(uuid.uuid4())

    # Send the audio file for background processing using Celery
    task = process_audio_task.apply_async(args=[audio_bytes, task_id])

    return BaseResult(
        status=status.HTTP_200_OK, message="Message Sent to queue", data={task.id}
    )


@router.get("/status/{task_id}")
async def get_audio_status(task_id: str):
    """
    Fetches the processing status of an audio verification task.
    - Checks the current state of the Celery task.
    - Returns the status and result if completed.
    - Returns an error message if the task fails.
    """

    task_result = AsyncResult(task_id)

    if task_result.state == "PENDING":
        return {"status": "Processing..."}
    elif task_result.state == "SUCCESS":
        return {"status": "Completed", "result": task_result.result}
    elif task_result.state == "FAILURE":
        return {"status": "Failed", "error": str(task_result.result)}

    return {"status": "Unknown"}
