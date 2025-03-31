import io
from typing import Any, Dict
import uuid
from fastapi import (
    APIRouter,
    BackgroundTasks,
    File,
    HTTPException,
    UploadFile,
    status,
)
from pydantic import BaseModel, Field
from app.utils.result.base_result import BaseResult
import soundfile as sf
from app.worker import (
    process_audio_background,
    process_audio_task,
    task_store,
    TaskResult,
)
from celery.result import AsyncResult

router = APIRouter()


MAX_FILE_SIZE = 10 * 1024 * 1024


@router.post("/test/upload-audio", summary="Verify an audio file using in-memory")
async def upload_audio(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
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

    background_tasks.add_task(process_audio_background, audio_bytes, task_id)

    return BaseResult(
        status=status.HTTP_200_OK,
        message="Message Sent to queue",
        data={"status": "processing", "task_id": task_id},
    )


@router.get(
    "/test/status/{task_id}",
    summary="Fetches the processing status of an audio verification task from in-memory.",
)
async def get_audio_status(task_id: str):

    # Check if task exists
    if task_id not in task_store:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

    task_result = task_store[task_id]

    if task_result["status"] == "PENDING":
        return BaseResult(
            status=status.HTTP_200_OK,
            message="Audio Processing",
            data={"status": "Processing...", "task_id": task_id},
        )
    elif task_result["status"] == "RUNNING":
        return BaseResult(
            status=status.HTTP_200_OK,
            message="Audio Processing",
            data={"status": "Processing...", "task_id": task_id},
        )
    elif task_result["status"] == "SUCCESS":
        return BaseResult(
            status=status.HTTP_200_OK,
            message="Audio Processing succeed",
            data={"status": "Completed", "result": task_result["result"]},
        )
    elif task_result["status"] == "FAILURE":
        return BaseResult(
            status=status.HTTP_200_OK,
            message="Audio Processing Failed",
            data={"status": "Failed", "error": task_result["error"]},
        )
    return BaseResult(
        status=status.HTTP_200_OK,
        message="Audio Processing Failed",
        data={"status": "Unknown", "task_id": task_id},
    )


@router.post("/upload-audio", summary="Verify an audio file using celery and redis")
async def verify_audio(file: UploadFile = File(...)):

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


@router.get(
    "/status/{task_id}",
    summary="Fetches the processing status of an audio verification task from using celery and redis.",
)
async def get_audio_status(task_id: str):

    task_result = AsyncResult(task_id)

    if task_result.state == "PENDING":
        return {"status": "Processing..."}
    elif task_result.state == "SUCCESS":
        return {"status": "Completed", "result": task_result.result}
    elif task_result.state == "FAILURE":
        return {"status": "Failed", "error": str(task_result.result)}

    return {"status": "Unknown"}
